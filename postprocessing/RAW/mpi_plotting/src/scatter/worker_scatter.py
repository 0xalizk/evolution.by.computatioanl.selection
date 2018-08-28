import sys,os
sys.path.insert(0, os.getenv('lib'))
import time, math, json, numpy as np,  init_plotting as init, util_plotting as util
#######################################################################################
mywrite = util.mywrite # screen and log file
myprint = util.myprint # screen only
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
        file_path = p[5]
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
def setup(arguments, rank):
   
    configs       = init.load_simulation_configs (arguments, rank) #at this point, configs doesnt yet contain configs ['worker_load'] and configs ['num_workers'], obtained after json-loading configs json-dumped by master (below)
    M, configs_update, loaded =  None, None, False
  
    while not loaded: #wait for master.py to dump  updated configs and get it
        try:
            if os.path.isdir(configs['output_dir']) and  os.path.isfile(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0')):
                if (time.time()-os.path.getmtime(util.slash(configs['output_dir'])+ "configs/configs_"+str(rank).rjust(4,'0'))) > 5:  #give master a chance to finish writing M/configs
                    f = open (os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0')),'r')
                    configs_update = json.load(f)
                    f.close()
                    loaded = True
                else:
                    time.sleep(3)
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
        mywrite(log, "\nworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": FATAL, unable to rename "+os.path.join(configs['configs_dir']+"configs_"+str(rank).rjust(4,'0'))+"\nExiting..")
        sys.exit(1)
    if rank == 1: # have worker 1 report activity 
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+", loaded configs from .."+'/'.join(configs['output_dir'].split('/')[-3:])+ ", no. of plots (my AXES) ".rjust(16,' ')+str(len(configs['AXES'])))
    
    return configs
#######################################################################################        
def data_processor (file_path, num_lines, plot_title, rank, configs):
    mode, cbar_label = 'percentage' ,  "$Frequency \quad (\%)$" # defaults
    if configs['mode'].strip() == 'count':
        cbar_label = "$Frequency \quad (log_2)$"
        mode = 'count'            
    #-------------------------------------
    df = open (file_path, 'r')
    #-------------------------------------            
    lines_so_far, fraction_freq  = 0, {}
    while lines_so_far < num_lines:
        Bs_Ds         = {}
        next(df)      # skip over objects
        tmp_Bs        = [int(s) for s in next(df).split()]
        tmp_Ds        = [int(s) for s in next(df).split()]
        next(df)      #skip over Xs (solution vector)
        next(df)      #skip over coresize/exec_time
        lines_so_far += 5         
        assert len(tmp_Bs) == len(tmp_Ds)

        if len(tmp_Bs)>0:
            for obj in zip(tmp_Bs, tmp_Ds):
                if obj in Bs_Ds.keys():
                    Bs_Ds[obj] +=1
                else:
                    Bs_Ds[obj] = 1                  
            for obj in zip(tmp_Bs, tmp_Ds):
                if obj not in fraction_freq.keys(): 
                    fraction_freq[obj] = {'avg_frac_sofar':0.0,'count_sofar':0.0}
                fraction  =  float(Bs_Ds[obj])/len(tmp_Bs)
                fraction_freq[obj]['avg_frac_sofar']   = ((fraction_freq[obj]['avg_frac_sofar']*fraction_freq[obj]['count_sofar']) + fraction ) /  (fraction_freq[obj]['count_sofar'] + 1)
                fraction_freq[obj]['count_sofar']      = fraction_freq[obj]['count_sofar'] + 1             
    Bs, Ds, frequency = [],[],[]
    for obj in fraction_freq.keys():
        Bs.append(obj[0])
        Ds.append(obj[1])
        if mode == 'percentage':
            frequency.append(fraction_freq[obj]['avg_frac_sofar']*100) # convert it to %
        else:
            frequency.append(math.log (fraction_freq[obj]['count_sofar'], 2))
    #-------------------------------
    if rank == 1 and mode == 'percentage':
        print_freqs(fraction_freq, plot_title, configs['worker_log'])                 
    #-------------------------------

    return Bs, Ds, frequency, cbar_label
#######################################################################################
def dump (file_no, rows, cols, pos, prefix, file_path, title, xlim, ylim, Bs, Ds, frequency, cbar_label, configs, rank, log):
    current_file = configs['DUMP_DIR'] + "worker_"+str(rank).rjust(4,'0')+ "_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(rows).rjust(4,'0')+ "_cols_"+str(cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')
    with  open(current_file,'w') as f:
        json.dump([file_no, rows, cols, pos, prefix, file_path, title, xlim, ylim, Bs, Ds, frequency, cbar_label], f)
        f.close()
    try:
        os.rename (current_file, current_file+'.done') #master will use 'done' as signal this worker is done writing to this file
    except:
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+" says "+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+": WARNING, unable to rename "+current_file+'.done .. master will wait forever')
        pass
#######################################################################################
def Done(plot, configs, rank):
    file_no, rows, cols, pos, prefix, file_path, title, processing_bit = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5], plot[6], plot[7]
    if processing_bit == 0:
        mywrite(log,"\t\t\t\tworker "+str(rank)+" not processing: "+file_path)
        return False
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            f=f.split('_figure_')
            if len(f)>1:
                if f[1] == str(file_no).rjust(4,'0')+ "_rows_"+str(rows).rjust(4,'0')+ "_cols_"+str(cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')+'.done':
                    return True
    return False
#######################################################################################                   
def work(arguments, rank):
    
    configs  = setup(arguments, rank)
    log      = configs['worker_log']
    AXES     = configs['AXES']    
    if len(AXES) > 0:
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": I'm working")        
        t0 = time.time()
        for  pair in AXES:
            
            xlim, ylim, num_lines = calculate_Axis_limits (pair, configs)
            
            if rank == 1:
                mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": xlim "+str(xlim)+", ylim "+str(ylim)+', no. instances to read: '+util.pf(float(num_lines)/5.0))
                
            for plot in pair: 
                if not Done(plot, configs, rank):
                   
                                              
                    #####################################################################
                    file_no, rows, cols, pos, prefix, file_path, title, processing_bit = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5], plot[6]+", "+util.pf(num_lines/5)+" instances]", plot[7]
                    
                    Bs, Ds, frequency, cbar_label = data_processor (file_path, num_lines, title,  rank, configs)
                    
                    dump (file_no, rows, cols, pos, prefix, file_path, title, xlim, ylim, Bs, Ds, frequency, cbar_label, configs, rank, log)
                    
                    del Bs, Ds, frequency, cbar_label
                    mywrite(log,"\n\t\t\t\tworker #"+str(rank)+" finished file no. "+str(file_no)+' plot no. '+str(pos)+' ('+title.replace('\n','').replace('$','')+')')   
                    #####################################################################
        t1 =time.time()
        mywrite(log,"\n\t\t\t\tworker #"+str(rank) +" I'm done ("+str(int(t1-t0))+"s)! Good night!")
    else:
        mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": I got nothing to do. I received an empty AXES (there is probably more workers than plots). Goodbye!")
         
