import sys, os
#--------------------------------------------------------------------------------------
def getCommandLineArg():
    try:
        input_file  = str(sys.argv[1])
    except:
        print ('Usage: python3 plot_in_pairs.py [input-file (containing paths to BY_GENE.csv files) ] \nExiting...')
        sys.exit(1)
    return input_file
#--------------------------------------------------------------------------------------------------
def slash(path):
    return path+(path[-1] != '/')*'/'
#--------------------------------------------------------------------------------------

#Suratanee_RAW_INSTANCES_p25.0_t5.0_V3_MINKNAP_4X_BOTH_REVERSE_June-01-2016-h01m03s47.csv

if __name__ == "__main__": 
    input_file = getCommandLineArg()
    stamp      = '.'.join(input_file.split('/')[-1].strip().replace('\n','').split('.')[0:-1])
    ALL_FILES = open(input_file,'r').readlines()
    ALL_Ps        = []
    ALL_Ts        = []
    ALL_Solvers   = []
    ALL_NEP_modes = []
    ALL_Reduction_modes = []
    ALL_Networks  = []
    ALL_versions  = []
    SPECS = {}
    i=0 # in the input file, put files in the order u want them to be plotted (e.g. Suratanee Reverse >> Suratanee Scramble >> ER_Suratanee Reverse >> ER_Suratanee Scramble
    for file in ALL_FILES:
        spoint = '_RAW_INSTANCES_'
        if 'raw' in file.strip().split('/')[-1].split('_') and 'instances' in file.strip().split('/')[-1].split('_'):
            spoint = '_raw_instances_'
        split = file.strip().split('/')[-1].split(spoint)
        network_name, simulation_configs = split[0], split[1].split('_')
        
        SPECS[i]={}
        SPECS[i][network_name]={}
        SPECS[i][network_name]['name']           = network_name
        SPECS[i][network_name]['p']              = float(''.join([d for d in simulation_configs[0] if d.isdigit() or d=='.']))
        SPECS[i][network_name]['t']              = float(''.join([d for d in simulation_configs[1] if d.isdigit() or d=='.']))
        SPECS[i][network_name]['version']        = simulation_configs[2]
        SPECS[i][network_name]['solver']         = simulation_configs[3]
        SPECS[i][network_name]['rounds']         = simulation_configs[-4]
        SPECS[i][network_name]['NEP_mode']       = simulation_configs[-3]
        SPECS[i][network_name]['reduction_mode'] = simulation_configs[-2]     
        SPECS[i][network_name]['path_to_data']   = file


        ALL_Ps.append         (SPECS[i][network_name]['p'])
        ALL_Ts.append         (SPECS[i][network_name]['t'])
        ALL_Solvers.append    (SPECS[i][network_name]['solver'])
        ALL_NEP_modes.append  (SPECS[i][network_name]['NEP_mode'])
        ALL_Reduction_modes.append (SPECS[i][network_name]['reduction_mode'])
        ALL_versions.append(SPECS[i][network_name]['version'])
        
        
        i+=1
    
    
    for i in sorted(SPECS.keys()):
        for net in SPECS[i].keys():
            ALL_Networks.append(SPECS[i][net]['name'])
            #print (">>>>"+SPECS[i][net]['name'])
    ALL_Networks        = set (ALL_Networks)
    ALL_Ps              = set (ALL_Ps)
    ALL_Ts              = set (ALL_Ts)
    ALL_Solvers         = set (ALL_Solvers)
    ALL_NEP_modes       = set (ALL_NEP_modes)
    ALL_Reduction_modes = set(ALL_Reduction_modes)
    ALL_versions        = set(ALL_versions)   
    
    ALL_Ps = [(str(p)).rjust(5, '0') for p in list(ALL_Ps)]
    
    if not os.path.isdir(slash(os.getenv('post'))+"RAW/input"):
        os.makedirs(slash(os.getenv('post'))+"RAW/input")
    #print ("modes: "+str(ALL_NEP_modes)) 
    #print ("ALL_Ps: "+str(ALL_Ps))
    #print ("ALL_Solvers: "+str(ALL_Solvers))
    #print ("ALL_versions: "+str(ALL_versions))
    csv_stamp_pairs = []
    # BOTH, SOURCE, TARGET
    printed=False

    for mode in sorted(ALL_NEP_modes):
                                                    
        # PT
        for p in sorted(ALL_Ps):
            super_network = stamp.split('.')[0]
            if len(super_network.split('_')) > 1:
                super_network=super_network.split('_')[1]
            current_dir = slash(os.getenv('post'))+"RAW/input/"+super_network+"/"
            if not os.path.isdir(current_dir):
                os.makedirs(current_dir)
            file = current_dir+"INPUT_"+stamp+"_p"+p+".txt"
            out = open (file, 'a')
            if os.stat(file).st_size != 0: 
                out.write('\n')
            
            #if not printed:
                #print ("python3 plot_in_pairs.py "+slash(os.getenv('post'))+"RAW/input/INPUT_"+stamp+"_p"+p+".txt p"+str(p).rjust(3,' ')+stamp+" > p"+p+"_"+stamp+".log &")
                #print (slash(os.getenv('post'))+"RAW/input/INPUT_"+stamp+"_p"+p+".txt p"+str(p).rjust(3,' ')+stamp)
            csv_stamp_pairs.append((current_dir+"INPUT_"+stamp+"_p"+p+".txt", stamp+"_p"+str(p)))
            first_line=True
            for t in sorted(ALL_Ts):

                #DPsolver, MINKNAP
                for solver in ALL_Solvers:


                    #rows = REVERSE, SCRAMBLE
                    for reduction in sorted(ALL_Reduction_modes):
                        
                        #V4NU, V4NB, V4EU, V4EB
                        for version in sorted(ALL_versions):
                        
                            # Suratanee, ER_Suratanee
                            for network_name in sorted(list(ALL_Networks), reverse=True):        
              
              
                                # find the right file
                                for i in SPECS.keys():
                                    if network_name in SPECS[i].keys():
                                        if (SPECS[i][network_name]['NEP_mode'] == mode ):
                                            if (SPECS[i][network_name]['version'] == version ):
                                                if (SPECS[i][network_name]['reduction_mode'] == reduction ):
                                                    if (SPECS[i][network_name]['p'] == float(p) ):
                                                        if (SPECS[i][network_name]['solver'] == solver ):
                                                            if (SPECS[i][network_name]['t'] == t ):
                                                                #print ("writing: "+SPECS[i][network_name]['path_to_data'])
                                                                if first_line:
                                                                    first_line=False
                                                                    out.write(SPECS[i][network_name]['path_to_data'].strip())
                                                                else:
                                                                    out.write("\n"+SPECS[i][network_name]['path_to_data'].strip())
                                                                out.flush()
        printed=True 
        out.close()

    CSVs = [c[0] for c in set(csv_stamp_pairs)]
    STAMPs = [c[1] for c in set(csv_stamp_pairs)]
    print ('\n<input_files'.ljust(30,' ')+'= '+','.join(CSVs))
    print ('<stamps'.ljust(29,' ')+'= '+','.join(STAMPs))
    '''print ('\ncolumns            = 4')
    print ('file_extension     = svg')

    print ('output_dir           =')
    print ('PLOTTING_ROOT_SCRIPT =') 

    print ('# used by launcher.py to determine how many workers needed')
    print ('files_per_worker     = ')

    print ('\n#default = max (30, min(90, num_workers * 3))') 
    print ('walltime=30')
  
    print ('\ndone')
    '''
