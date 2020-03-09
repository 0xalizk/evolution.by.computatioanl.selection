import sys, os
#--------------------------------------------------------------------------------------
def getCommandLineArg():
    try:
        input_file  = str(sys.argv[1])
    except:
        sys.stdout.write  ('Usage: python3 check_integrity.py [input-file (containing paths to RAW.csv files) ] \nExiting...')
        sys.exit(1)
    return input_file
#--------------------------------------------------------------------------------------
def getPairs (datafiles, files_per_pair):
    PAIRS = []
    counter = 0
    if len(datafiles)%files_per_pair != 0:
        sys.stdout.write  ("\n<<<<<<<<<<<<<<<<<<<<<< WARNING: number of files % files_per_pair isn't even! (last file will be ignored)>>>>>>>>>>>>>>>>>>>>>>")
        datafiles = datafiles[0:int(len(datafiles)/files_per_pair)*files_per_pair]
    while counter < len(datafiles):
        tmp = [] 
        for i in range(counter, counter+files_per_pair, 1):
            tmp.append(datafiles[i])      
        PAIRS.append(tmp)   
        counter += files_per_pair
    SUBPLOTS = [] 
    for pair in PAIRS:
        data_files = [p.strip() for p in pair]
        tmp        = [df.split('/')[-1].split('_RAW_INSTANCES_') for df in data_files]
        net_name   = [n[0] for n in tmp]
        suffix     = [n[1].split('_') for n in tmp] 
        titles     = [n+" [$"+s[0].replace('p','p=')+", "+s[1].replace('t','t=')+"$, "+s[3]+", "+s[-3]+", "+s[-2]+"]"  for n,s in zip(net_name, suffix)]
        SUBPLOTS.append ([e for e   in   zip(net_name, data_files, titles)])      
    return SUBPLOTS
#--------------------------------------------------------------------------------------
def Diagnose (PAIRS): 
    pcounter = 0
    problematic_files = []
    for pair in PAIRS:
        pcounter += 1
        #sys.stdout.write ("\n==========================================================================================\nPAIR # "+str(pcounter)+":")
        for tuple in pair:           
            prefix, file_path, title = tuple[0], tuple[1], tuple[2]
            df = open (file_path, 'r').readlines()            
            sys.stdout.write ("\ndiagnosing "+str(file_path))
            if len(df) % 5 != 0:
                sys.stdout.write ("\n\tlen(df)%5 == 0:no (trailing "+str(len(df)%5)+")".ljust(30,' '))
                #----------------------------------------------------------------------------------------
                df = df[0:int(len(df)/5)*5]
                #----------------------------------------------------------------------------------------
            else:
                sys.stdout.write ("\n\tlen(df)%5 == 0: yes".ljust(30,' '))
            num_instances = float(len(df))/5.0
            
            nils = 0
            Gs, Bs, Ds, Xs, c_t = [], [], [], [], []
            for i in range(0,len(df),5):
                Gs     = [g for g in df[i].split() if g!='nil']
                try:
                    Bs     = [int(s) for s in df[i+1].strip().split() if s!='nil']
                except:
                    problematic_files.append(file_path)
                    sys.stdout.write ("\n\tB problem on line# "+str(i+1))
                    sys.stdout.write ("\n\ttype:\t "+str(sys.exc_info()[0]))
                    sys.stdout.write ("\n\tvalue:\t"+str(sys.exc_info()[1]))
                    break
                try:
                    Ds     = [int(s) for s in df[i+2].strip().split() if s!='nil']
                except:
                    problematic_files.append(file_path)
                    sys.stdout.write ("\n\tD problem on line# "+str(i+2))
                    sys.stdout.write ("\n\ttype:\t "+str(sys.exc_info()[0]))
                    sys.stdout.write ("\n\tvalue:\t"+str(sys.exc_info()[1]))
                    break
                try:
                    Xs     = [int(x) for x in df[i+3].strip().split() if x!='nil']
                except:
                    problematic_files.append(file_path)
                    sys.stdout.write ("\n\tX problem on line# "+str(i+3))
                    sys.stdout.write ("\n\ttype:\t "+str(sys.exc_info()[0]))
                    sys.stdout.write ("\n\tvalue:\t"+str(sys.exc_info()[1]))
                    break
                try:
                    c_t    = [int (s) for s in df[i+4].strip().split() if s!='nil'] #coresize, execution_time
                except:
                    problematic_files.append(file_path)
                    sys.stdout.write ("\n\tc_t problem on line# "+str(i+4))
                    sys.stdout.write ("\n\ttype:\t "+str(sys.exc_info()[0]))
                    sys.stdout.write ("\n\tvalue:\t"+str(sys.exc_info()[1]))
                    break
                if len(Gs) == 0: # nil instance
                    nils += 1
                    try:
                        assert 0 == len(Bs) == len(Ds) == len(Xs) == len(c_t)
                    except:
                        problematic_files.append(file_path)
                        sys.stdout.write ("\n\tProblem assert 0 == len(Bs) == len(Ds) == len(Xs) == len(c_t) "+str(i)+", moving on to the next file in this pair")
                        sys.stdout.write ("\n\ttype:\t "+str(sys.exc_info()[0]))
                        sys.stdout.write ("\n\tvalue:\t"+str(sys.exc_info()[1]))
                        break 
            
            sys.stdout.write("\tinstances "+str(num_instances))  
            sys.stdout.write("\tnils      "+str(nils))
            sys.stdout.flush()    
    return problematic_files         
#--------------------------------------------------------------------------------------

if __name__ == "__main__": 
    input_file       = getCommandLineArg()
    datapoints_files = open (input_file).readlines()
    
    columns = 2  
    PAIRS   = getPairs (datapoints_files, columns)
     
    problematic_files = Diagnose (PAIRS)
    
    output=open('problematic_files.log','a')
    output.write ('\nproblematic_files:\n'+'\n'.join([f.strip() for f in problematic_files])) 
    sys.stdout.write ("\n\nDone .. see: problematic_files.log ("+str(len(problematic_files))+" bad files)")
    
