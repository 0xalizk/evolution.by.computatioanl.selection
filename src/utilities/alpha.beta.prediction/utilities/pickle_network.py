import sys,os,pickle
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util, init

def usage():
    print('usage: python *py /path/to/edge/file.txt OR /path/to/dir/containing/edge_files \nExiting ..')
    sys.exit(1)

def pickleit(edge_file):
    
    M=None
    try:
        M = init.load_network ({'network_file':edge_file.strip(),'biased':False},undirected=False,quite=False)
    except:
        usage()
        
    with open (edge_file.strip().split('/')[-1].split('.')[0]+'.dump','wb') as file:
        pickle.dump(M,file)
    degrees = list(M.degree().values())
    count ={}
    for d in set(degrees):
        count[d] = degrees.count(d)/len(M.nodes())
    tmp = [(d,count[d]) for d in sorted(count.keys())]
    print (',\n\''+edge_file.split('/')[-1].split('.')[0]+'\':{')
    print ('\t\t\'deg\':'+ str([x[0] for x in tmp])+',')
    print ('\t\t\'freq\':'+ str([x[1] for x in tmp])+',')
    print ("\t\t\'edge2node\':" + str(len(M.edges())/len(M.nodes()))+',')
    print ("\t\t\'node2edge\':" + str(len(M.nodes())/len(M.edges()))+',')
    print ("\t\t\'edge2node_adj\':" + 'adj_largestC()[\'Bacteria\'][1]'+',')
    print ("\t\t\'node2edge_adj\':" + 'adj_largestC()[\'Bacteria\'][0]'+',')
    print ("\t\t\'edges\':" + str(len(M.edges()))+',')
    print ("\t\t\'nodes\':" + str(len(M.nodes())))
    print('}')
    #print ("str(sum(degrees)) = " + str(sum(degrees)))
    #print (str([x[1] for x in tmp]))

def batch_pickleit(dir):

    for root,dirs,files in os.walk(dir):
        for f in files:
            #print('='*50)
            pickleit(os.path.join(root,f))

if __name__ == '__main__':
    # individual file, provide a path to a single edge_file  
    if os.path.isfile(sys.argv[1]):
        pickleit(sys.argv[1]) 
    
    elif os.path.isdir(sys.argv[1]):
    # batch pickle it, provide a path to a dir containing all edge_files
        batch_pickleit(sys.argv[1])
    else:
        usage()
