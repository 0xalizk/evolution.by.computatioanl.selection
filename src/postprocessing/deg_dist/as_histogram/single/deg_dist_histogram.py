from scipy import stats as scipy_stats, random
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import networkx as nx, os, sys, math, numpy as np
from matplotlib import rcParams

rcParams['axes.labelsize'] = 11
rcParams['axes.titlesize'] = 12
rcParams['xtick.labelsize'] = 8
rcParams['ytick.labelsize'] = 8
#rcParams['font.family'] = 'sans-serif'  
#rcParams['font.family'] = 'serif'  
rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
rcParams['grid.alpha'] = 0.1
rcParams['axes.grid']=False
rcParams['xtick.minor.pad']=3
rcParams['xtick.major.pad']=3
rcParams['ytick.minor.pad']=3
rcParams['ytick.major.pad']=3
rcParams['savefig.pad_inches']=.1
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
def percentages_formatter(x, y):
    if float(x*100)>=1:
        return str(int(x*100))+"%"
    else:
        return str(x*100)+"%"
       
    '''
    significat_decimals = 0
    if float(x)>=1:
        #return '%1f' % (x*100) + "%"        
        tmp=float(x)
        while tmp >=1:
            significat_decimals+=1
            tmp = tmp/10.0
        format_string = "{:"+str(significat_decimals)+".0f}"
        print (str(x)+"\t\t\tfirst case\t\tformat_string = "+format_string)
        return format_string.format(x*100) + "%"
    else:
        #return '%1.1f' % (x*100) + "%"
        #return "{:10.2f}".format(x) + "%"        
        tmp=x
        while tmp <1:
            significat_decimals+=1
            tmp = tmp*10
        format_string = "{:"+str(significat_decimals)+"."+str(significat_decimals)+"f}"
        print (str(x)+"\t\t\tsecond case\t\tformat_string = "+format_string)
        return format_string.format(x*100) + "%"
        
        10.4 means a width of 10 characters and a precision of 4 decimal places
        http://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
        '''
#--------------------------------------------------------------------------------------------------
def deg_dist(deg_list, ax, title, color):
    numbins = 20.0
    relfreq = scipy_stats.relfreq(deg_list, numbins=int(numbins))
    #Calculate space of values for x
    xspace = relfreq.lowerlimit + np.linspace(0, relfreq.binsize*relfreq.frequency.size, relfreq.frequency.size)    
    ax.set_xlim([xspace.min(), xspace.max()])
    #ax.set_ylim([0,1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(False)
    ax.set_title(title)
    ax.set_xlabel ("Degree")
    ax.set_ylabel ("Percentage of nodes with that degree")
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    #ax.set_xticks(range(min(deg_list), max(deg_list), 2))
    ax.set_xticks(range(0, int(xspace.max()), int(math.ceil((xspace.max()/numbins) ))))
    ax.bar(xspace, relfreq.frequency, width=relfreq.binsize, color=color, edgecolor='white',log=True)
    print ("\n\nrelfreq.binsize="+str(relfreq.binsize))
    return ax
#--------------------------------------------------------------------------------------------------    
def deg_dist2(deg_count, ax, title, color, tick_interval=2.0):

    #formatter = FuncFormatter(percentages_formatter)
    

    bar_width = .50

    ax.set_xlim([min(deg_count.keys()), max(deg_count.keys())])
    #ax.set_ylim([0,1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(False)
    ax.set_title(title)
    ax.set_xlabel ("Degree")
    ax.set_ylabel ("Percentage of nodes with that degree")
    ax.tick_params(axis='x', which='major', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='x', which='minor', left='off', right='off', bottom='off', top='off',  labelbottom='off', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    #ax.set_xticks(range(min(deg_list), max(deg_list), 2))
    xticks = [tick+((bar_width/tick_interval)) for tick in range(min(deg_count.keys()), max(deg_count.keys()), int(tick_interval))]
    ax.set_xticks(xticks)
    ax.set_xticklabels([int(t) for t in xticks])
    degrees,percentage=[],[]
    divider = float(sum(deg_count.values()))
    for deg in sorted(deg_count.keys()):
        degrees.append(deg)
        percentage.append(float(deg_count[deg])/divider)
    
    plt.bar(degrees, percentage, width=bar_width, color=color, edgecolor='white',log=True)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(percentages_formatter))
    print ("sum(percentages)="+str(sum(percentage)))
    return ax
#--------------------------------------------------------------------------------------------------    
def deg_dist_combined (in_d_count, ou_d_count, ax, title="Degree distribution", colors=['forestgreen','#2F67B1'], tick_interval=2.0):

    bar_width   = 0.25 + .125
    bar_spacing = 2.0
    
    min_x = min(min(in_d_count.keys()), min(ou_d_count.keys()))
    max_x = max(max(in_d_count.keys()), max(ou_d_count.keys()))
    ax.set_xlim([min_x-(bar_width*2), max_x+(bar_width*2)])
    #ax.set_ylim([0,1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True)
    ax.set_title(title)
    ax.set_xlabel ("Degree")
    ax.set_ylabel ("Percentage of nodes with that degree")
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
    print (str(degrees))
    degrees, percentage =[],[]
    divider = float(sum(ou_d_count.values()))
    for deg in sorted(ou_d_count.keys()):
        degrees.append(deg )
        percentage.append(float(ou_d_count[deg])/divider)    
    plt.bar(degrees, percentage, width=bar_width, color=colors[1], edgecolor='',log=True)
    print (str(degrees))
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(percentages_formatter))
    ax.get_yaxis().set_tick_params(which='both', direction='out')
    ax.get_xaxis().set_tick_params(which='both', direction='out')
    return ax
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    network_file = getCommandLineArgs()
    netowrk_name = network_file.split('/')[-1].split('.')[0]
    M = load_network (network_file)
    
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

    fig = plt.figure(figsize=(10,10))
    fig.subplots_adjust(hspace = .3, wspace=.3)
    
    '''
    ax = fig.add_subplot(2,2,1)
    #ax = deg_dist(ou_d, ax, "Out-degree distribution", 'forestgreen') 
    ax = deg_dist2(ou_d_count, ax, "Out-degree distribution", 'forestgreen', tick_interval=2.0) 
        
    ax = fig.add_subplot(2,2,2)
    #ax = deg_dist(in_d, ax, "In-degree distribution", '#2F67B1') 
    ax = deg_dist2(in_d_count, ax, "In-degree distribution", '#2F67B1', tick_interval=2.0) 
    '''
    
    ax = fig.add_subplot(1,1,1)
    ax = deg_dist_combined(in_d_count, ou_d_count, ax, "Degree distribution", ['#f5883f','#63cae9'], tick_interval=2.0) 
    
    plt.savefig(netowrk_name+"_histogram.png", dpi=300, bbox_inches="tight")    
    #--------------------------------------------------------------------------------------------------
    

    
