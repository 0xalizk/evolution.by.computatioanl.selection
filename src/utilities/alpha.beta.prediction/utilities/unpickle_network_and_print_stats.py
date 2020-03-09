import sys,os,pickle
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, init

def usage():
    print('usage: python *py /path/to/edge/file.txt OR /path/to/dir/containing/edge_files \nExiting ..')
    sys.exit(1)

def unpickleit(edge_file):
    
    M=None
    try:
        with open(edge_file,'rb') as f:
            M=pickle.load(f)
    except:
        usage()
    
    degrees = list(M.degree().values())
    count ={}
    for d in set(degrees):
        count[d] = degrees.count(d)/len(M.nodes())
    tmp = [(d,count[d]) for d in count.keys()]
    print (',\n\''+edge_file.split('/')[-1].split('.')[0]+'\':{')
    print ('\t\t\'deg\':'+ str([x[0] for x in tmp])+',')
    print ('\t\t\'freq\':'+ str([x[1] for x in tmp])+',')
    print ("\t\t\'edge2node\':" + str(len(M.edges())/len(M.nodes()))+',')
    print ("\t\t\'node2edge\':" + str(len(M.nodes())/len(M.edges()))+',')
    print ("\t\t\'edge2node_adj\':" + 'adj_largestC()[\'Bacteria\'][1]'+',')
    print ("\t\t\'node2edge_adj\':" + 'adj_largestC()[\'Bacteria\'][0]'+',')
    print ("\t\t\'edges\':" + str(len(M.edges()))+',')
    print ("\t\t\'nodes\':"  + str(len(M.nodes())))
    print('}')
    
def batch_unpickleit(dir):

    for root,dirs,files in os.walk(dir):
        for f in files:
            #print('#'*50)
            unpickleit(os.path.join(root,f))

if __name__ == '__main__':
    # individual file, provide a path to a single edge_file  
    if os.path.isfile(sys.argv[1]):
        unpickleit(sys.argv[1]) 
    
    elif os.path.isdir(sys.argv[1]):
    # batch pickle it, provide a path to a dir containing all edge_files
        batch_unpickleit(sys.argv[1])
    else:
        usage()