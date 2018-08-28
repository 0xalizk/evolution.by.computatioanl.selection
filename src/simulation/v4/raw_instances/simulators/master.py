import sys, os, math, numpy as np, time, csv, json, shutil
from networkx.readwrite import json_graph
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, init
######################################
myprint = util.mylog
######################################

#--------------------------------------------------------------------------------------------------
def supervise (arguments, num_workers):
  
    M, configs   = init.initialize_master (arguments, num_workers)    
    
    log_dir = configs['output_directory']+"logs_raw_instances" 
    if not os.path.isdir (log_dir):
        os.makedirs(log_dir)
    with open (os.path.join(configs['output_directory'], "M"),'w') as f:
        json.dump(json_graph.node_link_data(M), f)
        f.close()
    if os.path.isdir(configs['output_directory']+ "configs_raw_instances"): #always start with a clean configs
        shutil.rmtree(configs['output_directory']+ "configs_raw_instances")
    os.makedirs(configs['output_directory']+ "configs_raw_instances")
    
     

    for rank in range(1, num_workers+1):
        with open (os.path.join(configs['output_directory'], "configs_raw_instances/configs_"+str(rank).rjust(4,'0')),'w') as f:
            json.dump(configs, f)
            f.close()
    if not os.path.isdir(configs['output_directory']+ "logs_raw_instances"):
        os.makedirs(configs['output_directory']+ "logs_raw_instances")
    if not os.path.isdir(configs['datapoints_dir']):
        os.makedirs(configs['datapoints_dir'])
    configs['master_log'] = configs['output_directory']+"logs_raw_instances/master_"+configs['timestamp']+".log"
    reporter = configs['master_log']
    myprint(reporter,"\n====================================\nmaster says: supervising\n====================================\n")
    return watch (M, configs)
#--------------------------------------------------------------------------------------------------
def watch (M, configs):
    t0 = time.time()    
    reporter = configs['master_log']  
    if len (configs['PT_pairs_dict'].keys()) == 0:
        myprint(reporter,"\n\tmaster says: configs['PT_pairs_dict'] is empty, Im exiting, goodnight")
    else:
        myprint(reporter,"\n\tmaster says: watching "+str(len(configs['PT_pairs_dict'].keys())) +" PT pairs")     
        total_dirs    = len(configs['PT_pairs_dict'].keys())
        files_per_dir = configs['num_workers']   
        pending_PTs   = []
        for key in sorted(configs['PT_pairs_dict'].keys()):
            pending_PTs.append ((configs['PT_pairs_dict'][key][0], configs['PT_pairs_dict'][key][1]))
        
        done          = False
        while not done:
            time.sleep (60)
            for root, dirs, files in os.walk(configs['DUMP_DIR']):              
                dirs.sort()
                for d in dirs:
                    if len(pending_PTs)==0:
                        done=True
                        break
                    #assuming dump dirs are of the form 0005_p_15.0_t_20.0
                    next_p, next_t = float(d.split('_')[2]), float(d.split('_')[4])
                    if next_p == pending_PTs[0][0] and next_t == pending_PTs[0][1]:
                        for r, ds, fs in os.walk (os.path.join(root,d)):
                            confirmation = False
                            if (len(fs) == files_per_dir): # skip directories recently modified (1 minutes), workers may still be writing to them
                                confirmation = harvest (os.path.join(root,d), configs)
                                if confirmation:
                                    try:
                                        shutil.rmtree(os.path.join(root,d)) 
                                    except:
                                        myprint(reporter,"\n\tmaster says: WARNING, couldn't delete this dir "+str(d))
                                        pass   
                                    if len(pending_PTs) <= 1:
                                        pending_PTs =[]
                                        done=True
                                        break
                                    else:
                                        pending_PTs=pending_PTs[1:]
                if len(pending_PTs) == 0:
                     done = True
                     break
        #------------------------------------
        write_checkpoint (configs, "done")
        #------------------------------------
        t1 = time.time()
        myprint(reporter,"\n\tmaster says: harvested "+str(total_dirs)+" directories in "+str(int(t1-t0))+" seconds")
        return True
#--------------------------------------------------------------------------------------------------    
def harvest(d, configs):
    reporter = configs['master_log']
    t0 = time.time()
    pt_pairs=[]              
    for root, dirs, files in os.walk(d):
        #----------------------------------------------------------------------
        RAW_files    = sorted([f for f in files if 'RAW.done' in f.split('_')])
        #----------------------------------------------------------------------
        
        if len(RAW_files) != configs['num_workers'] :
            return False
        for raw_file in RAW_files:
            pt_pairs.append ((raw_file.split('_')[3], raw_file.split('_')[5]))
        assert all(x == pt_pairs[0] for x in pt_pairs)
        
        datafile = open (util.slash(configs['datapoints_dir'])+configs['network_name']+'_RAW_INSTANCES_p'+str(pt_pairs[0][0]).rjust(5,'0')+'_t'+str(pt_pairs[0][1]).rjust(5,'0')+'_'+configs['stamp'].upper()+'_'+'alpha'+str(configs['alpha'])+'.'+configs['timestamp']+".csv",'w')
        
        # concatenate all the files into one file   
        first_line = True
        for raw_file in RAW_files:   
            f = open (os.path.join(d, raw_file),'r').readlines()
            if len(f)>=5:
                if len(f) % 5 !=0 : # RAW files must contain finished 
                    f = f[0:int(len(f)/5)*5]
                    myprint(reporter,"\n\t\tmaster says: WARNING, file "+raw_file+" seems incomplete, I chopped off "+str(len(f) % 5)+" trailing lines, see harvest() at master.py") 
                if first_line==True:
                    first_line=False
                else:
                    datafile.write("\n")
                datafile.write('\n'.join([line.strip() for line in f]))              
    datafile.flush()   
    datafile.close()    
    progress = str(pt_pairs[0][0])+' '+str(pt_pairs[0][1])
    #----------------------------------------
    write_checkpoint (configs, progress) 
    #----------------------------------------
    t1 = time.time()
    myprint(reporter,"\n\t\tmaster says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": I've harvested "+d+" in "+str(int(t1-t0))+" seconds")    
    return True
#--------------------------------------------------------------------------------------------------
def write_checkpoint (configs, latest):
    progress = open (configs['progress_file'], 'w')
    progress.write(latest)
    progress.flush()
    progress.close()
#--------------------------------------------------------------------------------------------------
