import networkx as nx, random, os, sys

def flip():
	ran = random.SystemRandom()
	if(ran.random() > 0.5): 
		return "+"	
	else: 
		return "-"

def get_params():
	if len(sys.argv)<3:
		print ('Usage: python generate.py [no. nodes] [absolute_path_to_output_file]\nExiting ..\n')
		sys.exit(1)
	else:
		return int(str(sys.argv[1])), str(sys.argv[2])

if __name__=="__main__":
    nodes, outputfile = get_params()
    G=nx.complete_graph(nodes)
    out=open (outputfile,'w')
    out.write("source\ttarget\tsign\n")
    for e in G.edges():
        temp = (list(e))
        out.write("N"+str(temp[0])+" "+"N"+str(temp[1])+" "+flip()+"\n")
    print ('Done: Complete directed-signed graph, '+str(len(G.nodes()))+ ' nodes, created in file '+outputfile)
