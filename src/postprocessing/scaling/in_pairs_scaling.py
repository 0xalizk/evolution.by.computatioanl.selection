import matplotlib.pyplot as plt
#mpl.use('Agg')
import networkx as nx, os, sys, math, numpy as np, random
from matplotlib.pyplot import cm 
import matplotlib.patches as mpatches
import matplotlib.collections as collections
from matplotlib import rcParams
from myast import *

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
#for key in rcParams.keys():
#    print (str(key).ljust(30,' ')+str(rcParams[key]))
#-------------------------------------------------
def slash(path):
    return path+(path[-1] != '/')*'/'
#--------------------------------------------------------------------------------------------------
def flip():
    return random.SystemRandom().choice([1,-1])
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
def scale0 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
	# http://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
	# mapping data in interval [mind, maxd] into interval [a,b]
	#        (b-a)(x - min)
	# f(x) = --------------  + a			<<< raise all this to power alpha to dodge the linearity
    #          max - min
    if d==None:
        return py2tex('((b-a)*(d-mind))/(maxd-mind)')
    else:
        if d < meand:
            return 0
        numerator   = (b-a)*(d-mind)
        denumenator = maxd-mind
        return  numerator/denumenator
#--------------------------------------------------------------------------------------------------
def scale1 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
	# http://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
	# mapping data in interval [mind, maxd] into interval [a,b]
	#        (b-a)(x - min)
	# f(x) = --------------  + a			<<< raise all this to power alpha to dodge the linearity
    #          max - min
    if d==None:
        return py2tex('((0.5*((d-mind)**2)/N))**\u03B1')
    if d < meand:
        return 0
    numerator   = (b-a)*math.pow((d-mind), 2)
    denumenator = N
    return  math.pow((float(numerator)/float(denumenator)) +a,alpha)
#--------------------------------------------------------------------------------------------------
def scale2 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    if d==None:
        return py2tex('(((x-\u03BC)**2)/N)**\u03B1')
    if d <= meand:
        return 0
    numerator   = (b-a)*math.pow((d-meand),2)
    denumenator = N*b
    return  math.pow((float(numerator)/float(denumenator)) +a,alpha)
#--------------------------------------------------------------------------------------------------
def scale3 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    if d==None:
        return py2tex('(((d-\u03BC)**2)/N)**((1/log(d,2))**\u03B1)')
    if d <= meand:
        return 0
    numerator   = (b-a)*math.pow((d-meand),2)
    denumenator = N/2
    return  math.pow((float(numerator)/float(denumenator)) +a, (1/math.log(d,2))**alpha) 
#--------------------------------------------------------------------------------------------------
def scale4 (d=None, N=None, maxd=None, mind=None, a=None, b=None, meand=None, std=None, alpha=None):
    if d==None:
        return py2tex('(((d-\u03BC)**2)/N)**(1/(log(d**2,2))**\u03B1)')
    if d <= meand:
        return 0
    numerator   = (b-a)*math.pow((d-meand),2)
    denumenator = N
    return  math.pow((float(numerator)/float(denumenator)) +a, (1/math.log(d**2,2))**alpha) 
