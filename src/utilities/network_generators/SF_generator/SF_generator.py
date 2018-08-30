import networkx as nx

N = 6704
E = 12184

#M = nx.scale_free_graph(N, alpha=0.41, beta=0.54, gamma=0.05, delta_in=0.2, delta_out=0, create_using=None, seed=None)
#with open ('pickled.dump','wb') as f:
#    import pickle
#    pickle.dump(M,f)

print('loading ..',end='')
with open ('pickled.dump','rb') as f:
    import pickle
    M = pickle.load(f)
print('done')

with open ('SF_6704.txt','w') as f:
    f.write('source target')
    for e in set(M.edges()):# no duplicate edges
        if e[0]!=e[1]: #no self loops
            f.write('\n'+str(e[0])+' '+str(e[1]))

print (str(len(M.edges())/len(M.nodes())))
