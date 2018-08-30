import networkx as nx, random, os, sys, operator

def flip():
	ran = random.SystemRandom()
	if(ran.random() > 0.5): 
		return "+"	
	else: 
		return "-"
#-----------------------------------------------------------------------
def get_params():
	if len(sys.argv)<4:
		print ('Usage: python generate.py [no. nodes] [no. edges] [absolute_path_to_output_file]\nExiting ..\n')
		sys.exit(1)
	else:
		return int(str(sys.argv[1])), int(str(sys.argv[2])), str(sys.argv[3])
#-----------------------------------------------------------------------
def remove_singletons_systematically (G):
    #this function removes edges from nodes with highest degree, and create an edge from nodes_with_zero_degree to them
    node_degree = []
    for node in G.nodes():
        node_degree.append((node, G.degree([node])[node]))
    nodes_sorted_by_degree = sorted(node_degree, key=operator.itemgetter(1), reverse=True)    
    nodes_with_zero_degree = [node[0] for node in nodes_sorted_by_degree if node[1]==0]
    '''
    print ("sorted by degree "+str(nodes_sorted_by_degree))
    print ("highest degrees node "+str(G.degree([nodes_sorted_by_degree[0][0]])))
    print ("nodes_with_zero_degree "+str(nodes_with_zero_degree))
    '''
    #take edges for highest-degree nodes and grant them to zero-degree nodes, flip() the direction 
    index_of_next_highest=0
    while len(nodes_with_zero_degree)>0:
        zero_deg_node = nodes_with_zero_degree[0]
        edges_to_select_from = G.neighbors(nodes_sorted_by_degree[index_of_next_highest][0])
        if len(edges_to_select_from) == 0: #the node with the highest degree has zero out degree, move on to the next highest
            index_of_next_highest+=1
            continue
        random_neighbor = random.SystemRandom().sample(edges_to_select_from, 1)[0]
        #print ("random neighbor "+str(random_neighbor) +" chosen from "+str(G.neighbors(nodes_sorted_by_degree[index_of_next_highest][0])))
        #if removing this edge will make the target a singleton, skip and try again
        if G.degree(random_neighbor) <=1:
            continue
        G.remove_edge(nodes_sorted_by_degree[index_of_next_highest][0], random_neighbor)
        #add an edge from zero_deg_node to a random node, direction = random
        random_node = zero_deg_node
        while random_node == zero_deg_node: #make sure the randomly selected node isn't the one with zero degree itself (no self loop)
            random_node = random.SystemRandom().sample(G.nodes(), 1)[0]
        
        if random.SystemRandom().sample([1,-1], 1)[0] == 1:
            #print ("adding "+str(zero_deg_node)+" "+str(random_node))
            G.add_edge(zero_deg_node, random_node) 
        else:
            #print ("adding "+str(zero_deg_node)+" "+str(random_node))
            G.add_edge(random_node, zero_deg_node) 
        nodes_with_zero_degree = nodes_with_zero_degree[1:]
        index_of_next_highest +=1
    # debugging ---------------------------------------------------------------------------
    '''
    node_degree=[]
    for node in G.nodes():
        node_degree.append((node, G.degree([node])[node]))
    nodes_sorted_by_degree = sorted(node_degree, key=operator.itemgetter(1), reverse=True)    
    nodes_with_zero_degree = [node[0] for node in nodes_sorted_by_degree if node[1]==0]
    print ("\nafter redist \n")
    print ("sorted by degree "+str(nodes_sorted_by_degree))
    print ("highest degrees node "+str(G.degree([nodes_sorted_by_degree[0][0]])))
    print ("nodes_with_zero_degree "+str(nodes_with_zero_degree))
    # -------------------------------------------------------------------------------------
    '''
    return G, nodes_with_zero_degree
