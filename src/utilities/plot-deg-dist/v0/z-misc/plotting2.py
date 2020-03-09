import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
def plot_degree_distribution(wiki): 
    degs = {}
    for n in wiki.nodes():
        deg = wiki.degree(n) 
        if deg not in degs:
            degs[deg] = 0 
        degs[deg] += 1
    items = sorted(degs.items())

    
    items = sorted(degs.items())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([k for (k,v) in items], [v for (k,v) in items]) 
    
    ax.set_xscale('log') 
    ax.set_yscale('log')
    plt.title("Wikipedia Degree Distribution") 
    fig.savefig("degree_distribution.png")


plot_degree_distribution (nx.scale_free_graph(1000))