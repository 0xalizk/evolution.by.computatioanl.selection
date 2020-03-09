#from scipy import interpolate
import numpy as np
from scipy.interpolate import UnivariateSpline

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

def InOut_degrees (M):
    print("indegrees "+str(sorted(M.in_degree().values())))
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
indeg, oudeg = InOut_degrees (M)


#print ("max in = "+str(max(indeg))+"\nmax ou = "+str(max(oudeg)))

#plt.figure(figsize=(8, 6), dpi=80)
#plt.subplot(1, 1, 1)
degree = [x for (x,y) in indeg]
num_of_nodes = [y for (x,y) in indeg]
print (str(degree)+"\n"+str(num_of_nodes))

spl = UnivariateSpline(degree, num_of_nodes)
newx = np.linspace(min(degree), max(degree), 1000)
plt.plot(newx, spl(newx), color="blue",  linewidth=2.5, linestyle="-", label="in-degree distribution")
plt.plot(degree,num_of_nodes, color="red",  linewidth=2.5, linestyle="-", label="in-degree distribution")
degree = [x for (x,y) in oudeg]
num_of_nodes = [y for (x,y) in oudeg]
#plt.plot(degree, num_of_nodes, color="green", linewidth=2.5, linestyle="-", label="out-degree distribution")

plt.legend(loc='upper left')
plt.yscale('log')
plt.xscale('log')
plt.savefig("myplt.png")
