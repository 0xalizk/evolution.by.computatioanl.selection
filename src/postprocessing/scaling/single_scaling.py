import matplotlib.pyplot as plt
#mpl.use('Agg')
import networkx as nx, os, sys, math, numpy as np, random
from matplotlib.pyplot import cm 
import matplotlib.patches as mpatches
from matplotlib import rcParams
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

colors = {'YlOrBr':[(0.99949250291375558, 0.95847751112545243, 0.71543254291310032), (0.99607843160629272, 0.85491734813241393, 0.4935178992795009), (0.99607843160629272, 0.69787006798912499, 0.24727413414740096), (0.95510957591673906, 0.50668205747417372, 0.11298731641442167), (0.83641677253386559, 0.33900808341362898, 0.02832756745537706), (0.62588237524032597, 0.21610150337219236, 0.014671281144461212)],
              'OrRd':  [(0.9955709345200483, 0.8996539852198433, 0.76299886072383205), (0.99215686321258545, 0.80292196484173051, 0.59001924781238335), (0.99051134235718674, 0.65763938987956327, 0.44688967828657111), (0.95864667682086724, 0.46189928428799498, 0.3103268086910248), (0.87044983471141146, 0.24855056188854516, 0.16822760867721892), (0.720230697183048, 0.024359862068120158, 0.01573241063777138)],
              'GnBu':  [(0.8682814380701851, 0.94888120258555697, 0.84765860192915976), (0.75903115623137529, 0.90563629935769474, 0.75434065285850971), (0.58477509874923561, 0.83869282007217405, 0.73448675169664268), (0.3799308030044331, 0.74309882346321554, 0.80276817784589882), (0.20845829207523198, 0.59340256172067973, 0.76899655356126673), (0.049134950339794162, 0.42611304170945108, 0.68364477087469666)]
    }
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
def scale (x, mind,maxd,a,b,alpha):
	# http://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
	# mapping data in interval [mind, maxd] into interval [a,b]
	#        (b-a)(x - min)
	# f(x) = --------------  + a			<<< raise all this to power alpha to dodge the linearity
    #          max - min
    if x < mind:
        return 0
    numerator   = math.pow((b-a)*(x-mind), 2)
    denumenator = maxd-mind
    return  math.pow((float(numerator)/float(denumenator)) +a,alpha) 
#--------------------------------------------------------------------------------------------------
def scale2 (x, maxd, a, b, alpha, meand, std):
    if x <= meand:
        return 0
    #numerator   = math.pow((b-a)*(x-mean), 2)
    numerator   = math.pow((b-a)*(x-meand),2)
    denumenator = maxd-meand
    return  math.pow((float(numerator)/float(denumenator)) +a,alpha) #*max(1, math.log(x,2))
