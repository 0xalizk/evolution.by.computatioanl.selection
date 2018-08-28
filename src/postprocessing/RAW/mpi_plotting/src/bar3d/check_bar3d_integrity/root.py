import check_masterdumps
import check_raw_csv
def f(n):
    return "{0:.2f}".format(n)


dump_paths = 'check_masterdumps.collect'
raw_paths  = 'check_raw_csv.collect'

result1 = check_masterdumps.check(dump_paths, print_progress=False)
result2 = check_raw_csv.check(raw_paths, print_progress=False)

keys1 = list(result1.keys())
keys2 = list(result2.keys())

common   = [k for k in keys1 if k in keys2]
uncommon = [k for k in keys1 if k not in keys2]+[k for k in keys2 if k not in keys1] 

tmp = [str(x) for x in sorted(result2[keys2[0]].keys())]
print ('='*80+'\n')
print ("FROM MASTER_DUMPS                  FROM RAW CSV\n\t\t\t "+'\t\t'.join(tmp)+'  instances\n'+'='*80)

for c in common:
    
    print(str(f(result1[c]['Bin']['TOT']))+'\t\t\t ',end='')
    for limit in sorted(result2[c].keys()):
        print (str(result2[c][limit]).ljust(15,' '),end='')
    print ('')
#print ('\n======================================\nThe following keys are singletons:\n'+str('\n'.join(uncommon)))
print ('\nDone',end='')
if len(uncommon) > 0:
    print('warning: there are '+str(len(uncommon))+' singletons')
else:
    print('\n')
