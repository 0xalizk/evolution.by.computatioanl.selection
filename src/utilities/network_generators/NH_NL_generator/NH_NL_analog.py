import random,sys,os,math
import networkx as nx
sys.path.insert(0, os.getenv('lib'))
import init, pickle, os,utilv4 as util
import operator, numpy as np, random
R = random.SystemRandom().sample

########################################################
def getCommandLineArgs():
    paths = None
    try: 
        assert len(sys.argv) == 2
    except:
        print ("Usage: python3 NH_NL_analogs.py [/absolute/path/to/configs/input.txt] (containing paths to edge files)\nExiting..\n")
        sys.exit(1)
    paths = util.cleanPaths(sys.argv[1])
    try:
        for p in paths:
            assert os.path.isfile(p)
        return paths
    except:
        print ("Encountered invalid files, check your input \nExiting..\n")
        sys.exit(1)
########################################################
def ff(s):
    return str(s).ljust(10,' ')
########################################################
def fff(s):
    return str(s).ljust(20,' ')
########################################################
def writeout(M,name):
    writer = open(name,'w')
    writer.write('source target sign')
    for e in M.edges():
        sign = '+'
        if M[e[0]][e[1]]['sign'] == -1:
            sign='-'
        writer.write('\n'+e[0]+' '+e[1]+' '+sign)
########################################################
def crunch_stats(M, dict):
    dict['01 mind']    = min([d for d in M.degree().values() if d>0])
    dict['02 maxd']    = max([d for d in M.degree().values()])
    dict['03 mind_in'] = min([d for d in M.in_degree().values()])
    dict['04 mind_ou'] = min([d for d in M.out_degree().values()])
    dict['05 maxd_in'] = max([d for d in M.in_degree().values()])
    dict['06 maxd_ou'] = max([d for d in M.out_degree().values()])         
    dict['07 avgd_alive']    = math.ceil (np.average([M.degree(n) for n in M.nodes() if M.degree(n) >0 ]))
########################################################
def print_stats(dict):
    print(fff('\n\n\nstat')+fff('orig. network')+fff('altered'))
    before = dict['before']
    after  = dict['after']
    for key in sorted(before.keys()):
        print (fff(key.split()[1])+ff(before[key])+ff('==>')+ff(after[key]))  
########################################################
def adjacents (M, node): 
    suc = M.successors(node)
    pre = M.predecessors(node)  
    return [e for e in M.edges()   if (e[1] in suc and e[0]==node)   or  (e[0] in pre and e[1]==node)   ] 
########################################################
def swap(M, Edges, Nodes,quite=False,randomize_sign=True):
    i,k=0, 0
    while len(Edges) >= 1 and len(Nodes) >=1:
        # delete 1 edge
        sign = M[Edges[0][0]][Edges[0][1]]['sign']
        M.remove_edge(*Edges[0])
        del Edges[0]
        # add 1 edge
        j       = R(range(len(Nodes)), 1)[0]
        n1      = Nodes[j]
        del Nodes[j]
        n2 = None
        if len(Nodes)==0:
            n2 = R(M.nodes(), 1)[0]
            k += 1
        else:
            j       = R(range(len(Nodes)), 1)[0]
            n2      = Nodes[j]
            del Nodes[j]
            i+=1       
        if randomize_sign:
            sign       = R([1,-1], 1)[0]
        direction  = R([1,-1], 1)[0]
        if direction == 1:
            M.add_edge(n1, n2)
            M[n1][n2]['sign'] = sign
        else:
            M.add_edge(n2, n1)
            M[n2][n1]['sign'] = sign
    if not quite:
        print('swapped '+str(i)+' (in) '+str(k)+' (out)') 
########################################################       
def produce_NH(M,savename,quite=False):
        avgd = math.ceil(np.average(list(M.degree().values())))   
        while True: 
            mind  = min([d for d in M.degree().values() if d>0])
            maxd  = max(M.degree().values())
            dead  = [n for n in M.nodes() if M.degree(n)==0]
            alive = len(M.nodes())-len(dead)

            Hub   = R([key for key in M.degree().keys() if M.degree(key) == maxd], 1)[0]
            Leafs = [key for key in M.degree().keys() if M.degree(key) == mind]
            if not quite:
                print('alive '+ff(alive)+'dead '+ff(len(dead))+'maxd '+ff(maxd)+'mind '+ff(mind)+'Hub deg '+ff(M.degree(Hub))+'no. Leafs '+ff(len(Leafs)),end='')
    
            if maxd<=avgd:
                break

            Edges      = adjacents(M, Hub)           # edges
            swap(M, Edges, Leafs,quite=quite)

        writeout (M,savename)
########################################################               
def produce_NL(M,savename, quite=False):
    avgd = math.ceil(np.average(list(M.degree().values())))   
    while True: 
        mind  = min([d for d in M.degree().values() if d>0])
        maxd  = max(M.degree().values())
        dead  = [n for n in M.nodes() if M.degree(n)==0]
        alive = [n for n in M.nodes() if M.degree(n) >0]
        num_dead = len(dead)
        num_alive = len(M.nodes())-num_dead
        # kill dead
        #for node in dead:
        #    M.remove_node(node)

        Leafs   = [key for key in M.degree().keys() if M.degree(key) == mind]
        Hubs    = [key for key in M.degree().keys() if M.degree(key) >= avgd]
        
        if not quite:
            print('num_alive '+ff(num_alive)+'dead '+ff(num_dead), end='')
            print('maxd '+ff(maxd)+'mind '+ff(mind), end='')
            print('Leafs '+ff(len(Leafs))+'no Hubs '+ff(len(Hubs)), end='')
            print('current_avgd (alive) '+ff(math.ceil(np.average([M.degree(n) for n in alive]))),end='')
        if mind >=avgd:
            break
        Edges=[]
        for L in Leafs:
            Edges += adjacents(M, L)           # edges
        Edges = list(set(Edges))
        swap(M, Edges, Hubs,quite=quite)
    writeout (M,savename)
########################################################               
########################################################               
if __name__ == '__main__':
  
    networks    = getCommandLineArgs()
    analogs     = zip([util.slash('/'.join(n.split('/')[0:-1]))+'NH_'+n.split('/')[-1] for n in networks], [util.slash('/'.join(n.split('/')[0:-1]))+'NL_'+n.split('/')[-1]  for n in networks])
    for (netpath, savename) in zip(networks,analogs):
        M = init.load_network({'network_file':netpath,'biased':False},undirected=False,quite=False)
        stats = {'before':{}, 'after':{}}
        crunch_stats(M,stats['before'])
        
        print('='*50+' '+savename[0].split('/')[-1]+' '+'='*50)
        M1 = M.copy()
        produce_NH(M1, savename[0],quite=False)
        crunch_stats(M1,stats['after'])
        print_stats(stats)
        del M1
        
        print('='*50+' '+savename[1].split('/')[-1]+' '+'='*50)
        
        M2 = M.copy()
        produce_NL(M2,savename[1],quite=False)
        crunch_stats(M2,stats['after'])
        print_stats(stats)
        print('#'*115+'\n'+'#'*115)       
        
