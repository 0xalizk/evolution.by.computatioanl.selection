import matplotlib
matplotlib.use('Agg') # This must be done before importing matplotlib.pyplot
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from scipy.stats import itemfreq
import sys
import random
#-------------------------------------------------
def flip():
    return random.SystemRandom().choice([1,-1])
#-------------------------------------------------
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 degree_dist.py [/absolute/path/to/network_file.txt]\nExiting..\n")
        sys.exit()
    return str(sys.argv[1])
#-------------------------------------------------
def load_network (network_file):
    edges_file = open (network_file,'r') #note: with nx.Graph (undirected), there are 2951  edges, with nx.DiGraph (directed), there are 3272 edges
    M=nx.DiGraph()     
    next(edges_file) #ignore the first line
    counter = 0
    for e in edges_file:
        counter +=1
        e = e.strip()
        interaction = e.split()
        assert len(interaction)>=2
        source, target = str(interaction[0]), str(interaction[1])
        if (len(interaction) >2):
            if (str(interaction[2]) == '+'):
                Ijk=1
            elif  (str(interaction[2]) == '-'):
                Ijk=-1
            else:
                print ("Error: bad interaction sign in file "+network_file+"\nExiting...")
                sys.exit()
        else:
            Ijk=flip()     
        M.add_edge(source, target, sign=Ijk)    
    
    return M
#-------------------------------------------------
def slash(path):
    return path+(path[-1] != '/')*'/'
#-------------------------------------------------
#-------------------------------------------------
if __name__ == "__main__":
    
    network_file = getCommandLineArgs()
    M = load_network(network_file)
    print ("nodes "+str(len(M.nodes()))+", edges "+str(len(M.edges())))
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
    
    dir = ""
    if len(network_file.split('/'))>1:   
        dir = slash ('/'.join(network_file.split('/')[:-1]))
    
    file_name = (network_file.split('/')[-1]).split('.')[0] 
    plt.savefig(dir+file_name+".png", dpi=300) # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    
    print ("plotted: "+dir+file_name+".png")