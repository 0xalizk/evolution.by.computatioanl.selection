import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

import numpy.random as rnd


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

n = 2000
M = nx.scale_free_graph(n)
indeg, oudeg = InOut_degrees (M)


t = [x for (x,y) in indeg]
s = [y for (x,y) in indeg]


fig = plt.figure(figsize=(12, 6))
vax = fig.add_subplot(121)


vax.plot(t, s , 'b^')
vax.vlines(t, [0], s)
vax.set_xlabel('degree')
vax.set_title('number of nodes')


plt.savefig("vlines.png")
