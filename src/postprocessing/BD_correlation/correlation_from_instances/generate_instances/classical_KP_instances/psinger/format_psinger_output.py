import sys
def getCommandLineArg():
    try:
        input_file  = str(sys.argv[1])
    except:
        print ('Usage: python3 *.py [input-file (psinger_instance.txt)] \nExiting...')
        sys.exit(1)
    return input_file

input =  getCommandLineArg()
file = open (input,'r').readlines()[1:-1]#ignore first and last line
logger = open (input.split('/')[-1].split('.')[0]+'_formated.txt','w')
Bs=[]
Ds=[]
for line in file:
    Bs.append (line.strip().split()[1])
    Ds.append (line.strip().split()[2])
for b in Bs:
    logger.write(str(b)+' ')
logger.write('\n')
for d in Ds:
    logger.write(str(d)+' ')
print ("done: "+input.split('/')[-1].split('.')[0]+'_formated.txt')
