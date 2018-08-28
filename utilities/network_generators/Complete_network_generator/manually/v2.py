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
    node_list = list (range(nodes)) 
    out=open (outputfile,'w')
    out.write("source\ttarget\tsign\n")
    direction =0
    sign ='+'
    edge_counter=0
    for i1 in range (len(node_list)):
        for i2 in range (i1+1,len(node_list),1):
            edge_counter+=1
            if direction == 0:
                out.write("N"+str(i1)+" "+"N"+str(i2)+" "+sign+"\n")
                direction=1
            else:
                out.write("N"+str(i2)+" "+"N"+str(i1)+" "+sign+"\n")
                direction =0
            if sign =='+':
                sign='-'
            else:
                sign='+'
    print ('Done: Complete directed-signed graph, '+str(nodes)+ ' nodes,'+str(edge_counter)+' edges, created in file '+outputfile)
