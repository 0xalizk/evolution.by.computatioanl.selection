import sys, os, networkx as nx
sys.path.insert(0, os.getenv('lib'))
import init, utilv4 as util
myprint = util.myprint
def getCommandLineArgs():
    if len(sys.argv) < 2:
        myprint ("Usage: python3 networks_intersection.py [/absolute/path/to/input.txt containing paths to edge files]\nExiting..\n")
        sys.exit()
    assert os.path.isfile(str(sys.argv[1]))
    return  util.cleanPaths(str(sys.argv[1]))


edge_files, Ms = getCommandLineArgs(), {} 

myprint ('loading networks:  ')
for line in edge_files: 
    randomize, net = line.strip().split()[0], line.strip().split()[1]
    myprint('\t'+str(net.split('/')[-1])+',  ')
    Ms[net]              = {}
    Ms[net]['nx']        = init.load_network({'network_file':net,'biased':False}, undirected=(randomize=='True'), quite=True)
    Ms[net]['undirected'] = (randomize=='True')

myprint ('\nDone. \n\ncomparing networks ..\n')
compared_already=[]
for M1 in sorted(Ms.keys()):
    for M2 in sorted(Ms.keys()):
        if M1 != M2 and (M1,M2) not in compared_already and (M2,M1) not in compared_already:
            # 10 case, we always compare  [  'undir'  to  ('undir.' OR 'dir')  ]    OR   [  'dir'  to  'dir'  ] ... we do not compare 'dir'  
            if not Ms[M1]['undirected'] and Ms[M2]['undirected']:
                continue # we'll compare M2 to M1 in a subsequent iterations
            
            intersection = 0
            myprint(M1.split('/')[-1][0:min(18,len(M1.split('/')[-1]))]+'('+str(len(Ms[M1]['nx'].edges()))+' edges, '+'un'*(Ms[M1]['undirected'])+'directed)'+'     vs     '+M2.split('/')[-1][0:min(18,len(M2.split('/')[-1]))]+'('+str(len(Ms[M2]['nx'].edges()))+' edges, '+'un'*(Ms[M2]['undirected'])+'directed): ')
            
            
            # 00, and 01 cases
            if Ms[M1]['undirected']:# and Ms[M2]['undirected']:
                for e in Ms[M1]['nx'].edges():
                    if (e[0],e[1]) in Ms[M2]['nx'].edges() or (e[1],e[0]) in Ms[M2]['nx'].edges():
                        intersection+=1
            # 11 case
            else:
                assert not Ms[M1]['undirected'] and not Ms[M2]['undirected']
                for e in Ms[M1]['nx'].edges():
                    if (e[0],e[1]) in Ms[M2]['nx'].edges():
                        intersection+=1
                    
            
            compared_already.append((M1,M2))

            myprint(str(intersection).rjust(28,' ')+' common edges\n')

