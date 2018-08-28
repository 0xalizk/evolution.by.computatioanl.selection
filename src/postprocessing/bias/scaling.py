
import matplotlib.pyplot as plt
import networkx as nx, os, sys, math, numpy as np
colors = {'YlOrBr':[(0.99949250291375558, 0.95847751112545243, 0.71543254291310032), (0.99607843160629272, 0.85491734813241393, 0.4935178992795009), (0.99607843160629272, 0.69787006798912499, 0.24727413414740096), (0.95510957591673906, 0.50668205747417372, 0.11298731641442167), (0.83641677253386559, 0.33900808341362898, 0.02832756745537706), (0.62588237524032597, 0.21610150337219236, 0.014671281144461212)],
              'OrRd':  [(0.9955709345200483, 0.8996539852198433, 0.76299886072383205), (0.99215686321258545, 0.80292196484173051, 0.59001924781238335), (0.99051134235718674, 0.65763938987956327, 0.44688967828657111), (0.95864667682086724, 0.46189928428799498, 0.3103268086910248), (0.87044983471141146, 0.24855056188854516, 0.16822760867721892), (0.720230697183048, 0.024359862068120158, 0.01573241063777138)],
              'GnBu':  [(0.8682814380701851, 0.94888120258555697, 0.84765860192915976), (0.75903115623137529, 0.90563629935769474, 0.75434065285850971), (0.58477509874923561, 0.83869282007217405, 0.73448675169664268), (0.3799308030044331, 0.74309882346321554, 0.80276817784589882), (0.20845829207523198, 0.59340256172067973, 0.76899655356126673), (0.049134950339794162, 0.42611304170945108, 0.68364477087469666)]
    }

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
    numerator   = (b-a)*(x-mind)
    denumenator = maxd-mind
    return  math.pow((float(numerator)/float(denumenator)) +a,alpha)
#--------------------------------------------------------------------------------------------------
def format_ax (ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    #ax.set_xticks(range(lolim, hilim, 1))
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    #ax.set_xlabel (xlabel)
    #ax.set_ylabel (ylabel)
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
    #fig.subplots_adjust(hspace = 0, wspace=0, left=.1, top=.9, right=.9, bottom=.1)
    #ax = fig.add_subplot(1,1,1,)
    #ax = format_ax(ax)

    # we are going to map the set of all degrees [mind, maxd] into the interval [0,1]
    network_file = getCommandLineArgs()
    M    = load_network (network_file)
    original_degs = [d for d in M.degree().values()]
    mind = min(original_degs)
    maxd = max(original_degs)
    a, b = 0, 1
    ALPHAS=[3, 1.5, 1, .5, .1 ] #max |ALPHAS| = 5, that as many colors as there are
    
    c = 'GnBu'
    i = 1
    for alpha in ALPHAS:
        scaled_degs=[scale(d,mind,maxd,a,b,alpha) for d in sorted(original_degs)]
        #plt.scatter(sorted(set(original_degs)), sorted(set(scaled_degs)), c=colors[c][i])
        plt.plot(sorted(set(original_degs)), sorted(set(scaled_degs)), c=colors[c][i], linewidth=3, marker='o',markeredgecolor='none')
        #ax.text(-0.5, y, nice_repr(linestyle), **text_style)
        #ax.plot(y * points, linestyle=linestyle, color=color, linewidth=3)        
        
        i+=1
    plt.plot(sorted(set(original_degs)), [0.5]*len(sorted(set(original_degs))), linewidth=4,c='grey', linestyle='dashed')
    plt.grid(True)
    print ("original degs(set):"+" ".join([str(round(x,2)).rjust(4,' ') for x in sorted(set(original_degs))]))
    print ("scaled   degs(set):"+" ".join([str(round(x,2)).rjust(4,' ') for x in sorted(set(scaled_degs))]))
 
    plt.show()
    #plt.savefig("scaling.png", dpi=1000, bbox_inches="tight")    
    
    