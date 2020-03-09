import sys, os, networkx as nx, numpy as np
sys.path.insert(0, os.getenv('lib'))
import init, utilv4 as util
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 max_degree.py [/absolute/path/to/configs/edge_fil.txt]\nExiting..\n")
        sys.exit()
    assert os.path.isfile(str(sys.argv[1]))
    return  util.cleanPaths(str(sys.argv[1]))



input = getCommandLineArgs() 
for line in input: 
    configs ={}  
    randomize, configs['network_file'], configs['biased'] = line.split()[0], line.split()[1].strip(), False    
    
    print('='*100+len(  line.split()[1].split('/')[-1]  )*'=')
    print(' '*40 +line.split()[1].split('/')[-1]+' ('+((randomize=='True')*'un')+'directed)'+' '*43)
    print('='*100+len(  line.split()[1].split('/')[-1]  )*'=')
    
    undirected = (randomize=='True')  # randomize edge direction in the newly created largest component
    M = init.load_network(configs,undirected=undirected,quite=False)

    ind = max(M.out_degree().values())
    oud = max(M.in_degree().values())
    d   = max(M.degree().values())

    promotional=0.0
    inhibitory=0.0
    for e in M.edges():
        if(  M[e[0]][e[1]]['sign']) ==1:
            promotional+=1
        elif (  M[e[0]][e[1]]['sign']) ==-1:
            inhibitory+=1
        else:
            print("I don't recognized this sign: "+str(M[e[0]][e[1]]['sign']))
    total=float(promotional+inhibitory)
    try:
        assert total==len(M.edges())
    except:
        print ("Warning: not all edges are signed")

    percent_p = round(((promotional/total)*100), 3)
    percent_i = round(((inhibitory/total)*100), 3)
    print ("\n\nNodes ".ljust(25)+str(len(M.nodes())))
    print ("Edges ".ljust(25)+str(len(M.edges())))
    print ("Promotional edges ".ljust(25)+str(percent_p)+' %')
    print ("Inhibitory edges  ".ljust(25)+str(percent_i)+' %')
    print ("max(in degree)".ljust(25)+str(ind))
    print ("max(ou degree)".ljust(25)+str(oud))
    print ("max(   degree)".ljust(25)+str(d))
    print ("Average degree = "+str(np.average(list(M.degree().values()))))
    print ("Average set(degree) = "+str(np.average(list(set(M.degree().values())))))
    components=sorted(nx.connected_components(M.to_undirected()), key = len, reverse=True)
    print ("no. connected components: "+str(len(components)))
    print ("component sizes: "+str([len(c) for c in components]))
    commulative_p, commulative_c=0,0
    print('')
    for d in sorted(set(M.degree().values())):
        percent=(len([n for n in M.nodes() if M.degree(n)==d])/len(M.nodes()))*100
        commulative_p+=percent
        count = len([n for n in M.nodes() if M.degree(n)==d])
        commulative_c+=count
        print("Nodes of degree: "+str(d).ljust(5,' ')+str(count).ljust(5,' ')+' nodes  (commulative '+str(commulative_c)+' nodes)'.ljust(20, ' ')+' ==>   '+str(round(percent,4)).ljust(8,' ')+' %   (commulative = '+str(commulative_p)+' %)')
        #print ("no. connected components: "+str(nx.number_connected_components(M.to_undirected())))
