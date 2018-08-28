######################################
import os, sys, time, math, json, numpy as np
from networkx.readwrite import json_graph
from ctypes import cdll
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, reducev4 as reduce, solver, init
######################################
myprint = util.mylog
######################################
def work(arguments, rank):
    print ("\t\t\t\tworker #"+str(rank)+" I'm working,\t")
    configs       = init.initialize_worker (arguments) #at this point, configs doesnt yet contain configs ['worker_load'] and configs ['num_workers'], obtained after json-loading configs json-dumped by master (below)
    M, configs_update, loaded =  None, None, False
    
    log_dir = configs['output_directory']+"logs_raw_instances" 
    while not os.path.isdir (log_dir): # master will create this dir
        time.sleep(5)
    while not loaded: #wait for master.py to dump  updated configs and get it
        try:
            if os.path.isdir(configs['output_directory']) and os.path.isfile(util.slash (configs['output_directory'])+ "M") and os.path.isfile(util.slash(configs['output_directory'])+ "configs_raw_instances/configs_"+str(rank).rjust(4,'0')):
                if (time.time()-os.path.getmtime(util.slash(configs['output_directory'])+ "configs_raw_instances/configs_"+str(rank).rjust(4,'0'))) > 20:  #give master a chance to finish writing M/configs
                    f = open (os.path.join(configs['output_directory'], "M"),'r')
                    M = json_graph.node_link_graph(json.load(f))
                    f.close()            
                    f = open (os.path.join(configs['output_directory'], "configs_raw_instances/configs_"+str(rank).rjust(4,'0')),'r')
                    configs_update = json.load(f)
                    f.close() 
                    loaded = True
        except Exception as e:
            with open (log_dir+"/worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as reporter:
                reporter.write ("worker "+str(rank)+": ERROR loading M/configs .. Exiting .. ")
                reporter.write("\t\tException "+str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                reporter.write("\t\texc_type "+str(exc_type)+'\n\t\tfname '+str(fname)+'\n\t\tline no. '+str(exc_tb.tb_lineno))
                reporter.flush()
                sys.exit(1)
    #at this point now master and workers have the same config dictionary
    configs={}
    for key in configs_update.keys():
        configs[key] = configs_update[key]    
    try:
        os.rename(os.path.join(configs['output_directory'], "configs_raw_instances/configs_"+str(rank).rjust(4,'0')), os.path.join(configs['output_directory'], "configs_raw_instances/configs_"+str(rank).rjust(4,'0')+"_loaded_"+configs['timestamp']))
    except:
        with open (log_dir+"/worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as reporter:
            reporter = open (log_dir+"/worker_"+configs['timestamp']+".log", 'a')
            reporter.write ("\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": FATAL, unable to rename "+os.path.join(configs['output_directory'], "configs_raw_instances/configs_"+str(rank).rjust(4,'0'))+"\nExiting..")
            sys.exit(1)
    reporter=log_dir+"/worker_"+configs['timestamp']+".log"
    if rank == 1: # have worker 1 report activity 
        #reporter = open (log_dir+"/worker_"+configs['timestamp']+".log", 'a') 
        if not os.path.isdir(configs['output_directory']+ "logs_raw_instances"):
            os.makedirs(configs['output_directory']+ "logs_raw_instances")       
        
        myprint(reporter, "\n=======================================\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": loaded configs from "+configs['output_directory']+ "\nnumber of PT_pairs ".rjust(16,' ')+str(len(configs['PT_pairs_dict'].keys()))+"\n=======================================\n")

    #--------------------------------------------------
    knapsack_solver = cdll.LoadLibrary(configs['KP_solver_binary'])
    #--------------------------------------------------
    if rank == 1:    
        myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": loaded solver "+configs['KP_solver_binary'])
        myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I am in " +configs['reduction_mode']+ " mode, my workload is "+str(configs['worker_load']))
    t0=time.time()
    
    myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says: my workload is "+str(configs['worker_load'] )+"\t.. Im in "+configs['reduction_mode']+" mode")
    if configs['worker_load'] > 0:
        for k in sorted([int(k) for k in configs['PT_pairs_dict'].keys()]): #json decoding turns integer keys into strings, this is a workaround
            i = str(k) 
    
            #----------------------------------------------------------------------------------------------------------------------------------------------------
            current_dir = util.slash(configs['DUMP_DIR'])+str(k).rjust(4,'0')+"_p_"+str(configs['PT_pairs_dict'][i][0])+ "_t_"+str(configs['PT_pairs_dict'][i][1])+"/"
            if not os.path.isdir(current_dir):#one of the workers will be the first to make this dump directory
                try:
                    os.makedirs(current_dir)
                except:
                    pass
            
            current_file       = current_dir + "worker_"+str(rank).rjust(4,'0')+ "_p_"+str(float(configs['PT_pairs_dict'][i][0]))+ "_t_"+str(float(configs['PT_pairs_dict'][i][1]))+"_RAW"
            instances_so_far   = 0
            output_file_RAW    = None
            FirstLine          = True
            if os.path.isfile(current_file):                
                tmp = open(current_file,'r').readlines()
                output_file_RAW    = open (current_file, 'w')
                if len(tmp) >= 5 : 
                    instances_so_far = int (len(tmp) / 5)
                    if instances_so_far >= configs['worker_load']:
                        try:
                            os.rename (current_file, current_file+'.done') #master will use 'done' as signal this worker is done writing to this file
                        except:
                            reporter.write ("\n\t\t\t\tworker #"+str(rank)+" says: WARNING, unable to rename "+current_file+'.done .. master will wait forever')
                            pass
                        continue
                    output_file_RAW.write('\n'.join([line.strip() for line in tmp[0:instances_so_far*5]])) #chop off trailing lines
                    output_file_RAW.flush()
                    FirstLine = False
                else:
                    output_file_RAW    = open (current_file, 'w')
            elif os.path.isfile(current_file+".done"):
                continue # go to the next PT
            else:
                output_file_RAW    = open (current_file, 'w')
            #---------------------------------------------------------------------------------------------------------------------------------------------------- 
            #calculate pressure % of nodes or edges
            p=0
            if configs['advice_upon']=='nodes':
                p = math.ceil ((float(configs['PT_pairs_dict'][i][0])/100.0)*len(M.nodes()))
            elif configs['advice_upon']=='edges':
                p = math.ceil ((float(configs['PT_pairs_dict'][i][0])/100.0)*len(M.edges()))
            else:
                with open (log_dir+"/worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as reporter:
                    reporter.write("FATAL: unrecognized advice_upon parameter: "+str(configs['advice_upon'])+"\nExiting ..\n")
                    sys.exit(1) 
            # t% of relevant edges will be calculated after KP instance is generated and relevant edges become known
            t = configs['PT_pairs_dict'][i][1]
            #----------------------------------------------------------------------------------------------------
            kp_instances = None
            if configs['reduction_mode']=='reverse':
                kp_instances = reduce.reverse_reduction(M, p, t, max(0, configs['worker_load']-instances_so_far), configs['advice_upon'], configs['biased'], configs['BD_criteria'])
                if rank == 1:
                    myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": reverse-reduced for p="+str(configs['PT_pairs_dict'][i][0])+"% ("+str(p)+" "+configs['advice_upon']+")\tt="+str(t)+"\tadvice_upon:"+configs['advice_upon']+", biased:"+str(configs['biased']))
            elif configs['reduction_mode']=='scramble':
                kp_instances = reduce.scramble_reduction(M, p, t, max(0, configs['worker_load']-instances_so_far), configs['advice_upon'], configs['biased'], configs['BD_criteria'])
                if rank == 1:
                    myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": scramble-reduced for p="+str(configs['PT_pairs_dict'][i][0])+"% ("+str(p)+" "+configs['advice_upon']+")\tt="+str(t)+"%\tadvice_upon:"+configs['advice_upon']+", biased:"+str(configs['biased']))
            else:
                myprint (reporter, "\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I don't know this reduction mode, I'm exiting ... Goodbye!")
                sys.exit(1)
            #-----------------------------------------------------------------------------------------------------
            avg_timer=[0]
            for kp in kp_instances: #consider multiprocessing here
                #if rank ==1:
                #    print ("solving for p"+str(float(p)/len(M.nodes())*100)+"\tt"+str(t))
                timer0 = time.time()
                a_result = solver.solve_knapsack (kp, knapsack_solver)
                timer1 = time.time()
                if len (a_result)>0:
                    Gs, Bs, Ds, Xs = [],[],[],[]
                    GENES_in, GENES_out, execution_stats = a_result['GENES_in'], a_result['GENES_out'], a_result['execution_stats']

                    for g in GENES_in:
                        Gs.append(g[0]+'$'+str(M.in_degree(g[0]))+'$'+str(M.out_degree(g[0])))
                        Bs.append(g[1])
                        Ds.append(g[2])
                        Xs.append(1)
                    for g in GENES_out:
                        Gs.append(g[0]+'$'+str(M.in_degree(g[0]))+'$'+str(M.out_degree(g[0])))
                        Bs.append(g[1])
                        Ds.append(g[2])
                        Xs.append(0)
                    if  FirstLine==True:
                        FirstLine=False
                    else:
                        output_file_RAW.write('\n')
                    output_file_RAW.write('\n'.join([' '.join(Gs),  ' '.join([str(b) for b in Bs]),    ' '.join([str(d) for d in Ds]),      ' '.join([str(x) for x in Xs]),     ' '.join([key+'$'+str(execution_stats[key]) for key in execution_stats.keys()])     ]))
                    output_file_RAW.flush()      
                    avg_timer.append  ((timer1-timer0))
            output_file_RAW.flush()
            output_file_RAW.close()
            try:
                os.rename (current_file, current_file+'.done') #master will use 'done' as signal this worker is done writing to this file
            except:
                myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": WARNING, unable to rename "+current_file+'.done .. master will wait forever')
                pass
            if rank == 1:
                myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": solver timer \t "+str(int(np.average(avg_timer)))+" s")
    t1=time.time()
    if rank == 1:
        myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I'm done ("+str(int(t1-t0))+") ... Goodbye!") 
    myprint (reporter, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I'm done ("+str(int(t1-t0))+" sec) ... Goodbye!") 
