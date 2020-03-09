import matplotlib
matplotlib.use('Agg') # This must be done before importing matplotlib.pyplot
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from scipy.stats import itemfreq

n = 2000
#M = nx.scale_free_graph(n)
M=nx.erdos_renyi_graph(n,0.001033859204933,seed=None,directed=True)

in_degrees, ou_degrees = list(M.in_degree().values()), list(M.out_degree().values())

tmp = itemfreq(in_degrees) # Get the item frequencies
indegs, indegs_frequencies =  tmp[:, 0], tmp[:, 1] # 0 = unique values in data, 1 = frequencies
plt.loglog(indegs, indegs_frequencies, basex=10, basey=10, linestyle='', color = 'blue', alpha=0.7,
                                markersize=7, marker='o', markeredgecolor='blue')
                                
tmp = itemfreq(ou_degrees)
outdegs, outdegs_frequencies = tmp[:, 0], tmp[:, 1] 
plt.loglog(outdegs, outdegs_frequencies, basex=10, basey=10, linestyle='', color='green', alpha=0.7,
                               markersize=7, marker='D', markeredgecolor='green')

#plt.figure(dpi=None, frameon=True)
ax = matplotlib.pyplot.gca() # gca = get current axes instance
#ax.set_autoscale_on(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tick_params( #http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    right='off',      # ticks along the right edge are off
    top='off',         # ticks along the top edge are off
)

in_patch =  mpatches.Patch(color='blue', label='In-degree')
out_patch = mpatches.Patch(color='green', label='Out-degree')
plt.legend(loc='upper right', handles=[in_patch, out_patch], frameon=False)
plt.xlabel('Degree (log) ')
plt.ylabel('Number of nodes with that degree (log)')
plt.title('Degree Distribution (network size = '+str(len(M.nodes()))+' nodes, '+str(len(M.edges()))+' edges)')

plt.savefig("np-hist.png", dpi=300) # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
