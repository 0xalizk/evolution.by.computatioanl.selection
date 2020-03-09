######################################
import sys,os
sys.path.insert(0, os.getenv('lib'))
import time, math, json, numpy as np,  init_plotting as init, util_plotting as util
######################################

#--------------------------------------------------------------------------------------
def max_lines (pair):

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
#--------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------
def work(arguments, rank):
    print ("\t\t\t\tworker #"+str(rank)+" I'm working,\t",end='')
    configs       = init.load_simulation_configs (arguments, rank) #at this point, configs doesnt yet contain configs ['worker_load'] and configs ['num_workers'], obtained after json-loading configs json-dumped by master (below)
    M, configs_update, loaded =  None, None, False

    log_dir = configs['logs_dir']
    
    while not loaded: #wait for master.py to dump  updated configs and get it
        try:
            if os.path.isdir(configs['output_dir']) and  os.path.isfile(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0')):
                if (time.time()-os.path.getmtime(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0'))) > 5:  #give master a chance to finish writing M/configs
                    f = open (os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')),'r')
                    configs_update = json.load(f)
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
    
    
    AXES       = configs['AXES']
    slices      = {}
    
    if len(AXES) > 0:
        for  plot in AXES:
            
            configs['num_lines']   = len(open(plot[5].strip(), 'r').readlines())
        
                   
            slices      = {}
            for key in configs['slices'].keys():
                slices[key] = configs['slices'][key]
        
            file_no, rows, cols, pos, prefix, file_path, title = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5], plot[6]+", "+util.pf(configs['num_lines']/5)+"]"
            
            current_file = configs['DUMP_DIR'] + "worker_"+str(rank).rjust(4,'0')+ "_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(rows).rjust(4,'0')+ "_cols_"+str(cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')
            if os.path.isfile(current_file+'.done'):
                continue
            if rank == 1:
                reporter = open (log_dir+"worker_"+configs['timestamp']+".log", 'a')
                reporter.write("\n\t\t\t\tworker #"+str(rank)+" working on file no. "+str(file_no))
                reporter.flush()
                reporter.close()
            
            #-------------------------------------
            df = open (file_path, 'r')
            #-------------------------------------
                        
            lines_so_far = 0
            
            while lines_so_far < configs['num_lines']:                
                next(df)                                     # skip over objects
                Bs     = [int(s) for s in next(df).split()]
                Ds     = [int(s) for s in next(df).split()]
                next(df)                                     #skip over Xs (solution vector)
                next(df)                                     #skip over coresize/exec_time
                lines_so_far += 5         
                assert len(Bs) == len(Ds)
                
                instance_size = 0
                for key in slices['segments'].keys():
                    slices['segments'][key]['count']=0
                if len(Bs)>0:
                    for b,d in zip (Bs, Ds):
                        instance_size += 1
                        #-------------------------------------
                        the_right_key = assign_range(slices, b, d)
                        slices['segments'][the_right_key]['count'] += 1
                        #-------------------------------------
                    counted=0
                    for key in slices['segments'].keys():
                        slices['segments'][key]['fractions'].append(float(slices['segments'][key]['count'])/instance_size)
                        counted += slices['segments'][key]['count']
                    
                    assert instance_size == len(Bs) == len(Ds)  == counted      

            
            with  open(current_file,'w') as f:
                #print ("\nworker #"+str(rank)+"\t"+"file_no "+str(file_no) +" total_rows "+str(rows) +" total_cols "+str(cols) +" pos "+str(pos)+" > "+current_file.split('/')[-1])
                json.dump([file_no, rows, cols, pos, prefix, file_path, title, slices], f)
            try:
                os.rename (current_file, current_file+'.done') #master will use 'done' as signal this worker is done writing to this file
            except:
                reporter.write ("\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": WARNING, unable to rename "+current_file+'.done .. master will wait forever')
                pass
        
        print ("\n\t\t\t\tworker #"+str(rank) +" I'm done! Good night!")
        reporter = open (log_dir+"worker_"+configs['timestamp']+".log", 'a')
        reporter.write("\n\t\t\t\tworker #"+str(rank) +" I'm done! Good night!")
        reporter.flush()
        reporter.close()
    else:
        reporter = open (log_dir+"worker_"+configs['timestamp']+".log", 'a')
        reporter.write ("\n\t\t\t\tworker #"+str(rank)+": I got nothing to do. I received an empty AXES (there is probably more workers than plots). Goodbye!")
        reporter.flush()
        reporter.close()
        print ("\n\t\t\t\tworker #"+str(rank)+": I got nothing to do. I received an empty AXES (there is probably more workers than plots). Goodbye!")




            
            
            
