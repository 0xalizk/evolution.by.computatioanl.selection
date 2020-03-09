from multiprocessing import Process
import sys, os, math, numpy as np, time, csv, json, shutil 
from networkx.readwrite import json_graph
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, worker, init, master
###########################################################
myprint = util.mylog
###########################################################

def supervise (arguments, num_workers):
  
    M, configs   = init.initialize_master (arguments, num_workers)    

    with open (os.path.join(configs['output_directory'], "M"),'w') as f:
        json.dump(json_graph.node_link_data(M), f)
        f.close()
    if os.path.isdir(configs['output_directory']+ "configs_raw_instances"): #always start with a clean configs
        shutil.rmtree(configs['output_directory']+ "configs_raw_instances")
    os.makedirs(configs['output_directory']+ "configs_raw_instances")
        
    spawn =[]
    for rank in range(1, num_workers+1):
        with open (os.path.join(configs['output_directory'], "configs_raw_instances/configs_"+str(rank).rjust(4,'0')),'w') as f:
            json.dump(configs, f)
            f.close()
            spawn.append(Process(target=worker.work, args=(arguments, rank,)))
    for process in spawn:
        process.start()
        time.sleep(1)
        
    
    if not os.path.isdir(configs['output_directory']+ "logs_raw_instances"):
        os.makedirs(configs['output_directory']+ "logs_raw_instances")
    if not os.path.isdir(configs['datapoints_dir']):
        os.makedirs(configs['datapoints_dir'])
    configs['master_log'] = configs['output_directory']+"logs_raw_instances/master_"+configs['timestamp']+".log"
    reporter = open (configs['master_log'], 'a')
    reporter.write ("\n====================================\nmaster says: supervising\n====================================\n")
    print          ("\n====================================\nmaster says: supervising\n====================================\n")
    reporter.flush()
    reporter.close()    
    return master.watch (M, configs)
