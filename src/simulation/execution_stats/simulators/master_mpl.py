from multiprocessing import Process
import sys, os, math, numpy as np, time, csv, json, shutil 
from networkx.readwrite import json_graph
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, worker, init_execstats as init, master_mpi
mywrite = util.mywrite
myprint = util.myprint
#--------------------------------------------------------------------------------------------------
def supervise (arguments, num_workers):
  
    M, configs   = init.initialize_master (arguments, num_workers)    

    with open (os.path.join(configs['output_directory'], "M"),'w') as f:
        json.dump(json_graph.node_link_data(M), f)
        f.close()
    if os.path.isdir(configs['configs_dir']): #always start with a clean configs
        shutil.rmtree(configs['configs_dir'])
    os.makedirs(configs['configs_dir'])
        
    spawn =[]
    for rank in range(1, num_workers+1):
        with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'w') as f:
            json.dump(configs, f)
            f.close()
            spawn.append(Process(target=worker.work, args=(arguments, rank,)))
    for process in spawn:
        process.start()
        time.sleep(1)
        
    
    if not os.path.isdir(configs['log_dir']):
        os.makedirs(configs['log_dir'])
    if not os.path.isdir(configs['datapoints_dir']):
        os.makedirs(configs['datapoints_dir'])
    configs['master_log'] = configs['log_dir']+"master_"+configs['timestamp']+".log"
    mywrite (configs['master_log'],"\n====================================\nmaster says: supervising\n====================================\n")    
    master_mpi.watch (M, configs)
    return
#--------------------------------------------------------------------------------------------------
