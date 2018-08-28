import os, sys, subprocess, time, socket
sys.path.insert(0, os.getenv('lib'))
sys.path.insert(0, os.getenv('SIMULATION_DIRECTORY_exec_stats')) #so I can import init.py
import init_execstats as init

def slash(path):
    return path+(path[-1] != '/')*'/'

def launch(simulation_script, launching_script, simulation_directory,launching_directory,configs_file, qsub_simulation_arg, qsub_launching_arg, dependency_switch, log):
    os.environ['SIMULATION_SCRIPT_exec_stats']    = simulation_script
    os.environ['LAUNCHING_SCRIPT_exec_stats']     = launching_script
    os.environ['SIMULATION_DIRECTORY_exec_stats'] = simulation_directory
    os.environ['LAUNCHING_DIRECTORY_exec_stats']  = launching_directory
    os.environ['SIMULATION_CONFIGS_exec_stats']   = configs_file
    log.write("\nos.environ['SIMULATION_SCRIPT_exec_stats']   = "+os.getenv('SIMULATION_SCRIPT_exec_stats'))
    log.write("\nos.environ['LAUNCHING_SCRIPT_exec_stats']    = "+os.getenv('LAUNCHING_SCRIPT_exec_stats'))
    log.write("\nos.environ['SIMULATION_DIRECTORY_exec_stats']= "+os.getenv('SIMULATION_DIRECTORY_exec_stats'))
    log.write("\nos.environ['LAUNCHING_DIRECTORY_exec_stats'] = "+os.getenv('LAUNCHING_DIRECTORY_exec_stats'))
    log.write("\nos.environ['SIMULATION_CONFIGS_exec_stats']  = "+os.getenv('SIMULATION_CONFIGS_exec_stats'))
    log.write("\nPATH  = "+os.getenv('PATH'))
    log.write("\nLD_LIBRARY_PATH  = "+os.getenv('LD_LIBRARY_PATH'))
    #print("os.environ['SIMULATION_SCRIPT_exec_stats']   = "+os.getenv('SIMULATION_SCRIPT_exec_stats'))
    #print("os.environ['LAUNCHING_SCRIPT_exec_stats']    = "+os.getenv('LAUNCHING_SCRIPT_exec_stats'))
    #print("os.environ['SIMULATION_DIRECTORY_exec_stats']= "+os.getenv('SIMULATION_DIRECTORY_exec_stats'))
    #print("os.environ['LAUNCHING_DIRECTORY_exec_stats'] = "+os.getenv('LAUNCHING_DIRECTORY_exec_stats'))
    print("os.environ['SIMULATION_CONFIGS_exec_stats']  = "+os.getenv('SIMULATION_CONFIGS_exec_stats'))
    #print("PATH  = "+os.getenv('PATH'))
    #print("LD_LIBRARY_PATH  = "+os.getenv('LD_LIBRARY_PATH'))
    print ("Please wait ..")    
    simulation_job_id   = (subprocess.Popen (qsub_simulation_arg, stdout=subprocess.PIPE, universal_newlines=True)).stdout.read().replace('\n','').strip()
    log.write ("\nSimulation job dispatched .. "+simulation_job_id+"\nI will wait 5 seconds  before dispatching the Launching job, Please wait ...")
    print ("Simulation job dispatched .. "+simulation_job_id+"\nI will wait 5 seconds before dispatching the Launching job, Please wait ...")
    log.flush()
    time.sleep(5)
    launching_job_id    = (subprocess.Popen (qsub_launching_arg+[dependency_switch, "depend=afterany:"+simulation_job_id.split(".")[0]], stdout=subprocess.PIPE, universal_newlines=True)).stdout.read().replace('\n','').strip() 
    log.write ("\nLaunch job dispatched .. "+launching_job_id+"\n")  
    print ("Launch job dispatched .. "+launching_job_id+"\n")
    log.flush()
    log.close()
