import sys, os, random
#######################################################################################
def realp(path):
    path=path.strip()
    Ds,i = path.split('/'),0
    for d in Ds:
        if len(d.split('$'))>1:
            d = d.split('$')
            d[1]=os.getenv(d[1])
            if d[1]==None:
                d[1]='***UNRECOGNIZED-ENV-VAR***'
            Ds[i]='/'.join(d).replace('//','/')
        i+=1
    path='/'.join(Ds).replace('//','/')
    return os.path.realpath(path) # turns relative to absolute
#######################################################################################
def savedivision(n,d):
    if d==0:
        return n
    return n/d
#######################################################################################
def cleanLines(path):
    # ignore empty lines
    # ignore lines beginning with '#'
    # ignore lines enclosed by @ .. @
    clean = []
    LINES = open(path,'r').readlines()
    inside_comment = False
    for i in range(len(LINES)): 
        line = LINES[i].strip()
        if len(line)==0:
            continue
        if inside_comment:
            if line[0] == '@':
                inside_comment = False
        else:
            if line[0]=='@':
                inside_comment = True
                continue
            if line[0]!='#':
                clean.append(line)
    return clean
#######################################################################################
def cleanPaths(path):
    # ignore empty lines
    # ignore lines beginning with '#'
    # ignore lines enclosed by @ .. @
    # replaces $env_var with the actual value 
    # turns relative to abolute path
    clean = []
    LINES = open(path,'r').readlines()
    inside_comment = False
    for i in range(len(LINES)): 
        line = LINES[i].strip()
        if len(line)==0:
            continue
        if inside_comment:
            if line[0] == '@':
                inside_comment = False
        else:
            if line[0]=='@':
                inside_comment = True
                continue
            if line[0]!='#':
                clean.append(line)
    clean = [realp(path) for path in clean]
    return clean
#######################################################################################
def myprint(s):
    sys.stdout.write(s)
    sys.stdout.flush()
#######################################################################################
def mywrite(f,s):
    myprint(s)
    reporter = open (f, 'a')
    reporter.write(s)
    reporter.flush()
    reporter.close()
#######################################################################################
def mylog(f,s):
    reporter = open (f, 'a')
    reporter.write(s)
    reporter.flush()
    reporter.close()
#######################################################################################
#--------------------------------------------------------------------------------------------------
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 simulator_v4.py [/absolute/path/to/configs/file.txt]\nExiting..\n")
        sys.exit()
    return [str(sys.argv[0]), str(sys.argv[1])]
#----------------------------------------------------------------------------  
def slash(path):
    return path+(path[-1] != '/')*'/'
#--------------------------------------------------------------------------------------------------
def flip():
    return random.SystemRandom().choice([1,-1])
#--------------------------------------------------------------------------------------------------
def sample_p_elements (elements,p):
    #elements = nodes or edges
    return  random.SystemRandom().sample(elements,p) 
#--------------------------------------------------------------------------------------------------
def advice_nodes (M, sample_nodes, biased):
    advice = {}
    if not biased:
        for node in sample_nodes: 
            advice[node]=flip()
    else:
        for node in sample_nodes:
            biased_center       = 0.5 + M.node[node]['conservation_score']
            rand                = random.SystemRandom().uniform(0,1)
            if rand <= biased_center:
                advice[node] = 1    #should be promoted (regulation) or conserved (evolution)
            else:
                advice[node] = -1   #should be inhibited (regulation) or deleted (evolution)
    
    return advice
#--------------------------------------------------------------------------------------------------  
def advice_edges (M, sample_edges, biased):
    advice = {}
    if not biased:
        for e in sample_edges: 
            advice[e]=flip()
    else:
        for e in sample_edges:
            biased_center       = 0.5 +  M[e[0]][e[1]]['conservation_score']
            rand                = random.SystemRandom().uniform(0,1) # in [0,1)
            if rand <= biased_center:
                advice[e] = M[e[0]][e[1]]['sign']      # Oracle agrees with the effect of this interaction (be it promotional or inhibitory)
            else:
                advice[e] = M[e[0]][e[1]]['sign'] * -1 # advice is the opposite of sign, Oracle disagrees
    return advice
#--------------------------------------------------------------------------------------------------
