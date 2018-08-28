######################################
import os, sys, time, math, json, numpy as np
from time import process_time as ptime
from networkx.readwrite import json_graph
from ctypes import cdll
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, reducev4 as reduce, solver_execstats as solver, init_execstats as init
mywrite = util.mywrite
myprint = util.myprint
######################################
def setup(arguments, rank):
    myprint("\n\t\t\t\tworker #"+str(rank)+": I'm setting up")
    configs       = init.initialize_worker (arguments) #at this point, configs doesnt yet contain configs ['worker_load'] and configs ['num_workers'], obtained after json-loading configs json-dumped by master (below)
    log_dir = configs['log_dir']
    
    M, configs_update, loaded =  None, None, False
    
    
    while not os.path.isdir (log_dir): # master will create this dir
        time.sleep(5)
    while not loaded: #wait for master.py to dump  updated configs and get it
        try:
            if os.path.isdir(configs['output_directory']) and os.path.isfile(util.slash (configs['output_directory'])+ "M") and os.path.isfile(configs['configs_dir']+ "configs_"+str(rank).rjust(4,'0')):
                if (time.time()-os.path.getmtime(configs['configs_dir']+ "configs_"+str(rank).rjust(4,'0'))) > 20:  #give master a chance to finish writing M/configs
                    f = open (os.path.join(configs['output_directory'], "M"),'r')
                    M = json_graph.node_link_graph(json.load(f))
                    f.close()            
                    f = open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'r')
                    configs_update = json.load(f)
                    f.close() 
                    loaded = True
        except Exception as e:
            with open (log_dir+"worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as error:
                error.write ("worker "+str(rank)+": ERROR loading M/configs .. Exiting .. ")
                error.write("\t\tException "+str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                error.write("\t\texc_type "+str(exc_type)+'\n\t\tfname '+str(fname)+'\n\t\tline no. '+str(exc_tb.tb_lineno))
                error.flush()
                sys.exit(1)
    #at this point now master and workers have the same config dictionary
    
    configs={}
    for key in configs_update.keys():
        configs[key] = configs_update[key]    
    try:
        os.rename(os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')), os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')+"_loaded_"+configs['timestamp']))
    except:
        with open (log_dir+"worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as error:
            error.write ("\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": FATAL, unable to rename "+os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0'))+"\nExiting..")
            sys.exit(1)
    log = log_dir+"worker_"+configs['timestamp']+".log"
    if rank == 1: # have worker 1 report activity
        mywrite(log, "\n=======================================\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": loaded configs from "+configs['output_directory']+ "\nnumber of PT_pairs ".rjust(16,' ')+str(len(configs['PT_pairs_dict'].keys()))+"\n=======================================\n")
    
    #--------------------------------------------------
    knapsack_solver = cdll.LoadLibrary(configs['KP_solver_binary'])
    #--------------------------------------------------
    
    if rank == 1:    
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I am in " +configs['reduction_mode']+ " mode, my workload is "+str(configs['worker_load']))
        mywrite(log, "\n\t\t\t\tmy workload is "+str(configs['worker_load'] )+"\t.. Im in "+configs['reduction_mode']+" mode")
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": loaded solver "+configs['KP_solver_binary'])    
    return configs, knapsack_solver, log, M
######################################        
def next_file(configs, rank, log, i):
    current_dir = util.slash(configs['DUMP_DIR'])+str(i).rjust(4,'0')+"_p_"+str(configs['PT_pairs_dict'][i][0])+ "_t_"+str(configs['PT_pairs_dict'][i][1])+"/"
    if not os.path.isdir(current_dir):#one of the workers will be the first to make this dump directory
        try:
            os.makedirs(current_dir)
        except:
            pass
    
    RAW_file_path       = current_dir + "worker_"+str(rank).rjust(4,'0')+ "_p_"+str(float(configs['PT_pairs_dict'][i][0]))+ "_t_"+str(float(configs['PT_pairs_dict'][i][1]))+"_EXECSTATS"
    
    instances_so_far   = 0
    RAW_writer    = None
    FirstLine          = True
    done=False
    if os.path.isfile(RAW_file_path):                
        tmp = open(RAW_file_path,'r').readlines()
        RAW_writer    = open (RAW_file_path, 'w')
        if len(tmp) >= 5 : 
            instances_so_far = int (len(tmp) / 5)
            if instances_so_far >= configs['worker_load']:
                try:
                    os.rename (RAW_file_path, RAW_file_path+'.done') #master will use 'done' as signal this worker is done writing to this file
                except:
                    mywrite (log, "\n\t\t\t\tworker #"+str(rank)+" says: WARNING, unable to rename "+RAW_file_path+'.done .. master will wait forever')
                    pass
                done=True
            RAW_writer.write('\n'.join([line.strip() for line in tmp[0:instances_so_far*5]])) #chop off trailing lines
            RAW_writer.flush()
            FirstLine = False
        else:
            RAW_writer    = open (RAW_file_path, 'w')
    elif os.path.isfile(RAW_file_path+".done"):
        done = True
    else:
        RAW_writer    = open (RAW_file_path, 'w')
    return RAW_writer, RAW_file_path, done, instances_so_far, FirstLine
######################################  
def next_pt(configs, M, i):
    #calculate pressure % of nodes or edges
    p=0
    if configs['advice_upon']=='nodes':
        p = math.ceil ((float(configs['PT_pairs_dict'][i][0])/100.0)*len(M.nodes()))
    elif configs['advice_upon']=='edges':
        p = math.ceil ((float(configs['PT_pairs_dict'][i][0])/100.0)*len(M.edges()))
    else:
        with open (configs['log_dir']+"worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as reporter:
            reporter.write("FATAL: unrecognized advice_upon parameter: "+str(configs['advice_upon'])+"\nExiting ..\n")
            sys.exit(1) 
    # t% of relevant edges will be calculated after KP instance is generated and relevant edges become known
    t = configs['PT_pairs_dict'][i][1]
    return p,t
######################################             
def next_instances(configs,rank, log,instances_so_far, M, p, t, i):
    kp_instances = None
    if configs['reduction_mode']=='reverse':
        kp_instances = reduce.reverse_reduction(M, p, t, max(0, configs['worker_load']-instances_so_far), configs['advice_upon'], configs['biased'], configs['BD_criteria'])
        if rank == 1:
            mywrite (log,"\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": reverse-reduced for p="+str(configs['PT_pairs_dict'][i][0])+"% ("+str(p)+" "+configs['advice_upon']+")\tt="+str(t)+"\tadvice_upon:"+configs['advice_upon']+", biased:"+str(configs['biased']))
    elif configs['reduction_mode']=='scramble':
        kp_instances = reduce.scramble_reduction(M, p, t, max(0, configs['worker_load']-instances_so_far), configs['advice_upon'], configs['biased'], configs['BD_criteria'])
        if rank == 1:
            mywrite (log,"\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": scramble-reduced for p="+str(configs['PT_pairs_dict'][i][0])+"% ("+str(p)+" "+configs['advice_upon']+")\tt="+str(t)+"%\tadvice_upon:"+configs['advice_upon']+", biased:"+str(configs['biased']))
    else:
        mwrite(log, "\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I don't know this reduction mode, I'm exiting ... Goodbye!")
        sys.exit(1)
    return kp_instances
######################################                  
def process(kp_instances, knapsack_solver, rank, log, RAW_writer, RAW_file_path, FirstLine):
    avg_timer = []
    for kp in kp_instances: #consider multiprocessing here
        a_result = solver.solve_knapsack (kp, knapsack_solver)
        if len (a_result)>0:
            
            # a_result = num_white_genes, num_black_genes, num_grey_genes, TOTAL_Bin, TOTAL_Din, TOTAL_Bou, TOTAL_Dou, core_size, Ctime_s, Ctime_ms, PythonTime 
            
            if  FirstLine==True:
                FirstLine=False
            else:
                RAW_writer.write('\n')
            RAW_writer.write(' '.join([str(x) for x in a_result]))
            RAW_writer.flush()      
            avg_timer.append  (a_result[-1])
    RAW_writer.flush()
    RAW_writer.close()
    
    if len(avg_timer)==0:
        avg_timer=[0]
    try:
        os.rename (RAW_file_path, RAW_file_path+'.done') #master will use 'done' as signal this worker is done writing to this file
    except:
        mywrite(log,"\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": WARNING, unable to rename "+RAW_file_path+'.done .. master will wait forever')
        pass
    if rank == 1:
        mywrite(log,"\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": solver timer \t "+str(int(np.average(avg_timer)))+" s")
######################################
def work(arguments, rank):
    
    configs, knapsack_solver, log, M = setup (arguments, rank)

    t0=ptime()
    if configs['worker_load'] > 0:
        for i in sorted([int(k) for k in configs['PT_pairs_dict'].keys()]): #json decoding turns integer keys into strings, this is a workaround
            i = str(i)
            
            RAW_writer, RAW_file_path,  done, instances_so_far, FirstLine = next_file(configs, rank, log, i)
            
            if done:
                continue # move on to the next p,t pair
            
            p, t = next_pt(configs, M, i)

            kp_instances = next_instances(configs, rank, log,instances_so_far, M, p, t, i)
            
            process(kp_instances, knapsack_solver, rank, log, RAW_writer, RAW_file_path, FirstLine)
            
    t1=ptime()
    mywrite(log, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I'm done ("+str(int(t1-t0))+" sec) ... Goodbye!") 
