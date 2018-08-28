#from scipy import interpolate
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.stats import itemfreq
import matplotlib
matplotlib.use('Agg') # This must be done before importing matplotlib.pyplot
import matplotlib.pyplot as plt
import networkx as nx

def InOut_degrees (M):
    
    indegrees = {}
    outdegrees = {}
    for n in M.nodes():
        i = M.in_degree(n) 
        if i not in indegrees:
            indegrees[i] = 0 
        indegrees[i] += 1
        
        o = M.out_degree(n)
        if o not in outdegrees:
            outdegrees[o]=0
        outdegrees[o]+=1
    return sorted(indegrees.items()), sorted(outdegrees.items())
    #return [(deg, number_of_nodes) for deg

n = 2000
M = nx.scale_free_graph(n)
#M=nx.erdos_renyi_graph(n,0.001033859204933,seed=None,directed=True)
indeg, oudeg = InOut_degrees (M)

degree = list(M.degree().values())
in_degree = list(M.in_degree().values())
ou_degree = list(M.out_degree().values())

#print("degree "+str(sorted(M.degree().values())))
#degree = [x for (x,y) in indeg]
#num_of_nodes = [y for (x,y) in indeg]

#hist, bins = np.histogram(degree)
#hist, bins = np.histogram(degree, bins=[0,2,4,6,8, 10, 50, 100,max(degree)])
#hist, bins = np.histogram(num_of_nodes, bins=50)

#width = 10#0.7 * (bins[1] - bins[0])
#center = (bins[:-1] + bins[1:]) / 2
#plt.bar(center, hist, align='center', width=width)
#plt.bar(hist, width=width)
#binwidth=50
#plt.hist(degree, bins=[0,2,4,6,8, 10, 50, 100,max(degree)],log=True)
#plt.hist(degree, bins=range(min(degree), max(degree) + binwidth, binwidth),log=True)

#-------------
#plt.loglog
#tmp = itemfreq(degree) # Get the item frequencies
#x = tmp[:, 0] # unique values in data
#y = tmp[:, 1] # freq

#print ("tmp \n"+str(tmp))
#print ("\nx "+str(x)+"\ny "+str(y))

#plt.loglog(x,y, basex=10, basey=10, linestyle='-', marker='o', markeredgecolor='blue')
#plt.autoscale (enable=True, axis='both', tight=True)
#----------
tmp = itemfreq(in_degree) # Get the item frequencies
x = tmp[:, 0] # unique values in data
y1 = tmp[:, 1] # freq
plt.loglog(x,y1, basex=10, basey=10, linestyle='', marker='o', markeredgecolor='blue')
tmp = itemfreq(ou_degree) # Get the item frequencies
x = tmp[:, 0] # unique values in data
y2 = tmp[:, 1] # freq
#plt.autoscale (enable=True, axis='both', tight=True)
#plt.hist([y1,y2])

plt.loglog(x,y2, basex=10, basey=10, linestyle='', marker='D', markeredgecolor='red')

plt.xlabel('degree ')
plt.ylabel('number of nodes with that degree ')
plt.title('Degree Distribution')

plt.savefig("np-hist.png")