import sys,os,copy
from collections import Counter
sys.path.insert(0, os.getenv('lib'))
import time, math, pickle, numpy as np,  init_plotting as init, util_plotting as util
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
        file_path = p[5]
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
    '''
    num_lines=[]
    for prefix, file_path, title in pair:
        num_lines.append(0)
        df = open (file_path, 'r')
        while True:
            try: # insist on reading chunks of 5 lines 
                next(df)                
                next(df)
                next(df)
                next(df) 
                next(df) 
            except:
                break
            num_lines[-1] += 5       
    if len(num_lines)==0:
        num_lines=[0]
    return min(num_lines)
    '''
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
def cruncher1 (Gs,Bs,Ds,Xs,slices): # relative COUNT of genes in each slice regardless if gene is IN or OUT knapsack
    for key in slices['segments'].keys():
        slices['segments'][key]['count']=0
    instance_size = 0
    for b,d in zip (Bs, Ds):
        instance_size += 1
        the_right_key = assign_range(slices, b, d)
        slices['segments'][the_right_key]['count'] += 1   # <<<<<<<<<<<<<<<
    counted=0
    for key in slices['segments'].keys():
        slices['segments'][key]['fractions'].append(float(slices['segments'][key]['count'])/instance_size)  # <<<<<<<<<<<<<<<
        counted += slices['segments'][key]['count']
    assert instance_size == len(Bs) == len(Ds)  == counted
#######################################################################################
def cruncher2 (Gs,Bs,Ds,Xs,slices): # relative tot. benefit of genes in each slice regardless if gene is IN or OUT knapsack (obviously genes with b=0 are OUT)
    for key in slices['segments'].keys():
        slices['segments'][key]['count']=0
    instance_size = 0
    for b,d in zip (Bs, Ds):
        instance_size += 1
        the_right_key = assign_range(slices, b, d)
        slices['segments'][the_right_key]['count'] += b   # <<<<<<<<<<<<<<<
    for key in slices['segments'].keys():
        slices['segments'][key]['fractions'].append(float(slices['segments'][key]['count'])/sum(Bs))  # <<<<<<<<<<<<<<<
#######################################################################################                            
def cruncher3 (Gs,Bs,Ds,Xs,slices): # only genes IN knapsack 
    for key in slices['segments'].keys():
        slices['segments'][key]['count']=0
    instance_size = 0
    for b,d,x in zip (Bs, Ds, Xs):
        if x==1:                                           # <<<<<<<<<<<<<<<
            instance_size += 1        
            the_right_key = assign_range(slices, b, d)
            slices['segments'][the_right_key]['count'] += b # <<<<<<<<<<<<<<<
    for key in slices['segments'].keys():
        slices['segments'][key]['fractions'].append(float(slices['segments'][key]['count'])/sum(Bs)) # <<<<<<<<<<<<<<<
#######################################################################################
def cruncher4 (Gs,Bs,Ds,Xs,slices): # relative COUNT of genes in each slice regardless if gene is IN or OUT knapsack
    instance_size = len(Gs)
    tmp_count     = {}
    for slice_id in slices['segments'].keys():
        tmp_count[slice_id]=[]
    
    for g,b,d in zip (Gs, Bs, Ds):
        the_right_slice_id = assign_range(slices, b, d)
        degree          = sum([int(deg) for deg in g.split('$')[1:]])
        tmp_count[the_right_slice_id].append(degree)       # <<<<<<<<<<<<<<<
    #print (str(tmp_count))    
    tmp_freq = {}
    for slice_id in tmp_count.keys(): # 1, 2, ... 
        freq = Counter (tmp_count[slice_id]) # freq is a dictionary
        tmp_freq[slice_id]={}
        for degree in freq.keys():
            tmp_freq[slice_id][degree]=freq[degree]

    #print ('\n\n'+str(tmp_freq))    
    check = 0
    for slice_id in tmp_freq.keys():
        #--------------------------------------------------
        normalizer = float(sum(tmp_freq[slice_id].values())) # normalizer = the total number of genes in a given b:d slice
        check +=normalizer
        #--------------------------------------------------
        for degree in tmp_freq[slice_id].keys():
            tmp_freq[slice_id][degree] =  tmp_freq[slice_id][degree] / normalizer
    assert check == instance_size
    #print ('\n\n'+str(tmp_freq))
    for slice_id in tmp_freq.keys():
        for degree in tmp_freq[slice_id].keys():
            if degree not in slices['segments'][slice_id]['degree_freq'].keys():
                slices['segments'][slice_id]['degree_freq'][degree] = {'avg_so_far':tmp_freq[slice_id][degree],'count_so_far':1}
            else:
                count_so_far = slices['segments'][slice_id]['degree_freq'][degree]['count_so_far']
                avg_so_far   = slices['segments'][slice_id]['degree_freq'][degree]['avg_so_far']
                new_count    = count_so_far + 1
                new_avg      = ((avg_so_far*count_so_far) + tmp_freq[slice_id][degree]) / new_count
                slices['segments'][slice_id]['degree_freq'][degree]['avg_so_far']   = new_avg
                slices['segments'][slice_id]['degree_freq'][degree]['count_so_far'] = new_count 
