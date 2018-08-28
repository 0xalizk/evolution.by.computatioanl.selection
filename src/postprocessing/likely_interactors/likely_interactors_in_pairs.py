import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx, os, sys, math, numpy as np
from matplotlib import rcParams
import pylab
import matplotlib.ticker as ticker
from scipy.stats import itemfreq
from scipy import stats as scipy_stats, random

rcParams['savefig.pad_inches'] = .2

rcParams['axes.grid']          = True
rcParams['axes.titlesize']     = 36
rcParams['axes.labelsize']     = 20

rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

rcParams['figure.titleweight']    = 'bold'
rcParams['figure.titlesize']      = 45 
rcParams['figure.subplot.hspace'] = 0.2
rcParams['figure.subplot.wspace'] = 0.1  #wspace: horizental space between subplots on the same row
rcParams['figure.subplot.left']   = 0.1
rcParams['figure.subplot.right']  = 0.9
rcParams['figure.subplot.top']    = 0.9 # create a space between title and subplots
rcParams['figure.subplot.bottom'] = 0.1

rcParams['grid.alpha']         =  1
rcParams['grid.color']         =  '#63cae9'
rcParams['grid.linestyle']     =  'solid' # dashed solid dashdot dotted
rcParams['grid.linewidth']     =  0.5
rcParams['axes.grid.axis']     =  'both'
rcParams['axes.grid.which']    =  'major'


rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
rcParams['xtick.labelsize']    =  22
rcParams['xtick.major.pad']    =  4.0
rcParams['xtick.major.size']   =  10.0      # how long the tick is
rcParams['xtick.major.width']  =  1.0
rcParams['xtick.minor.pad']    =  4.0
rcParams['xtick.minor.size']   =  2.0
rcParams['xtick.minor.width']  =  0.5
rcParams['xtick.minor.visible']=  False


rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
rcParams['ytick.labelsize']    =  22
rcParams['ytick.major.pad']    =  4.0
rcParams['ytick.major.size']   =  10.0
rcParams['ytick.major.width']  =  1.0
rcParams['ytick.minor.pad']    =  4.0
rcParams['ytick.minor.size']   =  4
rcParams['ytick.minor.width']  =  0.5
rcParams['ytick.minor.visible']=  True


rcParams['legend.borderaxespad']   =  0.5
rcParams['legend.borderpad']       =  0.4
rcParams['legend.columnspacing']   =  2.0
rcParams['legend.edgecolor']       =  'inherit'
rcParams['legend.facecolor']       =  'inherit'
rcParams['legend.fancybox']        =  False
rcParams['legend.fontsize']        =  20
rcParams['legend.framealpha']      =  1
rcParams['legend.frameon']         =  False
rcParams['legend.handleheight']    =  0.7
rcParams['legend.handlelength']    =  2.0
rcParams['legend.handletextpad']   =  0.8
rcParams['legend.isaxes']          =  True
rcParams['legend.labelspacing']    =  0.5
rcParams['legend.markerscale']     =  1.0
rcParams['legend.numpoints']       =  2
rcParams['legend.scatterpoints']   =  3
rcParams['legend.shadow']          =  False


#-------------------------------------------------
def slash(path):
    return path+(path[-1] != '/')*'/'
#--------------------------------------------------------------------------------------------------
def getCommandLineArgs():
    try:
        edge_files = open(str(sys.argv[1]),'r').readlines()
        clean_paths  = []
        clean_titles = []
        for line in edge_files:
            line = line.strip().split()
            t = line[:-1]
            f = line[-1]
            assert os.path.isfile (f)
            clean_titles.append(' '.join(t))
            clean_paths.append(f)
            
        return clean_titles, clean_paths     
    except:
        print ("Usage: python3 bias.py [/absolute/path/to/input/file.txt (containing abs paths to edge files)]\nExiting..\n")
        sys.exit() 
