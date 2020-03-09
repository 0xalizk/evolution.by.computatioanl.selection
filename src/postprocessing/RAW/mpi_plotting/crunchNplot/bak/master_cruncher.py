import sys,os
from collections import Counter
sys.path.insert(0, os.getenv('lib'))
import time, pickle, init_plotting as init, util_plotting as util, crunchers
#######################################################################################
mywrite = util.mywrite
#######################################################################################
def max_lines (pair, configs):
    num_lines = []      
    limit = 0
    try:
        limit = int(configs['max_lines'])
        if limit<=0:
            limit = -1
    except:
        limit = -1 # read the whole file
    for p in pair:
        if not os.path.isfile(p['file_path']): # in case we're processing directories (bar3d)
            return 0
    for p in pair:
        file_path = p['file_path']
        df = open (file_path, 'r')
        counter = 0       
        try:
            while True:
                next(df)
                next(df)
                next(df)       
                next(df)
                next(df)
                counter +=5
                if limit>0 and counter>limit:
                    num_lines.append(counter)
                    break              
        except:
            num_lines.append(counter)
            counter=0
    if len(num_lines)==0:
        num_lines=0
    else:
        num_lines=min(num_lines)  
    try:
        if int(configs['max_lines'])>0:
            num_lines = min(int(configs['max_lines']), num_lines)
    except:
        pass
    return num_lines
#######################################################################################
def print_freqs(fraction_freq, title, log):
    mywrite(log, '\n'+'='*90+'\n'+' '*90)
    mywrite(log, '\n####### '+title.replace('\n',' ').rjust(45,' ')+' #######')
    mywrite(log, '\n'+' '*90)
    mywrite(log, '\n(b,d)'.ljust(15,' ')+'frequency (%), i.e. average appearance of such b/d per each instance')
    mywrite(log, '\n'+'='*90)
    for e in sorted(fraction_freq.items(),key=lambda x: x[1]['avg_frac_sofar'],reverse=True):
        mywrite(log, '\n'+str(e[0]).ljust(15,' ')+str(util.f3(e[1]['avg_frac_sofar']*100)).ljust(8,' ')+' %')
    mywrite(log, '\n'+'='*90)
#######################################################################################
def calculate_Axis_limits (pair, configs):
    max_B, max_D, num_lines = 0, 0, []      
    limit = 0
    try:
        limit = int(configs['max_lines'])
        if limit<=0:
            limit = -1
    except:
        limit = -1 # read the whole file       
    for p in pair:
        file_path = p['file_path']
        df = open (file_path, 'r')
        counter = 0       
        try:
            while True:
                next(df)
                max_B    = max (max_B, max([int(b) for b in next(df).split()]))
                max_D    = max (max_D, max([int(d) for d in next(df).split()]))        
                next(df)
                next(df)
                counter +=5
                if limit>0 and counter>limit:
                    num_lines.append(counter)
                    break              
        except:
            num_lines.append(counter)
            counter=0
    if len(num_lines)==0:
        num_lines=0
    else:
        num_lines=min(num_lines)  
    try:
        if int(configs['max_lines'])>0:
            num_lines = min(int(configs['max_lines']), num_lines)
    except:
        pass
    try:
        configs['xlim'] = max(int(configs['xlim']), max_D)
    except:
        configs['xlim'] = max_D
        pass
    try:
        configs['ylim'] = max(int(configs['ylim']), max_B)
    except:
        configs['ylim'] = max_B
        pass
    return [configs['xlim'], configs['ylim'], num_lines]
#######################################################################################
def assign_range(slices, b, d):
    right_key, b2d_ratio, d2b_ratio = 0,0,0
    if b==0 and d==0:
        right_key =   [key for key in slices['segments'].keys() if slices['segments'][key]['range'][0]==0 and  slices['segments'][key]['range'][1]==0]

    elif b>=d: 
        b2d_ratio, d2b_ratio = round((float(b)/float(b+d))*100, 12), round((float(d)/float(b+d))*100,12)
        right_key = [key for key in slices['segments'].keys() if (b2d_ratio-slices['segments'][key]['range'][0]) >=0 and (b2d_ratio-slices['segments'][key]['range'][0]) <slices['interval']  and (slices['segments'][key]['range'][1]-d2b_ratio)>=0 and (slices['segments'][key]['range'][1]-d2b_ratio)<slices['interval'] ]
    
    else:
        b2d_ratio, d2b_ratio = (float(b)/float(b+d))*100, (float(d)/float(b+d))*100
        right_key = [key for key in slices['segments'].keys() if (slices['segments'][key]['range'][0]-b2d_ratio) >=0 and (slices['segments'][key]['range'][0]-b2d_ratio) <slices['interval']  and (d2b_ratio-slices['segments'][key]['range'][1])>=0 and (d2b_ratio-slices['segments'][key]['range'][1])<slices['interval'] ]
    
    
    assert len(right_key)==1
    return right_key[0]
