import random,sys,os,math
import networkx as nx
sys.path.insert(0, os.getenv('lib'))
import init, utilv4 as util
realp   = os.path.realpath
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 deform.py [/absolute/path/to/input_file.txt (containing paths edge files)] \nExiting..\n")
        sys.exit()
    return  util.cleanPaths(realp(sys.argv[1]))

input = getCommandLineArgs() 
for edge_file in input:

    temp = [1]#[.1, .25, .50, 1] # 1 ==> randomize 100% of edges

    for deforming_temp in temp:
    
        M = init.load_network({'network_file':edge_file, 'biased':False}, undirected=False, quite=False)
        print (edge_file.split('/')[-1]+": "+str(len(M.nodes()))+" nodes "+str(len(M.edges()))+" edges ",end='')
        number_of_edges_to_swap = math.ceil(deforming_temp*len(M.edges()))
    
        for i in range(number_of_edges_to_swap):
            source, target = random.SystemRandom().choice(M.edges()) # pick a random edge
            M.remove_edge(source,target)
        i=0
        while i < number_of_edges_to_swap:
            source = random.SystemRandom().choice(M.nodes()) # pick a random source
            target = random.SystemRandom().choice(M.nodes()) # pick a random target
            sign   = random.SystemRandom().choice(['+','-']) # do we wanna randomize the sign? yes
            if (source,target) not in M.edges():
                M.add_edge(source, target, sign=sign)
                i+=1
        
        savepath = util.slash('/'.join(edge_file.split('/')[0:-1])) + 'RN_'+edge_file.split('/')[-1]
        writer = open (savepath,'w')
        writer.write('source target sign')
        for source, target in M.edges():
            sign = str(M[source][target]['sign'])
        
            if sign != '+' and sign != '-':
                if int(sign) == 1:
                    sign = '+'
                elif int(sign) == -1:
                    sign = '-' 
                else:
                    print ("FATAL: I don't recognize this sign "+str(sign)+'\nExiting....')
                    sys.exit(1)
        
            writer.write('\n'+str(source)+' '+(target)+' '+sign)
        
        print ('==>  '+savepath.split('/')[-1]+": "+str(len(M.nodes()))+" nodes "+str(len(M.edges()))+" edges ")
        print ("saved: "+savepath)
    