#--------------------------------------------------------------------------------------------------
def formatter(x, y):
    if x==0:
        return ""
    return str(int(x))  
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
    print ("TOTAL NO. NODES "+str(len(M.nodes())))
    print ("TOTAL NO. EDGES "+str((M.number_of_edges())))
    
    d               = list(M.degree().values())
    dou             = list(M.out_degree().values())
    din             = list(M.in_degree().values())
   
    d_count         = {x:d.count(x) for x in d}
    dou_count       = {x:dou.count(x) for x in dou}
    din_count       = {x:din.count(x) for x in din}
    
    avg_d            = np.average(d)
    avg_set_d        = np.average(list(set(d)))
    avg_freq_d       = np.average(list(d_count.values()))
    
    avg_ou           = np.average(dou)
    avg_set_ou       = np.average(list(set(dou)))
    avg_freq_ou      = np.average(list(dou_count.values()))
    
    avg_in           = np.average(din)
    avg_set_in       = np.average(list(set(din)))
    avg_freq_in       = np.average(list(din_count.values()))
    
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
    print ("avg freq d   "+str(avg_freq_d))
    print ("avg freq dou "+str(avg_freq_ou))
    print ("avg freq din "+str(avg_freq_in))
    tmp=0
    for n in M.nodes():
        if d.count(M.degree(n)) > avg_freq_d:
            for s in M.successors(n):
                tmp+=1
    print ("no. edges originating from nodes whose degree frequency is above avg_freq "+str(tmp))
    
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
def scatter(dict, ax, title, fig, xlabel, ylabel, log=False):    
    
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
    
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.set_xticks(range(lolim, hilim, 1))
    if log==True:
        ax.set_yscale('log', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
        ax.set_xscale('log', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    else:
        ax.set_yscale('linear', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
        ax.set_xscale('linear', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    ax.set_xlabel (xlabel)
    ax.set_ylabel (ylabel)
    
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    
    '''
    ax.xaxis.set_major_formatter( formatter )
    ax.xaxis.set_minor_formatter( formatter )
    ax.yaxis.set_major_formatter( formatter )
    ax.yaxis.set_minor_formatter( formatter )

    ax.xaxis.set_major_locator( locator )
    ax.xaxis.set_minor_locator( locator )
    ax.yaxis.set_major_locator( locator )
    ax.yaxis.set_minor_locator( locator )
    '''
    cbar = fig.colorbar(sc, shrink=0.4, pad=0.01, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label("$Frequency$")
    cbar_ax = cbar.ax
    cbar_ax.tick_params(labelsize=rcParams['legend.fontsize']/2.0) 
    cbar_ax.tick_params(axis='y', which='minor', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='off')
    cbar_ax.tick_params(axis='y', which='major', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='on')
    
    return ax
#--------------------------------------------------------------------------------------------------
def save_figure(network_file):
    plot_dir = slash(slash(os.getcwd())+'plots')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    file_name = (network_file.split('/')[-1]).split('.')[0] 
    plt.savefig(plot_dir+file_name+".png", dpi=300,bbox_inches="tight") # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    print ("plotted: "+plot_dir+file_name+".png")
#--------------------------------------------------------------------------------------------------
def get_likely_interactors (M):
    likely_interactors = {}
    for e in M.in_edges_iter():
        source_deg = M.degree(e[0])
        target_deg = M.degree(e[1])
        if (source_deg,target_deg) in likely_interactors.keys():
            likely_interactors[(source_deg,target_deg)] +=1
        else:
            likely_interactors[(source_deg,target_deg)]  =1
    return likely_interactors
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    titles, network_files = getCommandLineArgs()
    output_file_name = []
    clean_titles =[]
    for t,f in zip(titles, network_files):
        output_file_name.append(f.split('/')[-1].split('.')[0])
        clean_titles.append(t.replace('_',' '))
    output_file_name = '_'.join(output_file_name)
    
    fig = plt.figure(figsize=(20, 6*len(network_files)))
    #fig.suptitle ("Likely interactors")

    rows = len(network_files)
    cols = 1
    pos  = 1
    for f,title, log in zip(network_files, clean_titles, [True, False]):
        M = load_network (f)
        print_stats (M)     
        likely_interactors = get_likely_interactors(M)
        ax = fig.add_subplot(rows, cols, pos)
        xlabel, ylabel = "Degree of source node", "Degree of target node"
        if pos==1:
            xlabel =""
        ax = scatter(likely_interactors, ax, "", fig, xlabel, ylabel, log) 
        pos+=1
    save_figure(output_file_name)
   
    #plt.show()
    
