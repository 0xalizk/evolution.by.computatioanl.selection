from scipy import stats as scipy_stats, random
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx, os, sys, math, numpy as np
from matplotlib import rcParams

rcParams['axes.labelsize'] = 8
rcParams['axes.titlesize'] = 8
rcParams['xtick.labelsize'] = 6
rcParams['ytick.labelsize'] = 6
#rcParams['font.family'] = 'sans-serif'  
#rcParams['font.family'] = 'serif'  
rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
rcParams['grid.alpha'] = 0.1
rcParams['axes.grid']=False
rcParams['ytick.minor.pad']=0.01
rcParams['ytick.major.pad']=0.01
rcParams['savefig.pad_inches']=.01
rcParams['grid.color']='white'
#--------------------------------------------------------------------------------------------------
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 bias.py [/absolute/path/to/network/file.txt]\nExiting..\n")
        sys.exit()
    return str(sys.argv[1])
#--------------------------------------------------------------------------------------------------
def load_network (network_edge_file):
    edges_file = open (network_edge_file,'r') #note: with nx.Graph (undirected), there are 2951  edges, with nx.DiGraph (directed), there are 3272 edges
    M=nx.DiGraph()
    next(edges_file) #ignore the first line
    for e in edges_file:
        interaction = e.split()
        assert len(interaction)>=2
        source, target = str(interaction[0]), str(interaction[1])
        if (len(interaction) >2):
            if (str(interaction[2]) == '+'):
                Ijk=1
            elif  (str(interaction[2]) == '-'):
                Ijk=-1
            else:
                print ("Error: bad interaction sign in file "+network_edge_file+"\nExiting...")
                sys.exit()
        else:
            Ijk=flip()
        M.add_edge(source, target, sign=Ijk)
    return M

#--------------------------------------------------------------------------------------------------
def deg_dist(deg_list, ax, title):
    relfreq = scipy_stats.relfreq(deg_list, numbins=10)
    #Calculate space of values for x
    xspace = relfreq.lowerlimit + np.linspace(0, relfreq.binsize*relfreq.frequency.size, relfreq.frequency.size)    
    ax.set_xlim([xspace.min(), xspace.max()])
    #ax.set_ylim([0,1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True)
    ax.set_title(title)
    ax.set_xlabel ("Degree")
    ax.set_ylabel ("Frequency")
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.set_xticks(range(min(deg_list), max(deg_list), 3))
    ax.bar(xspace, relfreq.frequency, width=relfreq.binsize, color='forestgreen', edgecolor='none')
    return ax
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    network_file = getCommandLineArgs()
    M = load_network (network_file)
    
    ou_d = list(M.out_degree().values())
    in_d = list(M.in_degree().values())
    
    ou_d_count = {x:ou_d.count(x) for x in ou_d}
    in_d_count = {x:in_d.count(x) for x in in_d}
      
    print ("(ou_deg, frequency):\n"        +str(ou_d_count)       +  "\navg ou_degrees\n"+str(np.average(list(set(ou_d)))))  
    print ("\n(in_degree, frequency):\n"   +str(in_d_count)  +  "\navg in_degree\n"+str(np.average(list(set(in_d)))))   
    print ('\n')
    print ("M.in_degrees\n" +str(sorted(set(ou_d))))
    print ("avg "+str(np.average(list(set(in_d)))))
    print ('\n')
    print ("M.out_degrees (log):\n"+str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2)))  for d in set(ou_d) if d!=0])))
    print ('\n')
    print ("M.in_degrees (log):\n" +str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2))) for d in set(in_d) if d!=0])))
    
    
    # the following code plots degree-dist. as histogram, change number of bins in deg_dist() function above to taste
    #--------------------------------------------------------------------------------------------------
    fig = plt.figure()
    fig.subplots_adjust(hspace = .3, wspace=.3)
    
    ax = fig.add_subplot(2,2,1)
    ax = deg_dist(ou_d, ax, "Out-degree dist") 
    ax = fig.add_subplot(2,2,2)
    ax = deg_dist(in_d, ax, "In-degree dist") 
    plt.savefig("d_freq_historgram.png", dpi=500, bbox_inches="tight")    
    #--------------------------------------------------------------------------------------------------
    

    