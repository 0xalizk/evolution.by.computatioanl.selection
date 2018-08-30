import sys,os, time, util_plotting as util, json, shutil
realp = util.realp
def load_simulation_configs (param_file, rank):
    param_file = realp(param_file)
    parameters = (open(param_file,'r')).readlines()
    assert len(parameters)>0
    configs = {}
    for param in parameters:
        param=param.strip()
        if len(param) > 0: #ignore empty lines
            if param[0] != '#': #ignore lines beginning with #
                param = param.split('=')
                if len (param) == 2:
                    key   = param[0].strip().replace (' ', '_')
                    value = param[1].strip()
                    configs[key] = value
    
    configs['input_files'] = [realp(f.strip()) for f in configs['input_files'].split(',')]
    configs['stamps']      = [s.strip() for s in configs['stamps'].split(',')]
    clean_i, clean_s =[],[]
    for i in range(len(configs['input_files'])):
        if not os.path.isfile(configs['input_files'][i]): 
            if not configs['input_files'][i][0]=='#': # don't make a fuss if the file was intended to be ignored anyway
                sys.stdout.write ("\ninit.py says: ignoring this one (not a valid file or dir): "+configs['input_files'][i])
                sys.stdout.flush()
        else:
            clean_i.append(configs['input_files'][i])
            clean_s.append(configs['stamps'][i])
    configs['input_files'] = [c for c in clean_i]
    configs['stamps']      = [c for c in clean_s]
    assert len(configs['stamps']) == len(configs['input_files'])
    
    if 'include' in configs.keys():
        configs['include'] = realp(configs['include'])
        if os.path.isfile(configs['include']):
            parameters = (open(realp(configs['include']),'r')).readlines()
            for param in parameters:
                param = param.strip()
                if len(param) > 0: #ignore empty lines
                    if param[0] != '#': #ignore lines beginning with #
                        param = param.split('=')
                        if len (param) == 2:
                            key   = param[0].strip().replace (' ', '_')
                            value = param[1].strip()
                            if key not in configs.keys(): # do not override a param 
                                configs[key] = value
                                
    if 'PLOTTING_ROOT_SCRIPT' in configs.keys():
        configs['PLOTTING_ROOT_SCRIPT'] = realp(configs['PLOTTING_ROOT_SCRIPT'])
    num_instances = '_all_instances'
    if 'max_instances' in configs.keys():
        if len(configs['max_instances'])>0:
            configs['max_instances'] = int(configs['max_instances'])
            if int(configs['max_instances']) > 0:
                num_instances = '_'+str(util.pf(int(configs['max_instances'])))+'_instances'
        else:
            configs['max_instances'] = -1
    else:
        configs['max_instances'] = -1
    cruncher,plot_key = "",""
    try: 
        if 'cruncher' in configs.keys():
            cruncher = '_'+configs['cruncher']
    except:
        pass
    try:
        plot_key = configs['plot_key'].strip()
        plot_key = '_'+plot_key
    except:
        configs['plot_key'] = ""
        pass
    configs['output_dir']         = util.slash (util.slash (realp(configs['output_dir'])) + param_file.split('/')[-1]+num_instances+cruncher+plot_key)
    configs['job_submission_dir'] = configs['output_dir']+ "submission/"
    configs['DUMP_DIR']           = configs['output_dir']+ "dump/"
    configs['logs_dir']           = configs['output_dir']+ "logs/"
    configs['configs_dir']        = configs['output_dir']+ "configs/"
    configs['plots_dir']          = configs['output_dir']+ "plots/"
    configs['qsub_dir']           = configs['output_dir'] +"qsub/"
    try:
        configs['max_degree']     = int(configs['max_degree'])
    except:
        configs['max_degree']     = 100
    try:
        configs['files_per_pair']   = int(configs['files_per_pair'])
    except:
        configs['files_per_pair']   = 1
    try:
        configs['pairs_per_worker'] = int(configs['pairs_per_worker'])
    except:
        configs['pairs_per_worker'] = 1
    try:
        configs['columns']        = int(configs['columns'])
    except:
        configs['columns']        = 1
    try:
        configs['xlim']           = int(configs['xlim'])
    except:
        configs['xlim']           = None 
    try:
        configs['ylim']           = int(configs['ylim'])
    except:
        configs['ylim']           = None
    try:
        configs['dpi']            = int(configs['dpi'])
    except:
        configs['dpi']            = 300
    try: 
        configs['walltime'] = int(configs['walltime']) 
    except:
        configs['walltime'] = 0 
    try:
        if len(configs['file_extension']) == 0:
            configs['file_extension']='png'
    except:
        configs['file_extension']='png'
    try:
        configs['mode']     = str(configs['mode']).strip()
    except:
        configs['mode']     = 'percentage'
    if 'Ps' in configs.keys():
        if len(configs['Ps'].strip())>0:
            try:
                configs['Ps']  = sorted([float(p) for p in str(configs['Ps']).split(',')], reverse=True)
            except:
                configs['Ps'] = [100.0]
        else:
            configs['Ps']  = [100.0]
    if 'Ts' in configs.keys():
        if len(configs['Ts'].strip())>0:
            try:
                configs['Ts']  = sorted([float(t) for t in str(configs['Ts']).split(',')])
            except:
                configs['Ts']  = [0.1]
        else:
            configs['Ts']  = [0.1] 
    
    if rank ==0: #only master creates dir, only one configs['timestamp'] is issued
        configs['timestamp']          = time.strftime("%B-%d-%Y-h%Hm%Ms%S")
        try:
            if not os.path.isdir(configs['qsub_dir']):
                os.makedirs(configs['qsub_dir'])
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