#-----------------------------------------------------------------------
def remove_singletons_randomly (G):
    
    #this function removes edges from nodes with degree >1, selected randomly, and create an edge from nodes_with_zero_degree to a randomly selected node
    nodes_with_zero_degree = []
    for node in G.nodes():
        if G.degree([node])[node] == 0:
            nodes_with_zero_degree.append( node)
    print ("randomly assigning edges to "+str(len(nodes_with_zero_degree))+" singleton")
    #print ("before: "+str(len(nodes_with_zero_degree))+" singletons")
    while len(nodes_with_zero_degree) > 0:
        #if in previous iteration you happend to attach an edge to this singleton, skip it
        if G.degree([nodes_with_zero_degree[0]])[nodes_with_zero_degree[0]] >=1:
            nodes_with_zero_degree=nodes_with_zero_degree[1:]
            continue       
        # select a random node that has deg > 1 and remove one of its edges
        random_node = random.SystemRandom().sample(G.nodes(), 1)[0]
        while G.degree([random_node])[random_node] <=1 or len(G.neighbors(random_node))<=1: 
            random_node = random.SystemRandom().sample(G.nodes(), 1)[0]            
        random_neighbor = random.SystemRandom().sample(G.neighbors(random_node), 1)[0]
        if G.degree([random_neighbor])[random_neighbor] <=1:
            continue # removing an edge from this neighbour will render it a singleton itself, start over
        G.remove_edge(random_node, random_neighbor)
    
        #select a random node and create an edge between it and the next nodes_with_zero_degree
        random_node = random.SystemRandom().sample(G.nodes(), 1)[0]
        if random.SystemRandom().sample([1,-1], 1)[0] == 1:
            G.add_edge(nodes_with_zero_degree[0], random_node) 
        else:
            G.add_edge(random_node, nodes_with_zero_degree[0]) 
        
        nodes_with_zero_degree=nodes_with_zero_degree[1:]
    
    # debugging --------------------------------------
    '''
    nodes_with_zero_degree = []
    for node in G.nodes():
        if G.degree([node])[node] == 0:
            nodes_with_zero_degree.append(node)
    print ("after: "+str(len(nodes_with_zero_degree))+" singletons")
    #-------------------------------------------------
    '''
    assert len(nodes_with_zero_degree)==0
    return G
#-----------------------------------------------------------------------
if __name__=="__main__":
    nodes, edges, outputfile = get_params()
    prob = edges/(nodes*nodes)
	
    G=nx.erdos_renyi_graph(nodes,prob,seed=None,directed=True)
    print ('First round: '+str(len(G.nodes()))+' nodes, '+str(len(G.edges()))+' edges')
    #trim off excess edges if any
    if len(G.edges()) > edges:
        print ('trimming off '+str(len(G.edges()) - edges)+' edges randomly')
        #randomly remove edges
        excess_edges  =  random.SystemRandom().sample(G.edges(),len(G.edges()) - edges ) 
        for e in excess_edges:
            G.remove_edge(e[0],e[1])
    #supplement extra edges if necessary
    elif len(G.edges()) < edges:
        print ('adding '+str( edges-len(G.edges()))+' more edges randomly')
        #randomly add edges
        while len(G.edges()) < edges:
            source = random.SystemRandom().sample(G.nodes(), (edges - len(G.edges())) )
            target = random.SystemRandom().sample(G.nodes(), (edges - len(G.edges())) )
            for [s,t] in zip (source, target):
                if [s,t] not in G.edges():
                    G.add_edge(s,t)
    #remove self loops if any
    self_loops=0
    for source, target in G.edges():
        if source == target:
            G.remove_edge(source, target)
            self_loops+=1
    print ("removed "+str(self_loops)+" self loops")      

    #if there are nodes with zero degree, take edges from nodes with highest degree and spread them on these singletons
    '''
    G, nodes_with_zero_degree = remove_singletons_systematically(G)
    while len(nodes_with_zero_degree):
        G, nodes_with_zero_degree = remove_singletons2(G)
    '''
    G = remove_singletons_randomly (G)
    
    
    out=open (outputfile,'w')
    out.write("source\ttarget\tsign\n")
    i=1
    for e in G.edges():
        #print(str(i)+' ',end='')
        i+=1
        temp = (list(e))
        out.write("N"+str(temp[0])+" "+"N"+str(temp[1])+" "+flip()+"\n")
    print ('\nDone: Erdos-Renyi graph, '+str(len(G.nodes()))+' nodes, '+str(len(G.edges()))+' edges, (prob='+str(prob)+'), created in file '+outputfile)
