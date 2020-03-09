import sys, os, networkx as nx
sys.path.insert(0, os.getenv('lib'))
import init, utilv4 as util
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 extract_largest_component.py [/absolute/path/to/input_file.txt]\nEach line in input file should be [True/False] [/path/to/edge/file] where True/False means to randomize edges or not (if the network is undirected, set it to True)\nExiting..\n")
        sys.exit()
    assert os.path.isfile(str(sys.argv[1]))
    return  util.cleanPaths(str(sys.argv[1]))

input = getCommandLineArgs() 

for line in input: 
    if line[0] == '#':
        continue
    configs ={}    
    randomize, configs['network_file'], configs['biased'] = line.split()[0], line.split()[1].strip(), False    
    undirected = (randomize=='True')  # randomize edge direction in the newly created largest component
    print ("#"*40 + "  "+configs['network_file'].split('/')[-1]+ ' ('+((randomize=='True')*'un')+'directed) '+'#'*40)
    
    M = init.load_network(configs,undirected=undirected,quite=False)
    components=sorted(nx.connected_components(M.to_undirected()), key = len, reverse=True)
    if undirected:
        print ("*************** The edges in the newly created largest component will be RANDOMIZED (change undirected=False if you want otherwise) *********")
        print ("*************** This is because I'm assuming the network is undirected unless otherwise specified *********\n")
    print ("no. connected components: "+str(len(components)))
    print ("component sizes: "+str([len(c) for c in components]))

    delete_nodes = []
    for c in components[1:]:
        delete_nodes += [n for n in c]
    nodes_before = len(M.nodes())
    edges_before = len(M.edges())
    M.remove_nodes_from(delete_nodes)
    nodes_after = len(M.nodes())
    edges_after = len(M.edges())
    print ("M.nodes() before ".ljust(30,' ')+str(nodes_before))
    print ("M.edges() before ".ljust(30,' ')+str(edges_before))
    print ("len(delete_nodes): ".ljust(30,' ')+str(len(delete_nodes)))
    print ("len(set(delete_nodes)): ".ljust(30,' ')+str(len(set(delete_nodes))))
    print ("M.nodes() after ".ljust(30,' ')+str(nodes_after))
    print ("M.edges() after ".ljust(30,' ')+str(edges_after))

    out = open ('/'.join(configs['network_file'].split('/')[:-1]) + '/' + '.'.join(configs['network_file'].split('/')[-1].split('.')[:-1])+'_'+((randomize=='True')*'un')+'directed_largest_component.txt', 'w')
    out.write('source target sign')
    for e in M.edges():
        sign = M[e[0]] [e[1]]['sign']
        if int(sign) == -1:
            sign = '-'
        elif int(sign) == 1:
            sign = '+'
        else:
            print('I dont recognize this sign '+str(sign)+'\nExiting')
            sys.exit(1)
        
        out.write('\n'+e[0]+' '+e[1]+' '+sign)
    print('\nwritten: '+'/'.join(configs['network_file'].split('/')[:-1]) + '/' + '.'.join(configs['network_file'].split('/')[-1].split('.')[:-1])+'_'+((randomize=='True')*'un')+'directed_largest_component.txt')
    print('')
    
    
