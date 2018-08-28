import sys, os,subprocess
local_dir = str(os.getcwd())
remote_files = (open (str(sys.argv[1]),'r')).readlines()
print ('Downloading: '+str(len(remote_files))+' files')
i=1
for file in remote_files:
    file = file.strip()
    command = ["scp","mosha@guillimin.hpc.mcgill.ca:"+file, local_dir+'/'+str(i)+'_'+file.split('/')[-1]]    
    result   = (subprocess.Popen (command, stdout=subprocess.PIPE, universal_newlines=True)).stdout.read()
    print (str(i)+" "+result)
    sys.stdout.flush()
    i+=1

