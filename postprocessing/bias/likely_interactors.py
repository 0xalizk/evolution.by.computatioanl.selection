from scipy import stats as scipy_stats, random
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx, os, sys, math, numpy as np
from matplotlib import rcParams
import pylab
import matplotlib.ticker as ticker
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
        print ("Usage: python3 likely_interactors.py [/absolute/path/to/network/file.txt]\nExiting..\n")
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
def ff(just,a_float):
    return str(round(a_float,1)).rjust(just,' ')
#--------------------------------------------------------------------------------------------------
def print_stats(M):
    print ("TOTAL NO. NODES "+str((M.number_of_nodes())))
    print ("TOTAL NO. EDGES "+str((M.number_of_edges())))
    
    d                = list(M.degree().values())
    dou             = list(M.out_degree().values())
    din             = list(M.in_degree().values())
   
    d_count          = {x:d.count(x) for x in d}
    dou_count       = {x:dou.count(x) for x in dou}
    din_count       = {x:din.count(x) for x in din}
    
    avg_d            = np.average(d)
    avg_set_d        = np.average(list(set(d)))
    avg_ou           = np.average(dou)
    avg_set_ou       = np.average(list(set(dou)))
    avg_in           = np.average(din)
    avg_set_in       = np.average(list(set(din)))
    
    #total_edges_belonging_to_nodes_whose_ou_degree_is_greater_than_the_average
    d_above_avg      = [x for x in d if x >  avg_d]
    d_below_avg      = [x for x in d if x <= avg_d]   
    d_set_above_avg  = set(list([x for x in d if x >  avg_set_d]))
    d_set_below_avg  = set(list([x for x in d if x <= avg_set_d])) 
    
    dou_above_avg     = [x for x in dou if x >  avg_ou]
    dou_below_avg     = [x for x in dou if x <= avg_ou]
    dou_set_above_avg = set(list([x for x in dou if x >  avg_set_ou]))
    dou_set_below_avg = set(list([x for x in dou if x <= avg_set_ou]))
    
    din_above_avg     = [x for x in din if x >  avg_in]
    din_below_avg     = [x for x in din if x <= avg_in]
    din_set_above_avg = set(list([x for x in din if x >  avg_set_in]))
    din_set_below_avg = set(list([x for x in din if x <= avg_set_in]))
    
    #nodes whose degree is abo above average
    nodes_above = len([n for n in M.nodes() if M.degree(n)> avg_d])
    nodes_below = len([n for n in M.nodes() if M.degree(n)<=avg_d])
    print ("nodes_above_avg "+str(nodes_above))
    print ("nodes_below_avg "+str(nodes_below))

    bias_d = [M.degree(n)-avg_d for n in M.nodes() if M.degree(n)>avg_d ]
    print ("bias_d:  \t"+str(sum(bias_d)))
    
    bias_ou_d = [M.out_degree(n)-avg_ou for n in M.nodes() if M.out_degree(n)>avg_ou ]
    print ("bias_ind:\t"+str(sum(bias_ou_d)))
    
    bias_in_d = [M.in_degree(n)-avg_in for n in M.nodes() if M.in_degree(n)>avg_in ]
    print ("bias_oud:\t"+str(sum(bias_in_d)))
    just = 19
    print (                                "avg".rjust(32,' ')   +"  above-avg edges".rjust(just,' ')    +"below-avg edges".rjust(just,' ')    +"above+below".rjust(just,' ')                                +"avg_set ".rjust(just,' ')   +"above-avg_set ".rjust(just,' ')      +"below-avg_set ".rjust(just,' '))
    print ("===========================================================================================================================================================================================================")
    print ("deg:".ljust(10,' ')    +'| '   +ff(just,avg_d)       +ff(just,sum(d_above_avg)/2)          + ff(just,sum(d_below_avg)/2)         + ff(just,int((sum(d_below_avg)+sum(d_above_avg))/2))         +ff(just,avg_set_d)           +ff(just,sum(d_set_above_avg))         +ff(just,sum(d_set_below_avg)))           
    print ("ou_deg:".ljust(10,' ') +'| '   +ff(just,avg_ou)      +ff(just,sum(dou_above_avg))           + ff(just,sum(dou_below_avg))          + ff(just,sum(dou_below_avg)+sum(dou_above_avg))                +ff(just,avg_set_ou)          +ff(just,sum(dou_set_above_avg))         +ff(just,sum(dou_set_below_avg)))       
    print ("in_deg:".ljust(10,' ') +'| '   +ff(just,avg_in)      +ff(just,sum(din_above_avg))           + ff(just,sum(din_below_avg))          + ff(just,sum(din_below_avg)+sum(din_above_avg))                +ff(just,avg_set_in)          +ff(just,sum(din_set_above_avg))         +ff(just,sum(din_set_below_avg)))   
    print ("===========================================================================================================================================================================================================")
   
   
    print ("(degree, frequency):sum(freq)="+ff(just,sum(d_count.values()))+"\n"        +str(d_count))
    
    
    #print ("\n(ou_deg, frequency):\n"        +str(dou_count))
    #print ("\n(in_degree, frequency):\n"   +str(din_count))
    #print ('------------------------------------------------------------------')
    '''
    print ("M.in_degrees\n" +str(sorted(set(dou))))
    print ("M.out_degrees (log):\n"+str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2)))  for d in set(dou) if d!=0])))
    print ("M.in_degrees (log):\n" +str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2))) for d in set(din) if d!=0])))
    '''