#######################################################################################
def setup(arguments, rank):
    configs       = init.load_simulation_configs (arguments, rank) #at this point, configs doesnt yet contain configs ['worker_load'] and configs ['num_workers'], obtained after pickle-loading configs pickle-dumped by master (below)
    M, configs_update, loaded =  None, None, False

    log_dir = configs['logs_dir']
    
    while not loaded: #wait for master.py to dump  updated configs and get it
        try:
            if os.path.isdir(configs['output_dir']) and  os.path.isfile(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0')):
                if (time.time()-os.path.getmtime(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0'))) > 5:  #give master a chance to finish writing M/configs
                    f = open (os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')),'rb')
                    configs_update = pickle.load(f)
                    f.close()
                    loaded = True
                else:
                    time.sleep(2)
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
    log            =  configs['logs_dir']+"worker_"+configs['timestamp']+".log"
    configs['worker_log'] = log    

    try:
        os.rename(os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')), os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')+"_loaded_"+configs['timestamp']))
    except:
        with open (log_dir+"worker_"+str(rank)+"_ERROR_"+configs['timestamp']+".log", 'a') as reporter:
            reporter = open (log_dir+"worker_"+configs['timestamp']+".log", 'a')
            reporter.write ("\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": FATAL, unable to rename "+os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0'))+"\nExiting..")
            sys.exit(1)
    reporter = None
    if rank == 1: # have worker 1 report activity 
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+", loaded configs from .."+'/'.join(configs['output_dir'].split('/')[-3:])+ ", no. of plots (my WROK_LOAD (#pairs) ) ".rjust(16,' ')+str(len(configs['WORK_LOAD'])))
    return configs
####################################################################################### 
def dump(harvest):
    current_file = harvest['worker_configs']['DUMP_DIR'] + "worker_"+str(harvest['rank']).rjust(4,'0')+ "_figure_"+str(harvest['file_no']).rjust(4,'0')+ "_pos_"+str(harvest['pos']).rjust(4,'0')
    with  open(current_file,'wb') as f:
        pickle.dump(harvest, f)
        f.close()
    try:
        os.rename (current_file, current_file+'.done') #master will use 'done' as signal this worker is done writing to this file
    except:
        mywrite (log, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": WARNING, unable to rename "+current_file+'.done .. master will wait forever')
        pass
#######################################################################################
def crunch(arguments, rank):
    configs  = setup(arguments, rank)  

    processor = None
    if configs['cruncher'] in ['ETXcruncher1','ETXcruncher2', 'ETXcruncher3']:
        processor =  crunchers.ETX_processor
    elif configs['cruncher'] == 'scatter':
        processor =  crunchers.scatter_processor
    elif configs['cruncher'] in ['cruncher1', 'cruncher2', 'cruncher3', 'cruncher4']: 
        processor = crunchers.wheel_processor
    else:
        mywrite(configs['worker_log'], '\n\n\nFATAL: I dont know what to crunch, \nExiting .. \n\n')
        sys.exit(1)
    log           = configs['worker_log']
    WORK_LOAD     = configs['WORK_LOAD'] # each element in workload is a collection of pairs
    
    if len(WORK_LOAD) > 0:
        t0=time.time()
        for pair in WORK_LOAD: 
            ##############################
            processor(configs, pair, rank)
            ##############################           
        t1=time.time()
        mywrite(log, "\n\t\t\t\tworker #"+str(rank) +": I'm done ("+str(int(t1-t0))+"s)! Good night!")
    else:
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": I got nothing to do. I received an empty WORK_LOAD (there is probably more workers than plots). Goodbye!")
#######################################################################################   
            
