from scipy import stats as scipy_stats, random
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import networkx as nx, os, sys, math, numpy as np
from matplotlib import rcParams
sys.path.insert(0, os.getenv('lib'))
import util
flip = util.flip

rcParams['savefig.pad_inches'] = .2

rcParams['axes.grid']          = True
rcParams['axes.titlesize']     = 36
rcParams['axes.labelsize']     = 28

rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

rcParams['figure.titleweight']    = 'bold'
rcParams['figure.titlesize']      = 45 
rcParams['figure.subplot.hspace'] = 0.9
rcParams['figure.subplot.wspace'] = 0.1
rcParams['figure.subplot.left']   = 0.1
rcParams['figure.subplot.right']  = 0.9
rcParams['figure.subplot.top']    = 0.90 # create a space between title and subplots
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
def percentages_formatter(x, y):
    if float(x*100)>=1:
        return str(int(x*100))+"%"
    else:
        return str(x*100)+"%"       
#--------------------------------------------------------------------------------------------------
def get_xlim(network_files):
    max_x, min_x = 0,0
    for f in network_files:
        M     = load_network (f)
        ou_d  = list(M.out_degree().values())
        in_d  = list(M.in_degree().values())
        max_x = max(max_x, max(ou_d), max(in_d))
        min_x = min(max_x, min(ou_d), max(in_d))
    return [min_x, max_x]
#--------------------------------------------------------------------------------------------------    
def deg_dist_combined (in_d_count, ou_d_count, ax, xlims, display_x_label, title="Degree distribution", colors=['forestgreen','#2F67B1'], tick_interval=2.0):

    bar_width   = 0.25 + .125
    bar_spacing = 2.0
    
    min_x = xlims[0]
    max_x = xlims[1]
    ax.set_xlim([min_x-(bar_width*2), max_x+(bar_width*2)])
    #ax.set_ylim([0,1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    #ax.set_title(title)
    ax.text(.5,.75,title, horizontalalignment='center', transform=ax.transAxes, size=30)
       
    
    ax.set_xlabel("")
    if display_x_label == True:
        ax.set_xlabel ("Degree")
    ax.set_ylabel ("% nodes with that degree")
    ax.tick_params(axis='x', which='major', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='x', which='minor', left='off', right='off', bottom='off', top='off',  labelbottom='off', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    
    xticks = [tick for tick in range(min_x, max_x, int(tick_interval))]
    ax.set_xticks([t for t in xticks if t%2==0])
    ax.set_xticklabels([int(t) for t in xticks])
    
    degrees, percentage =[],[]
    divider = float(sum(in_d_count.values()))
    for deg in sorted(in_d_count.keys()):
        degrees.append(deg-(bar_width))
        percentage.append(float(in_d_count[deg])/divider)    
    plt.bar(degrees, percentage, width=bar_width, color=colors[0], edgecolor='',log=True)
    #print (str(degrees))
    degrees, percentage =[],[]
    divider = float(sum(ou_d_count.values()))
    for deg in sorted(ou_d_count.keys()):
        degrees.append(deg )
        percentage.append(float(ou_d_count[deg])/divider)    
    plt.bar(degrees, percentage, width=bar_width, color=colors[1], edgecolor='',log=True)
    #print (str(degrees))
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(percentages_formatter))
    for t in ax.xaxis.get_ticklabels():
        t.set_color('black')
    
    in_patch =  mpatches.Patch(color='#f5883f', label='in-degree')
    out_patch = mpatches.Patch(color='#63cae9', label='out-degree')
    
    plt.legend(handles=[in_patch, out_patch], loc=(.77, .5)) # see rcParams above to make changes
    return ax
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    titles, network_files = getCommandLineArgs()
    output_file_name = []
    clean_titles =[]
    for t,f in zip(titles, network_files):
        output_file_name.append(f.split('/')[-1].split('.')[0])
        clean_titles.append(t.replace('_',' '))
    output_file_name = '_'.join(output_file_name)
    
    xlims = get_xlim(network_files)
    
    # use this if you're plotting in rows: fig = plt.figure(figsize=(20*len(network_files), 10))
    fig = plt.figure(figsize=(20, 6*len(network_files))) # width x height
    fig.subplots_adjust(hspace = .1, wspace=.1) #wspace: horizental space between subplots on the same row
    fig.suptitle ("In- and out-degree distribution\n")
    
    cols = 1
    rows = len(network_files)
    pos  = 0
    for f,title, display_x_label in zip(network_files, clean_titles, [True,True]):
        pos += 1
        M = load_network (f)
    
        ou_d = list(M.out_degree().values())
        in_d = list(M.in_degree().values())
    
        ou_d_count = {x:ou_d.count(x) for x in ou_d}
        in_d_count = {x:in_d.count(x) for x in in_d}
        
        '''
        print ("(ou_deg, frequency):\n"        +str(ou_d_count)       +  "\navg ou_degrees\n"+str(np.average(list(set(ou_d)))))  
        print ("\n(in_degree, frequency):\n"   +str(in_d_count)  +  "\navg in_degree\n"+str(np.average(list(set(in_d)))))   
        print ('\n')
        print ("M.in_degrees\n" +str(sorted(set(ou_d))))
        print ("avg "+str(np.average(list(set(in_d)))))
        print ('\n')
        print ("M.out_degrees (log):\n"+str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2)))  for d in set(ou_d) if d!=0])))
        print ('\n')
        print ("M.in_degrees (log):\n" +str(sorted([float("{0:.2f}".format(round(math.log2(int(d)),2))) for d in set(in_d) if d!=0])))
        '''
    
        ax = fig.add_subplot(rows,cols,pos)
        ax = deg_dist_combined(in_d_count, ou_d_count, ax, xlims, display_x_label, title, ['#f5883f','#63cae9'], tick_interval=2.0) 
    
    print ("\n\nsaving: "+output_file_name+"_histogram.png")
    plt.savefig(output_file_name+"_histogram.png", dpi=300, bbox_inches="tight")    
    #--------------------------------------------------------------------------------------------------
