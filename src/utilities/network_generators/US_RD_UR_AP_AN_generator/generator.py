import sys, os
sys.path.insert(0, os.getenv('lib'))
import init
def f(s):
    return s.ljust(max(15, len(s)+1), ' ')
def check(M):
    for e in M.edges():
        if M[e[0]][e[1]]['sign'] != 1 and M[e[0]][e[1]]['sign'] != -1:
            print ("hmmm .. this doesn't seem to be a signed network (sign = "+str(M[e[0]][e[1]]['sign'])+"), \nExiting\n")
            sys.exit(1)
        
M, original    = None, None
try:
    original = os.path.abspath(sys.argv[1].strip())
    assert os.path.isfile(original)
    M    = init.load_network({'network_file':original, 'biased':False})
except:
    print ('\nUsage: generator.py [/absolute/path/to/original_network/edge_file.txt]\nExiting...\n\n')
    sys.exit(1)

check (M)

name              = original.split('/')[-1].split('.')[0]
original          = open(      name+'.txt','w')
US_original       = open('US_'+name+'.txt','w')
RD_original       = open('RD_'+name+'.txt','w')
UR_original       = open('UR_'+name+'.txt','w')
AP_original       = open('AP_'+name+'.txt','w') # all positive signs
AN_original       = open('AN_'+name+'.txt','w') # all negative signs


original.write   (f('source')+f('target')+' sign\n')
US_original.write(f('source')+ 'target\n')
RD_original.write(f('target')+f('source')+' sign\n')
UR_original.write(f('target')+'source\n')
AP_original.write   (f('source')+f('target')+' sign\n')
AN_original.write   (f('source')+f('target')+' sign\n')

for e in M.edges():
    
    source, target= e[0].strip(), e[1].strip() 
    sign = M[source][target]['sign']
    if sign == 1:
        sign = '+'
    else:
        sign = '-'
    original.write    (f(source) + f(target) + ' '+sign+'\n')
    US_original.write (f(source) + f(target)          +'\n')  
    RD_original.write (f(target) + f(source) + ' '+sign+'\n')
    UR_original.write (f(target) + f(source)          +'\n')
    AP_original.write (f(source) + f(target) + ' '+'+'+'\n')
    AN_original.write (f(source) + f(target) + ' '+'-'+'\n')
print ('done')
