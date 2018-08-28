import sys, os
version = 'v4'
data_dir = os.environ.get ("scratch")
#version='v2'
#data_dir = os.environ.get ("data")
assert data_dir != ""
print ("\t\tcrawling "+data_dir+"\tversion "+version+'\n')
for root, dirs, files in os.walk(data_dir):
    for f in files:
        if str(f) =='progress.dat':
            #[item for sublist in l for item in sublist]
            geneology = [token for d in root.split('/') for token in d.split('_')]
            if version in geneology:
                progfile = open(os.path.join(root,f),'r')
                progress = (progfile).readlines()
                if len(progress)>0:
                    progress = progress[-1].strip()
                    d =  (os.path.join(root,f)).split("/")
                    print (progress.ljust(14, ' ')+"/".join(d[-6:]))
                else:
                    d =  (os.path.join(root,f)).split("/")
                    print ('?'.ljust(14, ' ')+"/".join(d[-6:]))
                progfile.close()
