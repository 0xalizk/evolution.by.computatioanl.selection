import os,sys
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util

for root,dirs,files in os.walk(sys.argv[1]):
    for d in dirs:
        for r2,ds2,fs2 in os.walk(os.path.join(root,d)):
            CSVs =  [f.replace('_EXECSTATS','') for f in fs2 if f.split('.')[-1] == 'csv']
            if len(CSVs)>1 and d=='data_points':
                # we may be in a data_points dir
                # RN_Bacteria-RegulonDB_RAW_INSTANCES_p100.0_t050.0_V4NU_DPSOLVER_1X_BOTH_REVERSE_alpha0.2.June-18-2017-h17m49s43.csv
                PTs  = [ (csv.split('_')[-8], csv.split('_')[-7]) for csv in CSVs ]
                for pt in set(PTs):
                    if PTs.count(pt)>1:
                        #print ('\n'.join(CSVs))
                        #sys.exit(1)
                        print(util.slash(os.path.join(root,d))+'*'+pt[0]+'_'+pt[1]+'*')



