import os,sys
##################################################################
def getCLA():
    try: #assert len (sys.argv) >=3
        root_directory  = str(sys.argv[1])
        patterns = [str(p) for p in sys.argv[2:] ]
    except:
        print ('Usage: python3 collector.py [root_dir_to_crawl] [space-seperated patterns to look for in file names, if non provided all files will be listed] \nExiting...')
        sys.exit(1)
    return [patterns, root_directory]
##################################################################
def get_matches(patterns, root_directory):
    matches = []
    for root, dirs, files in os.walk(root_directory):
        for name in files:
            matched=True
            for p in patterns:
                #chop = [x for x in name.split('/')[-1].split('_')] + [name.split('.')[-1]]
                #if not (p in chop):
                if p not in name:
                    matched=False
                    break
            if (matched):
                matches.append(os.path.join(root,name))
    return matches
##################################################################
if __name__ == "__main__":
    args = getCLA()
    patterns, root_directory = args[0], args[1] 
    m = get_matches(patterns, root_directory)
    for line in sorted(m):
        print (line)
