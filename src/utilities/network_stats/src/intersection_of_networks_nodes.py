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


whole_set=[]
edge_files, Ms = getCommandLineArgs(), {}

for path in edge_files:
    randomize, net = path.strip().split()[0], path.strip().split()[1]
    Ms[net]              = {}
    lines = open(net,'r').readlines()
    
    for interaction in lines:
        interaction    = interaction.strip().split()
        source,target  = interaction[0].strip().upper(),interaction[1].strip().upper()

        Ms[net][source], Ms[net][target] = None, None
        whole_set = whole_set + [source,target]
        whole_set = list(set(whole_set))

for key in Ms.keys():
    print(str(len(Ms[key].keys())))
print('whole set: '+str(len(whole_set)))
myprint ('\ncomparing networks ..\n')
compared_already=[]

for M1 in Ms.keys():
    for M2 in Ms.keys():
        if M1 != M2 and (M1,M2) not in compared_already and (M2,M1) not in compared_already:

            intersection = 0
            myprint( M1.split('/')[-1][0:min(18,len(M1.split('/')[-1]))].ljust(20,' ')+' ('+str(len(Ms[M1].keys())).ljust(10,' ')+' nodes)'\
                     +'     vs     '+\
                     M2.split('/')[-1][0:min(18,len(M2.split('/')[-1]))].ljust(20,' ')+' ('+str(len(Ms[M2].keys())).ljust(10,' ')+' nodes)')

            if len(Ms[M1].keys())>=len(Ms[M2].keys()): 
                intersection = len([n for n in Ms[M2].keys()  if n in Ms[M1].keys()])
            else:
                intersection = len([n for n in Ms[M1].keys()  if n in Ms[M2].keys()])

            
            compared_already.append((M1,M2))
            myprint(str(intersection).rjust(28,' ')+' common nodes\n')