#--------------------------------------------------------------------------------------------------
def scale3 (x, maxd, a, b, alpha, meand, std):
    if x <= meand:
        return 0
    #numerator   = math.pow((b-a)*(x-mean), 2)
    numerator   = math.pow((b-a)*(x-meand),2)
    denumenator = maxd-meand
    return  math.pow((float(numerator)/float(denumenator)) +a,1/math.log(x,2)) #*max(1, math.log(x,2))

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
    ax.set_xlabel (xlabel)
    ax.set_ylabel (ylabel)
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
    fig = plt.figure()

    # we are going to map the set of all degrees [mind, maxd] into the interval [0,1]
    network_file      = getCommandLineArgs()
    M                 = load_network (network_file)
    original_degs     = [d for d in M.degree().values()] 
    set_original_degs = sorted(list(set(original_degs)))
    deg_counts        = [original_degs.count(d) for d in set_original_degs]
    avg_frequency     = np.average(deg_counts)
    #mind = min(set_original_degs)
    #mind = np.average(set_original_degs)
    #mind  = np.average(original_degs)
    #maxd             = max(original_degs)
    meand             = np.average(original_degs)
    std               = np.std(original_degs)
    mind              = min(set_original_degs)#min(deg_counts)#min(set_original_degs)
    maxd              = M.number_of_nodes()
    a, b              = 0, 0.5
    ALPHAS=np.arange(.1,.46,.05)#[.1,.2,.25, .35,.375, .45, 0.53,0.75,0.9, 1, 1.5, 2, 3 ]
    #--------------------------- THIS SMOOTHES THE LINE -----------------
    #set_original_degs=np.linspace(min(set_original_degs),max(set_original_degs),1000)
    #--------------------------- THIS SMOOTHES THE LINE -----------------
    
    
    #ALPHAS=np.linspace(.45, .6, 10, endpoint=False)
    skip=5
    color=iter(cm.YlOrBr(np.linspace(0,1,len(ALPHAS)+skip))) #http://matplotlib.org/users/colormaps.html
    for i in range(skip):
        next(color)
    i = 0
    patch=[]
    
    print ("original degs(set):".ljust(37,' ')+" ".join([str(round(x,2)).rjust(4,' ') for x in set_original_degs]))
    print ("original count:".ljust(37,' ')+" ".join([str(round(x,2)).rjust(4,' ') for x in deg_counts]))
    print("mean_all "+str(np.average(original_degs)))
    print("mean_set "+str(np.average(set_original_degs)))
    print("std all "+str(np.std(original_degs)))
    print("std set "+str(np.std(set_original_degs)))
    
    print ("")
    for alpha in ALPHAS:       
        c=next(color)
        #scaled_degs=[scale(d,mind,maxd,a,b,alpha) for d in set_original_degs]
        scaled_degs=[scale2 (d, maxd, a, b, alpha, meand, std) for d in set_original_degs]
        print ("scaled degs(set), alpha ".ljust(27,' ')+(str(round(alpha,3))+":").ljust(10,' ')+" ".join([str(round(x,2)).rjust(4,' ') for x in sorted(scaled_degs)]))
        effective_harvest = [a*b*c for a,b,c in zip(scaled_degs,deg_counts,set_original_degs)]        
        print ("scaled*count, sum ".ljust(27,' ')+ str(round(sum(effective_harvest),2)).ljust(10,' ')+" ".join([str(round(x,2)).rjust(4,' ') for x in effective_harvest]))
        print("")
        plt.plot(set_original_degs, scaled_degs, c=c, linewidth=2, marker='',markeredgecolor='none')
        
        i+=1

        patch.append(mpatches.Patch(color=c, label='$\\alpha$ = '+str(alpha)))

    #taken from plot_inverse.py
    inverse_freq = [1./float(df) for df in deg_counts]
    print ("inverse_freq ".ljust(37,' ')+" ".join([str(round(x,2)).rjust(4,' ') for x in inverse_freq]))
    effective_harvest = [a*b*c for a,b,c in zip(inverse_freq, deg_counts, set_original_degs)]        
    print ("inverse_freq*count, sum ".ljust(27,' ')+ str(round(sum(effective_harvest),2)).ljust(10,' ')+" ".join([str(round(x,2)).rjust(4,' ') for x in effective_harvest]))
    print("")

    ax = plt.gca()
    format_ax (ax,"Degree","") 
    #ax.set_ylim([-1, max(deg_counts)])
    ax.set_ylim([-1, 1])
    
    plt.plot(sorted(set_original_degs), [0.5]*len(sorted(set_original_degs)), linewidth=1, c='grey', linestyle='dashed')
    plt.plot(sorted(set_original_degs), [0.25]*len(sorted(set_original_degs)), linewidth=1, c='grey', linestyle='dashed')
    #plt.plot(set_original_degs, deg_counts, linestyle='',color='green',alpha=0.7,markersize=7, marker='o',markeredgecolor='none')                          
    #plt.plot(set_original_degs, [1./(float(df)*max(1, math.log(d,2))) for df,d in zip(deg_counts, set_original_degs)], color='grey')
    #plt.plot(set_original_degs, [1./float(df) for df in deg_counts], color='blue')    
    plt.plot([meand], min([1./float(df) for df in deg_counts]),      color='black', marker='^',markersize=20,lw=10, alpha=.9,markeredgecolor='none')
    plt.plot(min(set_original_degs), [np.average(deg_counts)],       color='pink', marker='>',markersize=20,lw=10, alpha=.9, markeredgecolor='none')
    
    patch.append(mpatches.Patch(color='green', label='$ frequency$'))
    patch.append(mpatches.Patch(color='blue', label='$ frequency^{-1}$'))
    patch.append(mpatches.Patch(color='grey', label='$( frequency * log(degree))^{-1}$'))
    patch.append(mpatches.Patch(color='none', label=''))
    patch.append(mpatches.Patch(color='black', label='average degree   ('+str(np.round(meand,2))+')'))
    patch.append(mpatches.Patch(color='pink', label='average frequency ('+str(np.round(avg_frequency,2))+')'))
    plt.legend(loc=(0.8, 0.01), handles=patch, frameon=False)   

    
    
    #scaling_formula="[a, b] = ["+str(a)+","+str(b)+"]\nnumerator   = math.pow((b-a)*(x-mind), 2)\ndenumenator = maxd-mind\nmath.pow((numerator/denumenator) + a, alpha)"
    # these are matplotlib.patch.Patch properties
    #props = dict(boxstyle='round', facecolor='yellow', alpha=0.5)
    # place a text box in upper left in axes coords
    #ax.text(0.65, 0.55, scaling_formula, transform=ax.transAxes, fontsize=8, verticalalignment='top', bbox=props)
    

    #ax.set_xlim([0, 5])
    
    plot_dir = slash(slash(os.getcwd())+'plots')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    file_name = (network_file.split('/')[-1]).split('.')[0] 
    plt.savefig(plot_dir+file_name+".png", dpi=500,bbox_inches="tight") # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.savefig
    print ("plotted: "+plot_dir+file_name+".png")  
    plt.show()  