#######################################################################################
def process_instances (slices, file_path, num_lines, configs, cruncher):
    for key in slices['segments'].keys(): #assert slices 
        if configs['cruncher']=='cruncher4':
            assert slices['segments'][key]['degree_freq'] == {}
        else:
            assert slices['segments'][key]['count']     == 0
            assert slices['segments'][key]['fractions'] == []
    #-------------------------------------
    df = open (file_path, 'r')
    #-------------------------------------   
    lines_so_far = 0
    while lines_so_far < num_lines:                
        Gs     = [g for g in next(df).strip().split()]
        Bs     = [int(s) for s in next(df).strip().split()]
        Ds     = [int(s) for s in next(df).strip().split()]
        Xs     = [int(x) for x in next(df).strip().split()]  #skip over Xs (solution vector)
        next(df)                                     #skip over coresize/exec_time
        lines_so_far += 5         
        assert len(Bs) == len(Ds)

        if len(Bs)>0:
            cruncher(Gs,Bs,Ds,Xs,slices)    
    return slices
####################################################################################### 
def dump(file_no, rows, cols, pos, prefix, file_path, title, filled_slices, configs, rank):
    current_file = configs['DUMP_DIR'] + "worker_"+str(rank).rjust(4,'0')+ "_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(rows).rjust(4,'0')+ "_cols_"+str(cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')
    with  open(current_file,'wb') as f:
        pickle.dump([file_no, rows, cols, pos, prefix, file_path, title, filled_slices], f)
        f.close()
    try:
        os.rename (current_file, current_file+'.done') #master will use 'done' as signal this worker is done writing to this file
    except:
        mywrite (log, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": WARNING, unable to rename "+current_file+'.done .. master will wait forever')
        pass
#######################################################################################
def work(arguments, rank):
    
    configs  = setup(arguments, rank)  
    cruncher = None
    if 'cruncher' in configs.keys():
        if configs['cruncher'] in globals().keys():
            cruncher = globals()[configs['cruncher']]
        else:
            cruncher = cruncher1 # default    
    else:
        cruncher = cruncher1 # default
            
    log      = configs['worker_log']
    WORK_LOAD       = configs['WORK_LOAD'] # each element in workload is a collection of pairs
    
    if len(WORK_LOAD) > 0:
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+" I'm working .. "+cruncher.__name__)
        t0=time.time()
        
        for pair in WORK_LOAD: 
        
            num_lines = max_lines(pair, configs)
            
            for plot in pair: 
                
                file_no, rows, cols, pos, prefix, file_path, title, processing_bit = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5], plot[6]+", "+util.pf(float(num_lines)/5.0)+" instances]", plot[7]
                
                if processing_bit == 1:
                    #####################################################################
                    slices      = copy.deepcopy(configs['slices']) 
                    mywrite(log, "\n\t\t\t\tworker #"+str(rank)+" processing: "+str(file_path.split('/')[-1]))
                    filled_slices = process_instances(slices, file_path, num_lines, configs, cruncher)              
                    dump(file_no, rows, cols, pos, prefix, file_path, title.replace(']',','+cruncher.__name__+']'), filled_slices, configs, rank)
                    del filled_slices, slices
                    #####################################################################
                else:
                    mywrite(log,"\n\t\t\t\tworker "+str(rank)+"    skipping: "+file_path.split('/')[-1])
        t1=time.time()
        mywrite(log, "\n\t\t\t\tworker #"+str(rank) +" I'm done ("+str(int(t1-t0))+"s)! Good night!")
    else:
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": I got nothing to do. I received an empty WORK_LOAD (there is probably more workers than plots). Goodbye!")
    '''
    WORK_LOAD = [
                    [
                        [1, 4, 10, 1, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t000.1_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-12-2016-h14m26s11.csv', 'Vinayagam\n[$p=100.0, t=000.1$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 2, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t001.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=001.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 3, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t005.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=005.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 4, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t010.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=010.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 5, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t015.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=015.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 6, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t020.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=020.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 7, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t025.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=025.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 8, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t050.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=050.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 9, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t075.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=075.0$, V4NU, MI, 4X, BOTH, REVERSE', 1], 
                        [1, 4, 10, 10, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t100.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv', 'Vinayagam\n[$p=100.0, t=100.0$, V4NU, MI, 4X, BOTH, REVERSE', 1]
                    ], 
                    [
                        [1, 4, 10, 11, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t000.1_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m16s15.csv', 'Vinayagam\n[$p=100.0, t=000.1$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 12, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t001.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m16s15.csv', 'Vinayagam\n[$p=100.0, t=001.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 13, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t005.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m16s15.csv', 'Vinayagam\n[$p=100.0, t=005.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 14, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t010.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m16s15.csv', 'Vinayagam\n[$p=100.0, t=010.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 15, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t015.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m16s15.csv', 'Vinayagam\n[$p=100.0, t=015.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 16, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t020.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m55s25.csv', 'Vinayagam\n[$p=100.0, t=020.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 17, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t025.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m55s25.csv', 'Vinayagam\n[$p=100.0, t=025.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 18, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t050.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m55s25.csv', 'Vinayagam\n[$p=100.0, t=050.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 19, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t075.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m55s25.csv', 'Vinayagam\n[$p=100.0, t=075.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1], 
                        [1, 4, 10, 20, 'Vinayagam', '/mnt/malsha17/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/Vinayagam_RAW_INSTANCES_p100.0_t100.0_V4NU_MINKNAP_4X_BOTH_SCRAMBLE_alpha0.2.October-06-2016-h08m55s25.csv', 'Vinayagam\n[$p=100.0, t=100.0$, V4NU, MI, 4X, BOTH, SCRAMBLE', 1]
                    ]
               ]  
    '''    