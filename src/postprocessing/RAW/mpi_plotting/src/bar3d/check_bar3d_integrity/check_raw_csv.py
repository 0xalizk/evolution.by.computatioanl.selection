import os, sys, numpy as np

def ff (n):
    return "{0:.2f}".format(n)

#######################################################################################################################
max_lines = 20000 # no need to read all the instances in the CSV files (central theorem), no. instances = max_lines/5
#######################################################################################################################

def check(input, print_progress=True):
    RESULTS = {}
    checkpoints = {100:0., 1000:0., min(20000, max_lines):0.} # use it to compare 1X 2X etc. (how many instances need to be generated before central limit theorem takes effect)
    csv_files = open (input,'r').readlines()
    for file in csv_files:# ER_Vinayagam_RAW_INSTANCES_p100.0_t000.1_V4NB_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h05m25s35.csv 
        
        name = file.split('/')[-1].strip().split('_RAW_INSTANCES_')
        
        
        net  = name[0].ljust(18,' ')#'_'.join(name[-10:]).ljust(18,' ')
        name = name[1].lower().split('_')
        p    = name[0]
        t    = name[1]
        rest = name[2].ljust(10,' ')+name[5].ljust(10,' ')+name[6].ljust(10,' ')
        key  = net+rest+' '+str(p)+' '+str(t).ljust(10,' ')
        if print_progress: 
            sys.stdout.write ('\n'+key)
        key = '-'.join(key.split())
        RESULTS[key] = {}
        for limit in checkpoints.keys():
            RESULTS[key][limit] = 0
        Bin = []
        solution = open (file.strip(),'r')
        instance = 0
        while instance <= max_lines:
            next(solution) 
            Bs = [int(b) for b in next(solution).strip().split()]
            next(solution)
            Xs = [int(x) for x in next(solution).strip().split()]
            next(solution)
            b = sum([b[0] for b in zip(Bs,Xs) if b[1]==1])
            Bin.append (b)
            
            if instance in checkpoints.keys() and instance <= max_lines:
                RESULTS[key][instance] = float(ff(np.average(Bin)))
                checkpoints[instance]  = np.average(Bin)
                if print_progress: 
                    sys.stdout.write ('\t'+ff(checkpoints[instance])+ ' ('+str(instance)+')')
                    sys.stdout.flush()                
            instance +=5
    if print_progress:
        sys.stdout.write ('\n')
    return RESULTS
if __name__ == '__main__':
    input = sys.argv[1]
    RESULTS = check(input)
    print (RESULTS)
