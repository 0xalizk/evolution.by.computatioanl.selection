import os, pickle, sys, numpy as np

#################
measure = 'Bin'
#################

def get_DUMPS   (DUMP_DIR):
    MASTER_DUMPS = []
    for r, d, dumps in os.walk(DUMP_DIR.strip()):
        for file in dumps:
            if file.split('.')[-1]=='dump':
                MASTER_DUMPS.append(os.path.join(r,file))
    return MASTER_DUMPS

def ff(title):
    title = title.replace('\n',' ').replace(',','').split()
    name=title[0].ljust(18,' ')
    rest=[t.ljust(10,' ') for t in title[1:] if t.strip() !='4X' and t.strip()!='minknap']
    rest[-1]=rest[-1].ljust(15,' ')
    return name + ''.join(rest)

def fff (n):
    return "{0:.2f}".format(n)

def check(input, print_progress=True):
    RESULTS = {}
    list_of_dump_dirs = open (input,'r').readlines()
    for dir in list_of_dump_dirs:
        MASTER_DUMPS = get_DUMPS(dir)
        for dump in MASTER_DUMPS:
            current_dump = None
            with open (dump,'rb') as f:
                current_dump = pickle.load(f)
                f.close()
            title, ZLIMS, DICT_of_AVGs    =    current_dump[0], current_dump[1], current_dump[2]
            key = ff(title).split()
            key = '-'.join([key[0]]+[s.lower() for s in key[1:]])
            for pt in DICT_of_AVGs.keys():
                new_key = key+'-p'+str(pt[0]).rjust(5,'0')+'-t'+str(pt[1]).rjust(5,'0')
                RESULTS[new_key] = DICT_of_AVGs[pt]
                
            if print_progress:
                sys.stdout.write (ff(title) + str(fff(DICT_of_AVGs[(100,0.1)]['Bin']['TOT']))+'\n')
                sys.stdout.flush()
    return RESULTS
if __name__ == '__main__':
    input = sys.argv[1]
    RESULTS = check(input)
    for key in RESULTS.keys():
        print(key)
        print (str(RESULTS[key]))
        break
