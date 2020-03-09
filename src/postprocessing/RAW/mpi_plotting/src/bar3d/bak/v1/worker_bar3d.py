######################################
import sys,os
sys.path.insert(0, os.getenv('lib'))
import time, math, pickle, numpy as np,  init_plotting as init, util_plotting as util
######################################
#--------------------------------------------------------------------------------------
def setup (arguments, rank):
    print ("\t\t\t\tworker #"+str(rank)+" I'm working,\t",end='')
    configs       = init.load_simulation_configs (arguments, rank) #at this point, configs doesnt yet contain configs ['worker_load'] and configs ['num_workers'], obtained after pickle-loading configs pickle-dumped by master (below)
    M, configs_update, loaded =  None, None, False

    log_dir = configs['logs_dir']
    while not loaded: #wait for master.py to dump  updated configs and get it
        time.sleep(5)
        try:
            if os.path.isdir(configs['output_dir']) and  os.path.isfile(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0')):
                if (time.time()-os.path.getmtime(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0'))) > 5:  #give master a chance to finish writing M/configs
                    f = open (os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')),'rb')
                    configs_update = pickle.load(f)
                    f.close()
                    loaded = True
        except Exception as e:
            with open (log_dir+"worker_"+str(rank)+"_ERROR_"+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+".log", 'a') as reporter:
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
        os.rename(os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')), os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')+"_loaded_"+configs['timestamp']))
    except:
        with open (log_dir+"worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as reporter:
            reporter = open (log_dir+"worker_"+configs['timestamp']+".log", 'a')
            reporter.write ("\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": FATAL, unable to rename "+os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0'))+"\nExiting..")
            sys.exit(1)
    reporter = None
    if rank == 1: # have worker 1 report activity 
        reporter = open (log_dir+"worker_"+configs['timestamp']+".log", 'a')
        reporter.write ("\n=======================================\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": loaded configs from "+configs['output_dir']+ "\nnumber of plots ".rjust(16,' ')+str(len(configs['AXES']))+"\n=======================================\n")
        reporter.flush()
        reporter.close()
    return configs
#--------------------------------------------------------------------------------------
def zlim_and_zdata (dir_pair): 
    #print ("entering zlim_and_zdata: "+str(dir_pair))
    # dir_pair = [ [file_no, total_rows, total_cols, pos, net_name, dir_path, title, processing_bit], [..]
    if len(dir_pair) > 0:
        index, DICT, ALL_PTs   = 0, {}, []
        # dir  = (net_name, dir_path, title)
        for dir in dir_pair:            
            DICT[index] = {}
            for root, dirs, files in os.walk(dir[5]):
                for csv in files: #Vinayagam_RAW_INSTANCES_p075.0_t075.0_V4EB_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m51s20.csv
                    if csv.split('.')[-1] == 'csv':
                        p = float(str(''.join([d for d in csv.split('_')[-8] if d.isdigit() or d=='.'])))
                        t = float(str(''.join([d for d in csv.split('_')[-7] if d.isdigit() or d=='.'])))               
                        DICT[index][(p,t)] = ["", os.path.join(root, csv), ""] # friendly format for util.max_lines()
            index += 1
        assert len(dir_pair) == len(DICT.keys())
        #-------------------------------
        ALL_PTs = sorted(DICT[0].keys())
        #-------------------------------
        for i in range (1,len(dir_pair),1):
            assert ALL_PTs == sorted(DICT[i].keys())   
        zlim  = 0
        for p,t in ALL_PTs: 
            print ("current p,t: "+str(p)+","+str(t))
            current_PT = []
            for i in range(len(dir_pair)):
                current_PT.append(DICT[i][(p,t)])
            #---------------------------------------
            max_lines = util.max_lines(current_PT)
            #---------------------------------------            
            index = 0
            for _ , csv, _ in current_PT:
                instances = open (csv, 'r')
                step      = 0
                Bin       = []
                while step < max_lines:
                    next(instances) #skip G
                    Bs = [int(b) for b in next(instances).split()]
                    next(instances) # skip D
                    Xs = [int(x) for x in next(instances).split()]
                    next(instances) # skip 
                    #---------------------------------------------------------------------------
                    Bin.append(sum( set([b[0] for b in zip(Bs, Xs)  if b[1]==1]))) # those inside the knapsack
                    #---------------------------------------------------------------------------
                    step += 5
                #------------------------------------
                if len(Bin) > 0:
                    zlim = max(zlim, np.average(Bin))
                    DICT[index][(p,t)] = np.average(Bin)
                else:
                    DICT[index][(p,t)] = 0
                #------------------------------------
                index += 1
                instances.close()
        updated_dir_pair=[]
        for i in range(len(dir_pair)):
            tmp = [e for e in dir_pair[i]] # file_no, rows, cols, pos, prefix, dir_path, title, processing_bit
            tmp.append(zlim)
            tmp.append(DICT[i])
            updated_dir_pair.append(tmp)            
        return updated_dir_pair #file_no, total_rows, total_cols, pos, net_name, dir_path, title, processing_bit, zlim, {(p,t):Bin}   
    else:
        return []
#--------------------------------------------------------------------------------------
def work(arguments, rank):
    
    configs    = setup (arguments, rank)
    AXES       = configs['AXES']
    
    if len(AXES) > 0:       
        for  pair in AXES:
            #--------------------------------------------------------------
            updated_pair  =  zlim_and_zdata (pair) # [[network_name, csv_dir_path, plot_title, zlim, {(p,t):Bin}, [...]],
            #--------------------------------------------------------------
            for plot in updated_pair: 
                # file_no, rows, cols, pos, prefix, dir_path, title, processing_bit, zlim, {(p,t):Bin}
                file_no, rows, cols, pos, prefix, dir_path, title, processing_bit, zlim, Bin_dict = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5], plot[6], plot[7], plot[8], plot[9]
                
                if processing_bit == 0:
                    print ("\t\t\t\tworker "+str(rank)+"processing_bit=0; not processing file_no "+str(file_no))
                    continue
                current_file = configs['DUMP_DIR'] + "worker_"+str(rank).rjust(4,'0')+ "_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(rows).rjust(4,'0')+ "_cols_"+str(cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')
                if os.path.isfile(current_file+'.done'):
                    continue
                if rank == 1:
                    reporter = open (configs['logs_dir']+"worker_"+configs['timestamp']+".log", 'a')
                    reporter.write("\n\t\t\t\tworker #"+str(rank)+" working on file no. "+str(file_no))
                    reporter.flush()
                    reporter.close()
            
                with  open(current_file,'wb') as f:
                    pickle.dump([file_no, rows, cols, pos, prefix, dir_path, title, processing_bit, zlim, Bin_dict], f)
                try:
                    os.rename (current_file, current_file+'.done') #master will use 'done' as signal this worker is done writing to this file
                except:
                    reporter = open (configs['logs_dir']+"worker_"+configs['timestamp']+".log", 'a')
                    reporter.write ("\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": WARNING, unable to rename "+current_file+'.done .. master will wait forever')
                    reporter.flush()
                    reporter.close()
                    pass
        
        print ("\n\t\t\t\tworker #"+str(rank) +" I'm done! Good night!")
        reporter = open (configs['logs_dir']+"worker_"+configs['timestamp']+".log", 'a')
        reporter.write("\n\t\t\t\tworker #"+str(rank) +" I'm done! Good night!")
        reporter.flush()
        reporter.close()
    else:
        reporter = open (configs['logs_dir']+"worker_"+configs['timestamp']+".log", 'a')
        reporter.write ("\n\t\t\t\tworker #"+str(rank)+": I got nothing to do. I received an empty AXES (there is probably more workers than plots). Goodbye!")
        reporter.flush()
        reporter.close()
        print ("\n\t\t\t\tworker #"+str(rank)+": I got nothing to do. I received an empty AXES (there is probably more workers than plots). Goodbye!")
