import sys, os, networkx as nx
sys.path.insert(0, os.getenv('lib'))
import init, utilv4 as util
myprint = util.myprint
def getCommandLineArgs():
    if len(sys.argv) < 2:
        myprint ("Usage: python3 extract_nodes.py [/absolute/path/to/input.txt containing paths to edge files]\nExiting..\n")
        sys.exit()
    assert os.path.isfile(str(sys.argv[1]))
    return  util.cleanPaths(str(sys.argv[1]))



edge_files = getCommandLineArgs()

for path in edge_files:
    source_set, target_set = [], []
    randomize, net = path.strip().split()[0], path.strip().split()[1]
    lines = open(net,'r').readlines()

    print('='*100+len(  path.split()[1].split('/')[-1]  )*'=')
    print(' '*40 +path.split()[1].split('/')[-1]+' ('+str(len(lines))+' lines)'+' '*40)
    print('='*100+len(  path.split()[1].split('/')[-1]  )*'=')
    
    for interaction in lines:
        interaction    = interaction.strip().split()
        source,target  = interaction[0].strip().upper(),interaction[1].strip().upper()
        source_set  +=  [source]
        target_set  +=  [target]
    source_set, target_set = set(source_set), set(target_set)
    overall_set            = set(list(source_set)+list(target_set))

    #print('source_set    ('+str(len(source_set))+')  = '+str(list(source_set) [0:min(200,len(source_set))]))
    #print('\ntarget_set  ('+str(len(target_set))+')  = '+str(list(target_set) [0:min(200,len(target_set))]))
    #print('\noverall_set ('+str(len(overall_set))+') = '+str(list(overall_set)[0:min(200,len(overall_set))]))
    #print('\nNote: only the first 200 genes are printed ')

    print('source_set    ('+str(len(source_set))+')  = '+str(list(source_set)))
    print('\ntarget_set  ('+str(len(target_set))+')  = '+str(list(target_set)))
    print('\noverall_set ('+str(len(overall_set))+') = '+str(list(overall_set)))

