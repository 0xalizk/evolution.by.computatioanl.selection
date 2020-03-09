import matplotlib.pyplot as plt
#mpl.use('Agg')
import networkx as nx, os, sys, math, numpy as np, random
from matplotlib.pyplot import cm 
import matplotlib.patches as mpatches
import matplotlib.collections as collections
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
import in_pairs_scaling as sc # for the scale functions

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
if __name__ == "__main__":
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    SCALE_FUNCTIONS=[]
    for name, val in sc.__dict__.items():
        if 'scale' in name:
            SCALE_FUNCTIONS.append(val)
    ALPHAS = {}
    for s in SCALE_FUNCTIONS:
        ALPHAS[s]=np.arange(0.0001, 20, 0.001)
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------   
    
    fig = plt.figure()
    # we are going to map the set of all degrees [mind, maxd] into the interval [0,1]
    input       = getCommandLineArgs()
    files       = open(input,'r').readlines()
    if len(files)!=2:
        print("Usage: I import in_pairs_scaling.py and test all it's 'scale' function on sample data and pickup the 'sweet spot', which alpha results in maximal diff between PPI network and ER_PPI netowrk (biased harvest)\n. I expect 2 links (to edge files) in "+input+"\nExiting ..")
        sys.exit(1)    
    j= 0
    comparisons={}
    
    for scale in SCALE_FUNCTIONS:
        nnames = []
        for network_file in files[0:min(2, len(files))]:#consider only 2 files
            network_file      = network_file.strip().replace('\n','')
            nnames.append(network_file.split("/")[-1].split('.')[0])
            
            comparisons[nnames[-1]]={}

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
            k                 = 2
            maximum_harvest=[0,0]
            for alpha in ALPHAS[scale]:
                try:  
                    scaled_degs=[scale(d, N, maxd, mind, a, b, meand, std, alpha) for d in set_original_degs]
                except:
                    print ("hiccup at alpha "+str(alpha))
                    pass
                effective_harvest = [a*b*c for a,b,c in zip(scaled_degs, deg_counts, set_original_degs)]        
                comparisons[nnames[-1]][alpha]=sum(effective_harvest)         
                k+=1

            j += 1
    
        # find the sweet spot 
        diff, winner_alpha=0,0
        net1, net2 = nnames[0], nnames[1]
        print ("=================".rjust(50,' ')+'\n'+(scale.__name__).rjust(45,' ')+'\n'+"=================".rjust(50,' '))
        print ("\t".join(nnames))
        k=2
        for alpha in sorted(ALPHAS[scale]):
            if(math.log(k,2))==int(math.log(k,2)) or len(ALPHAS[scale])<20:
                print (str(round(comparisons[net1][alpha],1))+"\t\t"+str(round(comparisons[net2][alpha],1))+"\t\tdelta: "+str(round((comparisons[net1][alpha]-comparisons[net2][alpha]),1))+"\t\t \u03B1 = "+str(alpha))
            if (comparisons[net1][alpha]-comparisons[net2][alpha]) > diff:
                diff = comparisons[net1][alpha]-comparisons[net2][alpha]
                winner_alpha=alpha
            k+=1
        print ("\nsweet spot "+str(round(diff,1))+" @ alpha "+str(winner_alpha)+'\n')
            
