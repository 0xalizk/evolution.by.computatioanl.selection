import os,sys

#assert len (sys.argv) >=3
try:
    root_directory  = str(sys.argv[1])
    pattern = [str(p) for p in sys.argv[2:] ]
except:
    print ('Usage: python3 collector.py [root_dir_to_crawl] [space-seperated patterns to look for in file names, if non provided all files will be listed] \nExiting...')
    sys.exit(1)
print (pattern)
matches = []
for root, dirs, files in os.walk(root_directory):
    for name in files:
        matched=False
        for p in pattern:
            if p in str(name):
                matched=True
                break
        if (matched):
            matches.append(os.path.join(root,name))


for m in matches:
    print (m)
print ("done") 
