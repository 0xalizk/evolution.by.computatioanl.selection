import numpy as np
# Force matplotlib to not use any Xwindows backend.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import networkx as nx

M = nx.scale_free_graph(1000)
degrees = list(M.degree().values())
nodes = np.array (list(range(1,1001)))

x = np.array(degrees)
y = np.array(nodes)

ax = plt.figure().add_subplot(111)
#ax.set_xscale('log') 
#ax.set_yscale('log')
#plt.fill(x, y, 'r')


ax.plot(x,y,marker=mpath.Path.unit_circle(), markersize=5)

plt.savefig("line.png")

