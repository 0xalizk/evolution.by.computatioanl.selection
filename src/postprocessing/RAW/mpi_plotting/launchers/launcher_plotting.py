import os, sys, subprocess, time, socket, math
sys.path.insert(0, os.getenv('lib')) 
import init_plotting as init, util_plotting as util
#--------------------------------------------------------------------------------------------
def needed_workers(configs):
    DONEs           = []
    file_no         = 0      #an index to a svg files
    row_no          = 0      #an index to a row
    col_no          = 0      #an index to a column
    pos             = 0
    num_workers     = 0 
    remaining_dumps = 0
    remaining_plots = 0
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            if 'done' in f.split('.'):
                #worker_xxxx_figure_0001_rows_0006_cols_0004_pos_0001.done
                DONEs.append (f[11:])
    for file in sorted(configs['input_files']):
        file_no     +=  1      
        tmp          =  open(file.strip(), 'r').readlines()
        csv_files    =  []
        for line in tmp:
            if line.strip() !='':
                if not  (os.path.isfile(line.strip()) or os.path.isdir(line.strip())):
                    print ("\nFATAL: this is neither a file nor a dir: "+str(line)+"\nExiting ..\n")
                    sys.exit(1)
                csv_files.append(line)
        total_rows   =  math.ceil(len(csv_files)/configs['columns'])
        total_cols   =  configs['columns']  
        
        #PAIRS        =  util.getPairs (csv_files, min(len(csv_files), configs['files_per_pair']))                
        PAIRS       = util.getDirsPairs (csv_files, min(len(csv_files), configs['files_per_pair']))
        pos           = 1   
        for pair in PAIRS: # a pair for each worker 
            if len(pair)>0:
                #worker_0001_figure_0001_rows_0006_cols_0004_pos_0001.done
                processed = True
                for tuple in pair:
                    if ("_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(total_rows).rjust(4,'0')+ "_cols_"+str(total_cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')+'.done') not in DONEs:
                        processed = False
                        remaining_dumps+=1
                    pos += 1

                if not processed:
                    num_workers += 1
    remaining_plots = len(configs['input_files'])
    for root, dirs, files in os.walk(configs['output_dir']+'plots'):
        for f in files:
            remaining_plots = max (0, remaining_plots-1)
    return num_workers, remaining_dumps, remaining_plots 
#--------------------------------------------------------------------------------------------
def launch(root_script, configs_file, qsub_simulation_arg, qsub_launching_arg, dependency_switch, log):
    os.environ['PLOTTING_ROOT_DIRECTORY']       = '/'.join(root_script.split('/')[:-1])
    os.environ['PLOTTING_ROOT_SCRIPT']          = root_script
    os.environ['PLOTTING_SIMULATION_CONFIGS']   = configs_file
    log.write("\nos.environ['PLOTTING_SIMULATION_CONFIGS']  = "+os.getenv('PLOTTING_SIMULATION_CONFIGS'))

    print ("Please wait ..")    
    simulation_job_id   = (subprocess.Popen (qsub_simulation_arg, stdout=subprocess.PIPE, universal_newlines=True)).stdout.read().replace('\n','').strip()
    log.write ("\nSimulation job dispatched .. "+simulation_job_id+"\nI will wait 10 seconds before dispatching the Launching job, Please wait ...")
    print     ("Simulation job dispatched .. "+simulation_job_id+"\nI will wait 10 seconds before dispatching the Launching job, Please wait ...")
    log.flush()
    time.sleep(10)
    launching_job_id    = (subprocess.Popen (qsub_launching_arg+[dependency_switch, "depend=afterany:"+simulation_job_id.split(".")[0]], stdout=subprocess.PIPE, universal_newlines=True)).stdout.read().replace('\n','').strip() 
    log.write ("\nLaunch job dispatched .. "+launching_job_id+"\n")  
    print ("Launch job dispatched .. "+launching_job_id+"\n")
    log.flush()
    log.close()
#--------------------------------------------------------------------------------------------
if __name__ == "__main__":    
    timestamp    = time.strftime("%B-%d-%Y-h%Hm%Ms%S")   
    log = open (os.path.join (util.slash(os.getenv('PLOTTING_LAUNCHING_DIRECTORY')), "launcher.log" ), "a") 
    log.write("\n======================================\n"+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+"\n======================================\n")
    configs_file    = util.getCommandLineArg ()  
    configs_file    = os.path.abspath(configs_file)
    print ("configs_file: "+configs_file)
    assert (os.path.isfile (configs_file))     
    
    configs      = init.load_simulation_configs (configs_file, 0) #passing 0 will cause the creation of configs['output_dir'] and its subdirs    
    
    if not os.path.isdir(configs['output_dir']+"qsub"):
        os.makedirs(configs['output_dir']+"qsub") 
    ##########################################################################
    num_workers, remaining_dumps, remaining_plots  = needed_workers (configs)
    ##########################################################################
    print("number of workers: "+str(num_workers)+"\nremaining_dumps: "+str(remaining_dumps)+"\nremaining_plots: "+str(remaining_plots))
    log.write("\nnumber of workers: "+str(num_workers)+"\nremaining_dumps: "+str(remaining_dumps)+"\nremaining_plots: "+str(remaining_plots))   
    
    if remaining_dumps >0 or remaining_plots>0: # a job is considered done if dumps completed and plots completed
        minutes = max (30, min(90, num_workers * 3))
        if configs['walltime']>0:
            minutes=configs['walltime']
        sub_cmd           = "qsub"
        nodes             = 0
        host              = ''.join([i for i in socket.gethostname() if not i.isdigit()])
        plotting_job      = util.slash(configs['job_submission_dir'])+"submission_"+host+"_"+configs['timestamp']+".sh"
        sim_specs         = open (plotting_job, 'w')
        launch_job        = os.getenv('PLOTTING_LAUNCHING_JOB')
        dependency_switch = "-W" 
          
        if  "colosse" in host:
            print ("We are on colosse, eh!")
            sub_cmd    = "msub"
            dependency_switch ="-l"           
            nodes      = max(1, math.ceil(max(1.0, math.ceil(float(num_workers+1)/8.0))))
            sim_specs.write("#!/bin/bash")
            sim_specs.write("\n#PBS -l nodes="+str(nodes)+":ppn=8")
            sim_specs.write("\n#PBS -l walltime="+str(math.floor(minutes/60))+":"+str(minutes%60)+":00")
            sim_specs.write("\n#PBS -A ymj-002-aa")
            sim_specs.write("\n#PBS -q short") 
            sim_specs.write("\n\nmodule load compilers/intel/14.0\nmodule load mpi/openmpi/1.6.5\nmodule load libs/mkl/11.1")
            sim_specs.write("\n\ncd "+ '/'.join(configs['PLOTTING_ROOT_SCRIPT'].split('/')[:-1]))
            sim_specs.write("\n\nmpirun --mca mpi_warn_on_fork 0 -n "+str(nodes*8)+" python3 "+configs['PLOTTING_ROOT_SCRIPT']+" "+configs_file)
            log.write("\nmpirun -n "+str(nodes*8)) 
            
        elif "lg" in host or "gm" in host or "r-n" in host: #guililmin
            print ("We are on Guillimin, eh!")
            nodes      = num_workers+1 #math.ceil(max(1.0, math.ceil(float(num_workers+1)))/configs['files_per_worker']) #+1 for master         
            sim_specs.write("#!/bin/bash")
            sim_specs.write("\n#PBS -l procs="+str(nodes))
            sim_specs.write("\n#PBS -l walltime=00:"+str(minutes)+":00")
            sim_specs.write("\n#PBS -l pmem=4gb")
            sim_specs.write("\n#PBS -A ymj-002-aa")
            sim_specs.write("\n\nmodule load gcc/4.9.1\nmodule load MKL/11.2\nmodule load openmpi/1.8.3-gcc")
            sim_specs.write("\n\ncd "+ '/'.join(configs['PLOTTING_ROOT_SCRIPT'].split('/')[:-1]))
            sim_specs.write("\n\nmpirun --mca mpi_warn_on_fork 0 -n "+str(nodes)+" python3 "+configs['PLOTTING_ROOT_SCRIPT']+" "+configs_file)
            
        elif "ip" in host or "cp" in host: #mammoth
            print ("We are on Mammoth, eh!")
            nodes      = math.ceil(max(1.0, math.ceil(float(num_workers+1)/24))) #+1 for master
            sim_specs.write("#!/bin/bash")
            sim_specs.write("\n#PBS -l nodes="+str(nodes)+":ppn=1")
            sim_specs.write("\n#PBS -l walltime=00:"+str(minutes)+":00")
            sim_specs.write("\n#PBS -A ymj-002-aa")
            sim_specs.write("\nmodule unload intel64/12.0.5.220\nmodule unload pgi64/11.10\nmodule unload pathscale/4.0.12.1\nmodule load intel64/13.1.3.192\nmodule load pathscale/5.0.5\nmodule load pgi64/12.5\nmodule load openmpi_intel64/1.6.5\n")
            sim_specs.write("\n\ncd "+ '/'.join(configs['PLOTTING_ROOT_SCRIPT'].split('/')[:-1])) 
            sim_specs.write("\nmpirun --mca mpi_warn_on_fork 0 -n "+str(nodes*24)+" python3 "+configs['PLOTTING_ROOT_SCRIPT']+" "+configs_file)
        else:
            print ("I couldn't determine which host is this: "+host)
            print ("Exiting ..")
            sys.exit(1)
        #--------------------
        sim_specs.flush()
        sim_specs.close()
        #--------------------
        job_name              = configs['jobname'].strip()
        qsub_simulation_arg   = [sub_cmd, "-N", job_name,  "-o",  configs['qsub_dir']+"qsub_simulation_output_"+host+'_'+configs['timestamp']+".txt", "-e",  configs['output_dir']+"qsub/qsub_simulation_error_"+host+'_'+configs['timestamp']+".txt", "-V", plotting_job]
        qsub_launching_arg    = [sub_cmd,  "-N", job_name,  "-o", configs['qsub_dir']+"qsub_launching_output_" +host+'_'+configs['timestamp']+".txt", "-e",  configs['output_dir']+"qsub/qsub_launching_error_" +host+'_'+configs['timestamp']+".txt",  "-V",launch_job]
 
        launch (configs['PLOTTING_ROOT_SCRIPT'], configs_file, qsub_simulation_arg, qsub_launching_arg, dependency_switch, log)
 
    else:
        print     ("This job is done. No need to launch (done's == no. input files) and number of file in /plots dir == len(configs[input_files])")
        log.write ("\nThis job is done. No need to launch (done's == no. input files)")     
        log.flush ()
        log.close ()
    