if __name__ == "__main__":       
    log = open (os.path.join (slash(os.getenv('LAUNCHING_DIRECTORY_exec_stats')), "launcher_exec_stats.log" ), "a") 
    if len(sys.argv) < 2:
        log.write ("Usage: python3 launcher_vX.py [/absolute/path/to/configs/file.txt]\nExiting..\n")
        sys.exit()  
    log.write("\n======================================\n"+time.strftime("%B-%d-%Y-h%Hm%Ms%S")+"\n======================================\n")
    configs_file   = str(sys.argv[1])  
    configs_file    = os.path.abspath(configs_file)
    assert (os.path.isfile (configs_file))     
   
    timestamp   = time.strftime("%B-%d-%Y-h%Hm%Ms%S")
    configs = init.initialize_launcher(sys.argv)
    
    version_number              = configs["version"]
    network_name                = configs["network_name"]#configs [0].split("=")[1].strip()
    SCRATCH_DIR                 = slash(configs["output_directory"])+'qsub_logs/'#slash(configs [2].split("=")[1].strip())
    BD_criteria                 = configs["BD_criteria"]#configs [7].split('=')[1].strip()
    KP_solver_source            = configs["KP_solver_source"]#configs [8].split('=')[1].strip().split('/')[-1].split('.')[0]
    KP_solver_binary            = configs["KP_solver_binary"]#configs [9].split('=')[1].strip().split('/')[-1].split('.')[0]
    KP_solver_name              = configs["KP_solver_name"]
    progress_file               = configs['progress_file']
    reduction_mode              = configs['reduction_mode']
    sampling_rounds             = configs['sampling_rounds_nX']
    bias                        = configs['biased']
    advice_upon                 = configs['advice_upon']
    bORu = 'b'
    if not configs['biased']:
        bORu='u'
    #-------------------------------------------------------------
    soname = '-Wl,-soname,'+KP_solver_binary.split('/')[-1]
    compile = ['gcc', '-shared', soname, '-o', KP_solver_binary, '-fPIC', KP_solver_source]
    result = (subprocess.Popen (compile, stdout=subprocess.PIPE, universal_newlines=True)).stdout.read()       
    assert len(result) == 0 
    #-------------------------------------------------------------

    job_name = str(network_name.replace('_','')[0:3]+'_'+advice_upon[0]+bORu+'_'+sampling_rounds+'_'+KP_solver_name[0:2]+'_'+BD_criteria[0:2].upper()+reduction_mode) 
    if not os.path.isdir (SCRATCH_DIR):
        os.makedirs(SCRATCH_DIR)
    sim_script= ""
    sub_cmd   = "qsub"
    dependency_switch ="-W"
    host = ''.join([i for i in socket.gethostname() if not i.isdigit()])
    if  "colosse" in host:
        print ("We are on colosse, eh!")
        sim_script = "simulation_job_colosse.sh"
        sub_cmd    = "msub"
        dependency_switch="-l"
        launch_script="launching_job_colosse.sh"
    elif "lg" in host or "gm" in host or "r-n" in host: #guililmin
        print ("We are on Guillimin, eh!")
        sim_script = "simulation_job_guillimin.sh"
        launch_script="launching_job_guillimin.sh"
    elif "ip" in host or "cp" in host: #mammoth
        print ("We are on Mammoth, eh!")
        sim_script = "simulation_job_mammoth.sh"
        launch_script="launching_job_mammoth.sh"
    else:
        print ("I couldn't determine which host is this: "+host)
        print ("Exiting ..")
        sys.exit(1)
    
    qsub_simulation_arg         = [sub_cmd, "-N", job_name,  "-o",  SCRATCH_DIR+"qsub_simulation_output_"+host+'_'+timestamp+".txt", "-e",  SCRATCH_DIR+"qsub_simulation_error_"+host+'_'+timestamp+".txt", "-V", slash(os.getenv('LAUNCHING_DIRECTORY_exec_stats'))+sim_script]
    qsub_launching_arg          = [sub_cmd,  "-N", job_name,  "-o",  SCRATCH_DIR+"qsub_launching_output_"+host+'_'+timestamp+".txt", "-e",  SCRATCH_DIR+"qsub_launching_error_"+host+'_'+timestamp+".txt",  "-V", slash(os.getenv('LAUNCHING_DIRECTORY_exec_stats'))+launch_script]

    simulation_script           = os.getenv('SIMULATION_SCRIPT_exec_stats') 
    launching_script            = os.getenv('LAUNCHING_SCRIPT_exec_stats') 
    simulation_directory        = os.getenv('SIMULATION_DIRECTORY_exec_stats') 
    launching_directory         = os.getenv('LAUNCHING_DIRECTORY_exec_stats')   

    if os.path.isfile (progress_file):
        progress = (open (configs['progress_file'],"r")).readlines()
        if len (progress)>0: #this is a resubmission of a previous incomplete simulation
            if (progress[-1].strip() != "done"): #this is not a new simulation ... this is the point at which chain job submission stops
               launch (simulation_script, launching_script,simulation_directory,launching_directory, configs_file, qsub_simulation_arg, qsub_launching_arg, dependency_switch, log)
            else:
               print ("\nprogress.dat == done, I won't start a new job\n")
               log.write ("\nprogress.dat == done, I won't start a new job\n")
        else: #empty progress.dat, assume this is a new submission
            launch (simulation_script, launching_script, simulation_directory,launching_directory,configs_file, qsub_simulation_arg, qsub_launching_arg, dependency_switch, log)
    else: #this is a new simulation
        launch (simulation_script, launching_script, simulation_directory,launching_directory,configs_file, qsub_simulation_arg, qsub_launching_arg, dependency_switch, log)
