import sys,os
sys.path.insert(0,os.getenv('lib'))
import util 
import networkx as nx
def load_network (configs):
    edges_file = open (configs['network_file'],'r') #note: with nx.Graph (undirected), there are 2951  edges, with nx.DiGraph (directed), there are 3272 edges
    M=nx.DiGraph()
    next(edges_file) #ignore the first line
    i=0
    set_nodes=[]
    for e in edges_file:
        i+=1
        set_nodes.append(e.split()[0])
        set_nodes.append(e.split()[1])
        interaction = e.split()
        assert len(interaction)>=2
        source, target = str(interaction[0]), str(interaction[1])
        if source == target:
            print ("source == target")
        if (len(interaction) >2):
            if (str(interaction[2]) == '+'):
                Ijk=1
            elif  (str(interaction[2]) == '-'):
                Ijk=-1
            else:
                print ("Error: bad interaction sign in file "+network_edge_file+"\nExiting...")
                sys.exit()
        else:
            Ijk=util.flip()
        M.add_edge(source, target, sign=Ijk)
    
    print ("lines "+str(i))
    print ("nx edges "+str(len(M.edges())))
    print ("nx nodes "+str(len(M.nodes())))
    print ("set nodes "+str(len(set(set_nodes)))) 
    # conservation scores:
    if not configs['biased']:
        return M
    else:
        return conservation_scores (M, configs)
configs={}
configs['network_file']=sys.argv[1]
configs['biased']=False
load_network(configs)

