import sys, os
#--------------------------------------------------------------------------------------
def getCommandLineArg():
    try:
        input_file  = str(sys.argv[1])
    except:
        print ('Usage: python3 plot_in_pairs.py [input-file (containing paths to BY_GENE.csv files) ] \nExiting...')
        sys.exit(1)
    return input_file
#--------------------------------------------------------------------------------------

#Suratanee_RAW_INSTANCES_p25.0_t5.0_V3_MINKNAP_4X_BOTH_REVERSE_June-01-2016-h01m03s47.csv

if __name__ == "__main__": 
    input_file = getCommandLineArg()
    ALL_FILES = open(input_file,'r').readlines()
    ALL_Ps        = []
    ALL_Ts        = []
    ALL_Solvers   = []
    ALL_NEP_modes = []
    ALL_Reduction_modes = []
    ALL_Networks  = []
    
    SPECS = {}
    i=0 # in the input file, put files in the order u want them to be plotted (e.g. Suratanee Reverse >> Suratanee Scramble >> ER_Suratanee Reverse >> ER_Suratanee Scramble
    for file in ALL_FILES:
        
        split = file.strip().split('/')[-1].split("_RAW_INSTANCES_")
        network_name, simulation_configs = split[0], split[1].split('_')
        
        SPECS[i]={}
        SPECS[i][network_name]={}
        SPECS[i][network_name]['name']           = network_name
        SPECS[i][network_name]['p']              = float(''.join([d for d in simulation_configs[0] if d.isdigit() or d=='.']))
        SPECS[i][network_name]['t']              = float(''.join([d for d in simulation_configs[1] if d.isdigit() or d=='.']))
        SPECS[i][network_name]['version']        = simulation_configs[2]
        SPECS[i][network_name]['solver']         = simulation_configs[3]
        SPECS[i][network_name]['rounds']         = simulation_configs[4]
        SPECS[i][network_name]['NEP_mode']       = simulation_configs[5]
        SPECS[i][network_name]['reduction_mode'] = simulation_configs[6]     
        SPECS[i][network_name]['path_to_data']   = file


        ALL_Ps.append         (SPECS[i][network_name]['p'])
        ALL_Ts.append         (SPECS[i][network_name]['t'])
        ALL_Solvers.append    (SPECS[i][network_name]['solver'])
        ALL_NEP_modes.append  (SPECS[i][network_name]['NEP_mode'])
        ALL_Reduction_modes.append (SPECS[i][network_name]['reduction_mode'])
        
        
        
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
    
    
    ALL_Ps = [(str(p)).rjust(5, '0') for p in list(ALL_Ps)]
    
    if not os.path.isdir(os.getcwd()+'/input'):
        os.makedirs(os.getcwd()+'/input')
    
    # BOTH, SOURCE, TARGET
    for mode in ALL_NEP_modes:
        
                                                    
        # PT
        for p in sorted(ALL_Ps):
            first_line=True
            out = open (os.getcwd()+"/input/INPUT_"+mode.strip()+"_p"+p+".txt", 'w')
            print ("python3 plot_in_pairs.py "+os.getcwd()+"/input/INPUT_"+mode.strip()+"_p"+p+".txt  && wait")
            for t in sorted(ALL_Ts):

       
                # Suratanee, ER_Suratanee
                for network_name in sorted(list(ALL_Networks), reverse=True):        
              
              
                    #rows = REVERSE, SCRAMBLE
                    for reduction in sorted(ALL_Reduction_modes):


                        # find the right file
                        for i in SPECS.keys():
                            if network_name in SPECS[i].keys():
                                if (SPECS[i][network_name]['NEP_mode'] == mode ):
                                    if (SPECS[i][network_name]['reduction_mode'] == reduction ):
                                        if (SPECS[i][network_name]['p'] == float(p) ):
                                            if (SPECS[i][network_name]['t'] == t ):
                                                #print ("writing: "+SPECS[i][network_name]['path_to_data'])
                                                if first_line:
                                                    first_line=False
                                                    out.write(SPECS[i][network_name]['path_to_data'].strip())
                                                else:
                                                    out.write("\n"+SPECS[i][network_name]['path_to_data'].strip())
                                                out.flush()
        
        out.close()

    print ('done')
    
