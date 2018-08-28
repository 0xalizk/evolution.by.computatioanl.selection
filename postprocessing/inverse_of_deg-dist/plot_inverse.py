import matplotlib
#matplotlib.use('Agg') # This must be done before importing matplotlib.pyplot
import matplotlib.pyplot as plt, matplotlib.patches as mpatches, numpy as np, sys, os, random, math, networkx as nx
from matplotlib.ticker import ScalarFormatter
from scipy.stats import itemfreq
from scipy.interpolate import UnivariateSpline
import matplotlib.ticker as ticker

from matplotlib import rcParams
rcParams['axes.labelsize'] = 8
rcParams['axes.titlesize'] = 12
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
#for key in rcParams.keys():
#    print(str(key)+'\t\t'+str(rcParams[key]))
rcParams['legend.borderaxespad']	    =0.5
rcParams['legend.borderpad']			=0.4
rcParams['legend.columnspacing']		=2.0
rcParams['legend.fancybox']				=False
rcParams['legend.fontsize']				= 8
rcParams['legend.frameon']				=False
rcParams['legend.handleheight']			=0.7
rcParams['legend.handlelength']			=1.0
rcParams['legend.handletextpad']		=0.8
rcParams['legend.isaxes']				=True
rcParams['legend.labelspacing']			=0.5
rcParams['legend.shadow']				=False


def myLogFormat(y,pos):
    #credit: http://stackoverflow.com/questions/21920233/matplotlib-log-scale-tick-label-number-formatting/33213196#33213196
    # Find the number of decimal places required
    decimalplaces = int(np.maximum(-np.log10(y),0))     # =0 for numbers >=1
    # Insert that number into a format string
    formatstring = '{{:.{:1d}f}}'.format(decimalplaces)
    # Return the formatted tick label
    return formatstring.format(y)
#-------------------------------------------------
def flip():
    return random.SystemRandom().choice([1,-1])
#-------------------------------------------------
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 interpolate.py [/absolute/path/to/input.txt (containing paths to edge file)]\nExiting..\n")
        sys.exit()
    return str(sys.argv[1])
#-------------------------------------------------
def load_network (network_file):
    edges_file = open (network_file,'r') #note: with nx.Graph (undirected), there are 2951  edges, with nx.DiGraph (directed), there are 3272 edges
    M=nx.DiGraph()     
    next(edges_file) #ignore the first line
    for e in edges_file:
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
if __name__ == "__main__":
    
    network_file = getCommandLineArgs()
    M = load_network(network_file)
    print ("nodes "+str(len(M.nodes()))+", edges "+str(len(M.edges())))
    degrees = list(M.degree().values())
    avg_degree = np.average(degrees)
    tmp = itemfreq(degrees) # Get the item frequencies
    degs, degs_frequencies =  tmp[:, 0], tmp[:, 1] # 0 = unique values in data, 1 = frequencies
    avg_frequency=np.average(degs_frequencies)
    print ("avg_frequency "+str(avg_frequency))
    #plt.loglog(degs, degs_frequencies, basex=10, basey=10, linestyle='', color = 'blue', alpha=0.7,
    #                            markersize=7, marker='o', markeredgecolor='blue')
    plt.plot(degs, degs_frequencies, linestyle='',color='green',alpha=0.7,markersize=7, marker='o',markeredgecolor='none')                          
    plt.plot(degs, [1./(float(df)*max(1, math.log(d,2))) for df,d in zip(degs_frequencies,degs)], color='grey')
    plt.plot(degs, [1./float(df) for df in degs_frequencies], color='blue')    
    plt.plot([avg_degree], min([1./float(df) for df in degs_frequencies]), color='orange', marker='^',markersize=20,lw=10, alpha=.9,markeredgecolor='none')
    plt.plot(min(degrees), [avg_frequency],                                color='brown', marker='>',markersize=20,lw=10, alpha=.9, markeredgecolor='none')
    
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
 
    #ax.set_yscale('log')
    #ax.set_xscale('log')   
    #ax.yaxis.set_major_formatter(ticker.FuncFormatter(myLogFormat)) #see function above, values <0 have decimals, those >0 no decimals
    #ax.xaxis.set_major_formatter(ScalarFormatter())
    
    patch=[]
    patch.append(mpatches.Patch(color='green', label='$ frequency$'))
    patch.append(mpatches.Patch(color='blue', label='$ frequency^{-1}$'))
    patch.append(mpatches.Patch(color='grey', label='$( frequency * log(degree))^{-1}$'))
    patch.append(mpatches.Patch(color='none', label=''))
    patch.append(mpatches.Patch(color='orange', label='average degree   ('+str(np.round(avg_degree,2))+')'))
    patch.append(mpatches.Patch(color='brown', label='average frequency ('+str(np.round(avg_frequency,2))+')'))
    
    plt.legend(loc='upper right', handles=patch, frameon=False)
    plt.xlabel('Degree (log) ')
    plt.ylabel('Frequency (log)')
    plt.title(network_file.split('/')[-1].split('.')[0]+' network ['+'$'+str(len(M.nodes()))+'\/\/\/\/nodes$'+']')
    
    plot_dir = slash(slash(os.getcwd())+'plots')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)
    
    file_name = (network_file.split('/')[-1]).split('.')[0] 
    plt.savefig(plot_dir+file_name+".png", dpi=300) # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    #plt.show()
    print ("plotted: "+plot_dir+file_name+".png")

    #fitting  
    '''
    spl = UnivariateSpline (degs, degs_frequencies) #http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.UnivariateSpline.html#scipy.interpolate.UnivariateSpline
    spl.set_smoothing_factor(.5)    
    computed_degs_freqs  = [spl (y) for y in degs]   
    plt.plot(degs, computed_degs_freqs, color='blue', lw=1, marker='x')
    hypothetical_degrees = np.linspace(min(degs), max(degs), 100)
    plt.plot(hypothetical_degrees, [spl (y) for y in hypothetical_degrees], color='red', lw=1)
    print ("actual".ljust(10,' ')+"computed".ljust(10,' ')+"diff_abs".ljust(10,' ')+"diff_%".ljust(10,' '))
    print(''.join(['=']*50))
    for (a,b) in zip(degs_frequencies, computed_degs_freqs):
        print (str(np.round(a,2)).ljust(10,' ')+str(np.round(b,2)).ljust(10,' ')+str(np.round(abs(a-b),4)).ljust(10, ' ')+str((np.round(abs(a-b)/max(1,a),4)*100)).ljust(5, ' ')+"  %")
    '''

    
