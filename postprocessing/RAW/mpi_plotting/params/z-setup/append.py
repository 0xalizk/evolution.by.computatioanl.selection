import os, sys

def usage():
    print ("Usage: python append.py [/abs/path/to/append.txt]\nExiting ..\n")
    sys.exit(1)
def getCommandLineArgs():
    try:
        return os.path.abspath(sys.argv[1])
    except:
        usage()
        
line = open (getCommandLineArgs(), 'r')

signal      = [] # 0 = continue reading, 1 = flush
new_content = []
files       = []
next_in     = None
done        = False
while not done:
    try:
        next_in = next(line)
    except:
        done = True
    if not done: 
        if next_in[0] == '<':
            signal.append(0)
            new_content.append(next_in.replace('<',''))
        elif next_in[0] == '>':
            signal.append(1)
            files.append (next_in.replace('>','').strip())
        else: # ignore lines not beginning with '>' or '<'
            continue
    
    if (len(signal)>1 and signal[-1]==0 and signal[-2]==1) or done: #time to write
        for f in files:
            
            previous_content = open (f,'r').readlines()
            writer           = open (f,'w')
            if done:
                for c in new_content:
                    writer.write(c)
            else:
                for c in new_content[:-1]:
                    writer.write(c)
            for c in previous_content:
                writer.write(c)
        print ('writing\t'+str(f))
        signal, new_content, files, next_in  = [signal[-1]], [new_content[-1]], [], None

print ('Done')
