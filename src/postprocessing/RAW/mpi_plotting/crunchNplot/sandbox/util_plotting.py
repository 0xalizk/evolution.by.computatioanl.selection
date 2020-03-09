import sys
#######################################################################################
def myprint(s):
    sys.stdout.write(s)
    sys.stdout.flush()
#######################################################################################
def mywrite(f,s):
    myprint(s)
    reporter = open (f, 'a')
    reporter.write(s)
    reporter.flush()
    reporter.close()
#######################################################################################
def pf(num): # credit: http://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.0f%s' % (num, ['', 'K', 'M', 'B', 'T'][magnitude])
#######################################################################################
def f1 (n):
    return "{0:.1f}".format(n)
#######################################################################################
def f2 (n):
        return "{0:.2f}".format(n)
#######################################################################################
def f3 (n):
        return "{0:.3f}".format(n)
#######################################################################################
def slash(path):
    return path+(path[-1] != '/')*'/'
#######################################################################################
def getCommandLineArg():
    try:
        input_file = str(sys.argv[1])
    except:
        print ('Usage: python3 launcher.py /path/to/configs.txt  \nExiting...')
        sys.exit(1)
    return input_file
#######################################################################################
def getPairs (datafiles, files_per_pair):
    PAIRS = []
    counter = 0
    trailing = []
    print 
    if len(datafiles)%files_per_pair != 0:                
        trailing  = datafiles[int(len(datafiles)/files_per_pair)*files_per_pair:]
        datafiles = datafiles[0:int(len(datafiles)/files_per_pair)*files_per_pair]
        sys.stdout.write  ("\n\tUtil.py says: WARNING: number of files % files_per_pair isn't even! there's a trailing pair of size "+str(len(trailing)))
    while counter < len(datafiles):
        tmp = [] 
        for i in range(counter, counter+files_per_pair, 1):
            tmp.append(datafiles[i])      
        PAIRS.append(tmp)   
        counter += files_per_pair
    tmp2=[]
    
    for i in range(len(trailing)):
        tmp2.append(trailing[i])      
    if len(tmp2)>0:
        PAIRS.append(tmp2)   
    
    SUBPLOTS = []     
    for pair in PAIRS:
        DATA_FILES=[]
        data_files = [p.strip() for p in pair]
        for df in data_files:
            spoint = '_RAW_INSTANCES_'
            if 'raw' in df.split('/')[-1].split('_') and 'instances' in df.split('/')[-1].split('_'):
                spoint = '_raw_instances_'
            DATA_FILES.append((df,spoint))

        tmp        = [e[0].split('/')[-1].split(e[1]) for e in DATA_FILES]
        net_name   = [n[0] for n in tmp]
        suffix     = [n[1].split('_') for n in tmp] 
        titles     = [n+"\n[$"+s[0].replace('p','p=')+", "+s[1].replace('t','t=')+"$, "+s[2]+", "+s[3][0:2]+", "+s[4]+", "+s[5]+", "+s[6]  for n,s in zip(net_name, suffix)] # title will be later appended with num_instances +']' in PLOTTER
        SUBPLOTS.append ([e for e   in   zip(net_name, data_files, titles)])      
    return SUBPLOTS
#######################################################################################
def getDirsPairs (data_dirs, dirs_per_pair):
    PAIRS = []
    counter = 0
    trailing = []
    print 
    if len(data_dirs)%dirs_per_pair != 0:                
        trailing  = data_dirs[int(len(data_dirs)/dirs_per_pair)*dirs_per_pair:]
        data_dirs = data_dirs[0:int(len(data_dirs)/dirs_per_pair)*dirs_per_pair]
        sys.stdout.write  ("\n\tUtil.py says: WARNING: number of files % dirs_per_pair isn't even! there's a trailing pair of size "+str(len(trailing)))
    while counter < len(data_dirs):
        tmp = [] 
        for i in range(counter, counter+dirs_per_pair, 1):
            tmp.append(data_dirs[i])      
        PAIRS.append(tmp)   
        counter += dirs_per_pair
    tmp2=[]
    
    for i in range(len(trailing)):
        tmp2.append(trailing[i])      
    if len(tmp2)>0:
        PAIRS.append(tmp2)   
    
    SUBPLOTS = []     
    for pair in PAIRS:
        DATA_DIRs = [p.strip() for p in pair]
        #/rap/ymj-002-aa/mosha/Vinayagam/v4_alpha0.2/v4eb_minknap_4X_both_reverse/02_raw_instances_simulation/data_points
        net_names, titles =  [], []
        for dd in DATA_DIRs:
            if dd[-1] == '/':
                dd = dd[:-1]
            net_names.append(dd.split('/')[-5])
            titles.append   (dd.split('/')[-5]+'\n'+', '.join(dd.split('/')[-3].split('_')))
        SUBPLOTS.append ([e for e   in   zip(net_names, DATA_DIRs, titles)])      
    return SUBPLOTS
#######################################################################################
def max_lines (pair):
    #assert configs['plot']=='green_grey_red'
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
#######################################################################################