#--------------------------------------------------------------------------------------------------
def scatter(dict, ax, title, fig, xlabel, ylabel):    
    
    sc = None
    Xs, Ys, sizes, lolim, hilim = [], [], [], 0, 0
    for (source_deg,target_deg) in dict.keys():
        Xs.append (source_deg)
        Ys.append (target_deg)
        sizes.append(dict[(source_deg, target_deg)])       
        lolim=min(lolim,min(Xs))
        hilim=max(hilim,max(Xs))
    sc=ax.scatter (Xs, Ys, alpha=.7, marker='o', edgecolors='none',s=[5*z for z in sizes],  c=sizes, cmap=plt.cm.get_cmap('plasma'))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.set_xticks(range(lolim, hilim, 1))
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel (xlabel)
    ax.set_ylabel (ylabel)
    
    ax.xaxis.set_major_formatter( formatter )
    ax.xaxis.set_minor_formatter( formatter )
    ax.yaxis.set_major_formatter( formatter )
    ax.yaxis.set_minor_formatter( formatter )

    ax.xaxis.set_major_locator( locator )
    ax.xaxis.set_minor_locator( locator )
    ax.yaxis.set_major_locator( locator )
    ax.yaxis.set_minor_locator( locator )
    
    cbar = fig.colorbar(sc, shrink=0.4, pad=0.01, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label("$Frequency$")
    cbar_ax = cbar.ax
    cbar_ax.tick_params(axis='y', which='minor', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='off')
    cbar_ax.tick_params(axis='y', which='major', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='on')
    
    return ax
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    network_file = getCommandLineArgs()
    M = load_network (network_file)
    print_stats (M)  
    # who is likely to interact with whom (based on degrees)
    fig = plt.figure()
    fig.subplots_adjust(hspace = 0, wspace=0, left=.1, top=.9, right=.9, bottom=.1)
    
    likely_interactors = {}
    for e in M.in_edges_iter():
        source_deg = M.degree(e[0])
        target_deg = M.degree(e[1])
        if (source_deg,target_deg) in likely_interactors.keys():
            likely_interactors[(source_deg,target_deg)] +=1
        else:
            likely_interactors[(source_deg,target_deg)]  =1
    
    
    formatter = ticker.ScalarFormatter(useOffset=None, useMathText=True, useLocale=None)
    locator = ticker.LogLocator(base=10.0, subs=[1.0], numdecs=0, numticks=10)
    
    
    ax = fig.add_subplot(1,1,1,)
    ax = scatter(likely_interactors, ax, "Likely interactors", fig, "Degree of source node", "Degree of target node") 
    plt.savefig("likliehoods.png", dpi=1000, bbox_inches="tight")    
    plt.show()
    