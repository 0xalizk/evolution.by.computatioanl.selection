import os, sys, subprocess as sp
#-------------------------------------------------
def getCommandLineArgs():
    if len(sys.argv) < 2:
        print ("Usage: python3 batch_processor.py [/absolute/path/to/script_file.txt]\nExiting..\n")
        sys.exit()
    return str(sys.argv[1])
#-------------------------------------------------
#-------------------------------------------------
if __name__ == "__main__":
    input = getCommandLineArgs()
    arguments = (open (input, 'r')).readlines()
    #call script on each argument
    for command in arguments:
        command = [arg for arg in (command.split())] #Popen needs script/args as a list 
        output   = (sp.Popen (command, stdout=sp.PIPE, universal_newlines=True)).stdout.read()
        print (output)
