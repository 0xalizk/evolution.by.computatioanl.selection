import networkx as nx, random, os, sys

def flip_sign():
    ran = random.SystemRandom()
    if(ran.random() > 0.5): 
        return "+"	
    else: 
        return "-"
def flip_direction(n1,n2):
    return random.SystemRandom().choice( [[n1,n2],[n2,n1]])

def get_params():
    if len(sys.argv)<3:
        print ('Usage: python generate.py [no. nodes] [absolute_path_to_output_file]\nExiting ..\n')
        sys.exit(1)
    else:
        return int(str(sys.argv[1])), str(sys.argv[2])

if __name__=="__main__":
    nodes, outputfile = get_params()
    G=nx.Graph()
    G.add_nodes_from(range(nodes))
    node_list = sorted(G.nodes())
    print ('node_list '+str(len(node_list)))
    out=open (outputfile,'w')
    out.write("source\ttarget\tsign\n")
    for i1 in range (len(node_list)):
        for i2 in range (i1+1,len(node_list),1):
            print (str(i1)+'-'+str(i2))
            G.add_edge(node_list[i1],node_list[i2])
    for e in G.edges():
        temp=list(e)    
        direction = flip_direction(temp[0],temp[1])
        out.write("N"+str(direction[0])+" "+"N"+str(direction[1])+" "+flip_sign()+"\n")
    print ('Done: Complete directed-signed graph, '+str(len(G.nodes()))+ ' nodes,'+str(len(G.edges()))+' edges, created in file '+outputfile)