#--------------------------------------------------------------------------------------------------
def format_ax (ax, xlabel, ylabel):
    ax.grid(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.set_aspect('equal', adjustable='box')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.set_aspect('equal', adjustable='box')
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    #ax.set_xticks(range(lolim, hilim, 1))
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.set_xlabel (xlabel, fontsize=12)
    ax.set_ylabel (ylabel, fontsize=12)
    
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
    return ax
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    
    #----------------------------------------------------------------------------------------------
    scale = scale3
    #----------------------------------------------------------------------------------------------  
    formula = '$'+scale()+'$'
    ALPHAS = {scale0:np.arange(1,3,.5), scale1:np.arange(.2,.3,.05), scale2:np.arange(.1,1,.01), scale3:np.arange(1.6,2,.01), scale4:np.arange(.8,1.5,.1)}
    #scale1 winner 0.25
    #scale2 winner 0.21
    #scale3 winner 1.83
    #
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------   
    
    fig = plt.figure()
    # we are going to map the set of all degrees [mind, maxd] into the interval [0,1]
    input       = getCommandLineArgs()
    files       = open(input,'r').readlines()
    if len(files)>4:
        print("I can only handle 4 files at a time, if you need more add more colors to variable 'colors'\nExiting ..")
        sys.exit(1)    
    skip        = 5  
    #Spectral, PuBu
    colors      = [iter(cm.GnBu(np.linspace(0,1,len(ALPHAS[scale])+skip))), \
                   iter(cm.YlOrBr(np.linspace(0,1,len(ALPHAS[scale])+skip))),\
                   iter(cm.YlGn(np.linspace(0,1,len(ALPHAS[scale])+skip))),\
                   iter(cm.Spectral(np.linspace(0,1,len(ALPHAS[scale])+skip))), ] #http://matplotlib.org/users/colormaps.html    
    legend_size   =  int(math.log(len(ALPHAS[scale]), 2))
    print ("legend_size".ljust(30,' ')+str(legend_size)+"\nlen ALPHAS[scale]".ljust(30,' ')+str(len(ALPHAS[scale])))
    patch_entries, patch_colors, patch_labels, network_names = [], [], [], []

    j, xlim = 0, 0
    for network_file in files:
        patch_colors.append([])
        network_file      = network_file.strip().replace('\n','')
        network_names.append('$'+(network_file.split("/")[-1].split('.')[0]).replace('_','\_')+'$')
        
        color             = colors[j]        
        for i in range(skip): #increase skip value to start off with more solid color (but decrease it if len(ALPHAS) is large)
            next(color)          
        
        M                 = load_network (network_file)
        original_degs     = [d for d in M.degree().values()] 
        set_original_degs = sorted(list(set(original_degs)))
        deg_counts        = [original_degs.count(d) for d in set_original_degs]
        avg_frequency     = np.average(deg_counts)
        std               = np.std(original_degs)
        meand             = np.average(original_degs)
        mind              = min(set_original_degs)#min(deg_counts)#min(set_original_degs)
        maxd              = max(set_original_degs)
        N                 = M.number_of_nodes()
        a, b              = 0, 0.5
        xlim              = max(xlim, max(set_original_degs))
        
        degrees           = [d for d in M.degree().values()]
        assert float(sum(degrees))/N == meand        
        print("mean_all "+str(np.average(original_degs))+"\nmean_set "+str(np.average(set_original_degs))+"\nstd all "+str(np.std(original_degs))+"\nstd set "+str(np.std(set_original_degs))+'\n')      
        k=2
        maximum_harvest=[0,0]
        for alpha in ALPHAS[scale]:       
            c=next(color)
            scaled_degs=[scale(d, N, maxd, mind, a, b, meand, std, alpha) for d in set_original_degs]
            effective_harvest = [a*b*c for a,b,c in zip(scaled_degs,deg_counts,set_original_degs)]        
            
            sc=plt.plot(set_original_degs, scaled_degs, c=c, linewidth=2.5, marker='',markeredgecolor='none',alpha=.9)                 
            print (str(len(ALPHAS[scale])))
            if len(ALPHAS[scale])<15:
                if len (patch_colors)==j:
                    patch_colors.append([])                
                patch_colors[j].append(c)# = list(c)
                patch_labels.append('$\\quad\\alpha = '+str(alpha)+'$')                
            elif math.log(k,2)==int(math.log(k,2)) :
                if len (patch_colors)==j:
                    patch_colors.append([])                
                patch_colors[j].append(c)# = list(c)
                patch_labels.append('$\\quad\\alpha = '+str(alpha)+'$')
            print ("original degs(set):".ljust(37,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in set_original_degs]))
            print ("original count:".ljust(37,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in deg_counts]))
            print ("scaled degs(set), alpha ".ljust(27,' ')+(str(round(alpha,3))+":").ljust(10,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in sorted(scaled_degs)]))
            print ("scaled*count, sum ".ljust(27,' ')+ str(round(sum(effective_harvest),1)).ljust(10,' ')+" ".join([str(round(x,1)).rjust(4,' ') for x in effective_harvest]))
            print("")
            if sum(effective_harvest) > maximum_harvest[0]:
                maximum_harvest[0], maximum_harvest[1] = sum(effective_harvest), alpha
            k+=1

        #taken from plot_inverse.py
        print("")
        print ("maximum harvest "+str(maximum_harvest[0])+" at alpha "+str(maximum_harvest[1])) 
        print("")
        j += 1
    
    ax = plt.gca()
    format_ax (ax,"Degree","Conservatinon score") 
    ax.set_ylim([-.1, 1])    
    plt.plot(range(xlim), [0.5]*xlim, linewidth=4, c='grey', linestyle='-')
    plt.plot(range(xlim), [0.25]*xlim, linewidth=2, c='grey', linestyle='-')
     
    network_patch=[]
    for row in patch_colors: 
        network_patch.append(collections.CircleCollection([200]*len(row), facecolor = row, edgecolor='none'))   
    #---------------------------------------------------
    patch_colors = [x for x in zip(*patch_colors)]
    #---------------------------------------------------
    k=0
    for row in patch_colors:           
        patch_entries.append(collections.CircleCollection([200]*len(row), facecolor = row, edgecolor='none'))
        k+=1
    
    L1 = plt.legend(patch_entries, patch_labels, frameon=False, loc=(0.05, 0.75),                       scatterpoints=len(files),  scatteryoffsets=[0.18],        handlelength=3, fontsize=14, handleheight=1.3) 
    plt.gca().add_artist(L1)
    L2 = plt.legend(network_patch, network_names, frameon=False, loc=(0.6, 0.05*len(network_names)),  scatterpoints=legend_size, scatteryoffsets=[0.16], handlelength=1.5, fontsize=18, handleheight=len(network_names)*1.4)  
    plt.gca().add_artist(L2) 
    
    #plt.annotate(formula, xy=(.2, .2), xytext=(.2, .2), arrowprops=dict(facecolor='black', shrink=0.05),)
    plt.annotate(formula, xy=(12,.8), xytext=(12, .8), fontsize=30)
    plt.yticks([0,.25, .5], ['0','0.25','0.5'])
    
        
    plot_dir = slash(slash(os.getcwd())+'plots')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    file_name = 'multiple'#(network_file.split('/')[-1]).split('.')[0] 
    plt.savefig(plot_dir+file_name+".png", dpi=500,bbox_inches="tight") # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    print ("plotted: "+plot_dir+file_name+".png")  
    plt.show()  
