import os,sys

#assert len (sys.argv) >=3

try:
    root_directory  = str(sys.argv[1])
    pattern = [str(p) for p in sys.argv[2:] ]
except:
    print ('Usage: collectp [root_dir_to_crawl] [space-seperated patterns to look for in file names, if non provided all files will be listed] \nExiting...')
    sys.exit(1)
matches = []
for root, dirs, files in os.walk(root_directory):
   for name in dirs:
        chop = (os.path.join(root,name)).split('/')
        final=[]
        for i in range(len(chop)):
            final=final+[c for c in chop[i].split('_')]
            final=final+[c for c in chop[i].split('.')]
        matched=True
        for p in pattern:
            if not (p in final):
                matched=False
                break
        if (matched):
            matches.append(os.path.join(root,name))


for m in sorted(matches):
    print (m)
