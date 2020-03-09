import numpy as np
sys.path.insert(0, os.getenv('lib'))
import fitting_lib 

fittest_largestC   =  fitting_lib.adj_largestC
fittest_originals  =  fitting_lib.adj_original


avg_n2e = np.average([fittest_largestC[key][0]  for key in fittest_largestC.keys()])
avg_e2n  = np.average([fittest_largestC[key][1]  for key in fittest_largestC.keys()])
print ('largest component: '.ljust(20,' ')+str(avg_n2e)+'\t'+str(avg_e2n)) #0.398888888889	1.81111111111 (largestC) or 0.438571428571	2.0 (originals)
avg_n2e = np.average([fittest_originals[key][0]  for key in fittest_originals.keys()])
avg_e2n  = np.average([fittest_originals[key][1]  for key in fittest_originals.keys()])
print ('original net: '.ljust(20,' ')+str(avg_n2e)+'\t'+str(avg_e2n)) #0.398888888889	1.81111111111 (largestC) or 0.438571428571	2.0 (originals)


