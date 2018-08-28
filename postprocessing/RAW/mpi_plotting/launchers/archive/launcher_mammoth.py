import os, sys, init, util, socket, math, json,subprocess

if __name__ == "__main__": 

    configs_file = util.getCommandLineArg()
    configs_file = os.path.abspath(configs_file)
    configs      = init.load_simulation_configs (configs_file, 0) #passing 0 will cause the creation of configs['output_dir'] and its subdirs
    
    if not os.path.isdir(configs['output_dir']+"qsub"):
        os.makedirs(configs['output_dir']+"qsub") 

    num_workers = 0
    for f in configs['input_files']:
        csv_files             = open(f, 'r').readlines()          
        for line in csv_files: 
            if line.strip() !='' and os.path.isfile(line.strip()):
                num_workers      += 1
    
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            if 'done' in f.split('.'):
                num_workers = max (0, num_workers-1)
    done = False    
    if num_workers >0: 
        # launch a job with num_pairs workers + 1 master

        #hours   = math.floor(num_workers/20)
        minutes = 90 #max(30, num_workers * 3)
        
        sub_cmd           = "qsub"
        nodes             = 0
        host              = ''.join([i for i in socket.gethostname() if not i.isdigit()])
        submission_script = util.slash(configs['job_submission_dir'])+"submission_"+host+"_"+configs['timestamp']+".sh"
        sim_specs         = open (submission_script, 'w')
  
  
        
    
        if  "colosse" in host:
            print ("We are on colosse, eh!")
            sub_cmd    = "msub"
        elif "lg" in host or "gm" in host or "r-n" in host: #guililmin
            print ("We are on Guillimin, eh!")
            nodes      = max(1, math.ceil(float(num_workers+1))) #+1 for master
            
            sim_specs.write("#!/bin/bash")
            sim_specs.write("\n#PBS -l procs="+str(nodes))
            sim_specs.write("\n#PBS -l walltime=00:"+str(minutes)+":00")
            sim_specs.write("\n#PBS -l pmem=4gb")
            sim_specs.write("\n#PBS -A ymj-002-aa")
            sim_specs.write("\n\nmodule load gcc/4.9.1\nmodule load MKL/11.2\nmodule load openmpi/1.8.3-gcc")
            sim_specs.write("\n\nmpirun --mca mpi_warn_on_fork 0 -n "+str(nodes)+" python3 "+configs['master_script']+" "+configs_file)
        elif "ip" in host or "cp" in host: #mammoth
            print ("We are on Mammoth, eh!")

            nodes      = max(1, math.ceil(float(num_workers+1)/24)) #+1 for master
            sim_specs.write("#!/bin/bash")
            sim_specs.write("\n#PBS -l nodes="+str(nodes)+":ppn=1")
            sim_specs.write("\n#PBS -l walltime=00:"+str(minutes)+":00")
            sim_specs.write("\n#PBS -A ymj-002-aa")
            sim_specs.write("\nmodule unload intel64/12.0.5.220\nmodule unload pgi64/11.10\nmodule unload pathscale/4.0.12.1\nmodule load intel64/13.1.3.192\nmodule load pathscale/5.0.5\nmodule load pgi64/12.5\nmodule load openmpi_intel64/1.6.5\n")
            sim_specs.write("\nmpirun --mca mpi_warn_on_fork 0 -n "+str(nodes*24)+" python3 "+configs['master_script']+" "+configs_file)


        else:
            print ("I couldn't determine which host is this: "+host)
            print ("Exiting ..")
            sys.exit(1)

    
        job_name              = '_'.join(configs['stamps'])[0:12]
        qsub_simulation_arg   = [sub_cmd, "-N", job_name,  "-o",  configs['output_dir']+"qsub/qsub_simulation_output_"+host+'_'+configs['timestamp']+".txt", "-e",  configs['output_dir']+"qsub/qsub_simulation_error_"+host+'_'+configs['timestamp']+".txt", "-V", submission_script]
  
        if not os.path.isdir('resubmit'):
            os.makedirs('resubmit') 
        command = open('resubmit/resub-commands.sh','a')
        command.write('python launcher.py '+configs_file+'\n')
        command.close() 
        print ("go ahead and launch: \n"+' '.join(qsub_simulation_arg))
        #simulation_job_id   = (subprocess.Popen ([a.strip() for a in qsub_simulation_arg], stdout=subprocess.PIPE, universal_newlines=True)).stdout.read().replace('\n','').strip()
        #call(qsub_simulation_arg)
        #print ("\n\n"+str(simulation_job_id)+"\tlaunched")
 
    else:
        done = True
        print ("This job is done. No need to launch (done's == no. input files)")
        
    right_dir = '/'.join(sys.argv[0].split('/')[:-1])
    if len(right_dir)>0:
        right_dir=util.slash(right_dir)
    submitted = open(right_dir+'resubmit/resub-commands.sh','r').readlines()
    resubmit=[]
    first_line=True
    for line in submitted:
        conf = line.strip().split('/')[-1].replace('\n','')
        if not done or conf != configs_file.split('/')[-1]:
            resubmit.append(line)
    put_back = open(right_dir+'resubmit/resub-commands.sh','w')
    for command in set(resubmit):
        put_back.write(command)





