import os, sys,subprocess
#temp_agg.csv
#temp_by_gene.csv
def slash(path):
    return path+(path[-1] != '/')*'/'

collect = ['python3', slash(os.environ['util'])+'collect_files_by_name_pattern/collector-by-ORing-patterns.py',slash(os.environ['data']), 'temp_agg.csv', 'temp_by_gene.csv']
temp_files = (subprocess.Popen (collect, stdout=subprocess.PIPE, universal_newlines=True)).stdout.read()

if len (temp_files) >2:
    for f in temp_files.split('\n')[1:-2]:#skipt first and last lines
        result = (subprocess.Popen (['rm',f], stdout=subprocess.PIPE, universal_newlines=True)).stdout.read()
        if len(result)==0:
            print ("deleted: "+f)
        else:
            print ("failed: "+f)
