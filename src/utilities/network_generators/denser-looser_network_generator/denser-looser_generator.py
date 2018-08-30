import networkx as nx, random, os, sys

#----------------------------------------------------------
def flip():
    return random.SystemRandom().choice([1,-1])
#----------------------------------------------------------
def get_params():
        if len(sys.argv)<4:
                print ('Usage: python generate.py [multiplier (e.g. 10 or -10)] [absolute_path_to_network_file] [absolute_path_to_output_file]\nExiting ..\n')
                sys.exit(1)
        else:
                return float(str(sys.argv[1])), str(sys.argv[2]), str(sys.argv[3])
#----------------------------------------------------------
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
#----------------------------------------------------------
if __name__=="__main__":
    multiplier, input_file, output_file = get_params()
    input_network = load_network(input_file)
    print ("sum-in ="+str(sum(list(input_network.in_degree().values()))))
    print ("sum-out ="+str(sum(list(input_network.out_degree().values()))))
    if multiplier >0:
        indegree_sequence  = [int(d*multiplier) for d in list(input_network.in_degree().values())]
        outdegree_sequence = [int(d*multiplier) for d in list(input_network.out_degree().values())]
    elif multiplier <0:
        print ("Only positive multipliers accepted ") 
    print ("original: "+str(len(input_network.nodes()))+" nodes, "+ str(len(input_network.edges()))+" edges")
    #http://networkx.github.io/documentation/networkx-1.7/reference/generated/networkx.generators.degree_seq.directed_configuration_model.html#networkx.generators.degree_seq.directed_configuration_model
    M = nx.directed_configuration_model (indegree_sequence, outdegree_sequence,create_using=input_network)
    #remove parallel edges
    print (str(multiplier)+"X analog: "+str(len(M.nodes()))+" nodes", str(len(M.edges()))+" edges")
