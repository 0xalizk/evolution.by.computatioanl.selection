import sys, os, time, util, json, shutil

def load_simulation_configs (param_file, rank):

    parameters = (open(param_file,'r')).readlines()
    assert len(parameters)>0
    configs = {}
    for param in parameters:
        if len(param) > 0: #ignore empty lines
            if param[0] != '#': #ignore lines beginning with #
                param = param.split('=')
                if len (param) == 2:
                    key   = param[0].strip().replace (' ', '_')
                    value = param[1].strip()
                    configs[key] = value
    
    configs['input_files'] = [f.strip() for f in configs['input_files'].split(',')]
    configs['stamps']      = [s.strip() for s in configs['stamps'].split(',')]
    for f in configs['input_files']:
        try: 
            assert os.path.isfile(f) 
        except:
            print ("init.py says: Not a file: "+f)
    assert len(configs['stamps']) == len(configs['input_files'])
    configs['columns']            = int(configs['columns'])
    configs['output_dir']         = util.slash (util.slash (configs['output_dir']) + param_file.split('/')[-1])
    configs['job_submission_dir'] = configs['output_dir']+ "submission/"
    configs['DUMP_DIR']           = configs['output_dir']+ "dump/"
    configs['logs_dir']           = configs['output_dir']+ "logs/"
    configs['configs_dir']        = configs['output_dir']+ "configs/"
    configs['plots_dir']           = configs['output_dir']+ "plots/"
    if rank ==0: #only master creates dir, only one configs['timestamp'] is issued
        configs['timestamp']          = time.strftime("%B-%d-%Y-h%Hm%Ms%S")
        try:
            if not os.path.isdir(configs['job_submission_dir']):
                os.makedirs(configs['job_submission_dir'])
            if not os.path.isdir(configs['DUMP_DIR']):
                os.makedirs(configs['DUMP_DIR'])
            if not os.path.isdir(configs['logs_dir']):
                os.makedirs(configs['logs_dir'])
            if not os.path.isdir(configs['plots_dir']):
                os.makedirs(configs['plots_dir'])  
            if not os.path.isdir(configs['configs_dir']):
                os.makedirs(configs['configs_dir'])
            else: #always start with a fresh configs_dir              
                shutil.rmtree(configs['configs_dir'])
                os.makedirs(configs['configs_dir'])
 
        except Exception as e:
            print ("\ninit.py: FATAL, couldn't create directories\nExiting ..")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print ("\n\t\texc_type "+str(exc_type)+'\n\t\tfname '+str(fname)+'\n\t\tline no. '+str(exc_tb.tb_lineno))
            sys.exit(1)
    return configs
