try:
    xrange
except NameError:
    xrange = range

import sys
import random, networkx as nx
import matplotlib
matplotlib.use('Agg') # This must be done before importing matplotlib.pyplot
import matplotlib.pyplot as plt, matplotlib.patches as mpatches

#-------------------------------------------------
def sample_n_nodes(nodes,n):
    return  random.SystemRandom().sample(nodes,n)
#-------------------------------------------------
def load_network (network_file):
    edges_file = open (network_file,'r') #note: with nx.Graph (undirected), there are 2951  edges, with nx.DiGraph (directed), there are 3272 edges
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
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 sample_large_network.py [/absolute/path/to/network_file.txt]\nExiting..\n")
        sys.exit()
    return str(sys.argv[1])
#-------------------------------------------------
#-------------------------------------------------
if __name__ == "__main__":
    desired_network_size = 20000 # 3K nodes
    network_file = getCommandLineArgs()
    large_network = load_network(network_file)
    #plot deg dist + record stats
    print ("original: "+ "nodes "+str(len(large_network.nodes())) + ", edges  "+str(len(large_network.edges())))

    sample_nodes = sample_n_nodes (large_network.nodes(), desired_network_size)
    small_network = nx.DiGraph (large_network.subgraph(sample_nodes))
    
    dir = ""
    if len(network_file.split('/'))>1:   
        dir = slash ('/'.join(network_file.split('/')[:-1]))
    file_name = (network_file.split('/')[-1]).split('.')[0]+"_sampled"
    writer = open(dir+file_name+".txt","w")
    writer.write("source\ttarget\tsign")
    counter =0
    connected_nodes = []
    for e in list(small_network.edges_iter(data='sign')) :
        connected_nodes += [e[0], e[1]]
        if e[2] == 1:
            sign = "+"
        elif e[2] == -1:
            sign = "-"
        else:
            print ("WARNING: empty sign")
        writer.write("\n"+str(e[0])+" "+str(e[1])+" "+sign)
        counter +=1
    
    connected_nodes = set (connected_nodes)
    print ("sampled: "+"nodes "+str(len(connected_nodes)) + ", edges  "+str(len(small_network.edges())))
    print ("sampled network written to file: "+dir+file_name+".txt")
