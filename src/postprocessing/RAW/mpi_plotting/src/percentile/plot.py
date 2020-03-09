import os, sys
from sys import platform
import matplotlib as mpl
if platform == "linux" or platform == "linux2":
    mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
######################################
def f(num):
    return "{0:.2f}".format(num)
######################################
def formatter_x(x, y):
    #if x<=0:
    #    return ""
    return str(int(x)+" %") 
######################################
def update_rcParams():
    rcParams['savefig.pad_inches'] = .2

    rcParams['axes.grid']          = True
    rcParams['axes.titlesize']     = 36
    rcParams['axes.labelsize']     = 10

    rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
    rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

    rcParams['figure.titleweight']    = 'bold'
    rcParams['figure.titlesize']      = 45 
    rcParams['figure.subplot.hspace'] = 0.2
    rcParams['figure.subplot.wspace'] = 0.1  #wspace: horizental space between subplots on the same row
    rcParams['figure.subplot.left']   = 0.1
    rcParams['figure.subplot.right']  = 0.9
    rcParams['figure.subplot.top']    = 0.9 # create a space between title and subplots
    rcParams['figure.subplot.bottom'] = 0.1

    rcParams['grid.alpha']         =  .7
    rcParams['grid.color']         =  '#63cae9'
    rcParams['grid.linestyle']     =  'solid' # dashed solid dashdot dotted
    rcParams['grid.linewidth']     =  0.5
    rcParams['axes.grid.axis']     =  'both'
    rcParams['axes.grid.which']    =  'major'


    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  6
    rcParams['xtick.major.pad']    =  4.0
    rcParams['xtick.major.size']   =  10.0      # how long the tick is
    rcParams['xtick.major.width']  =  1.0
    rcParams['xtick.minor.pad']    =  4.0
    rcParams['xtick.minor.size']   =  2.0
    rcParams['xtick.minor.width']  =  0.5
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  6
    rcParams['ytick.major.pad']    =  4.0
    rcParams['ytick.major.size']   =  10.0
    rcParams['ytick.major.width']  =  1.0
    rcParams['ytick.minor.pad']    =  4.0
    rcParams['ytick.minor.size']   =  4
    rcParams['ytick.minor.width']  =  0.5
    rcParams['ytick.minor.visible']=  True


    rcParams['legend.borderaxespad']   =  0.5
    rcParams['legend.borderpad']       =  0.4
    rcParams['legend.columnspacing']   =  2.0
    rcParams['legend.edgecolor']       =  'inherit'
    rcParams['legend.facecolor']       =  'inherit'
    rcParams['legend.fancybox']        =  False
    rcParams['legend.fontsize']        =  20
    rcParams['legend.framealpha']      =  1
    rcParams['legend.frameon']         =  False
    rcParams['legend.handleheight']    =  0.7
    rcParams['legend.handlelength']    =  2.0
    rcParams['legend.handletextpad']   =  0.8
    rcParams['legend.isaxes']          =  True
    rcParams['legend.labelspacing']    =  0.5
    rcParams['legend.markerscale']     =  1.0
    rcParams['legend.numpoints']       =  2
    rcParams['legend.scatterpoints']   =  3
    rcParams['legend.shadow']          =  False
###################################### 
def setup_ax():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xlabel, ylabel = "% of Total Knapsack Value", "% of Genes to Acoomplish that"

    ax.set_xlabel (xlabel)
    ax.set_ylabel (ylabel)
    
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter_x))
    #ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter_y))    
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    
    return ax
###################################### 
def plot (ax, Xs, Ys, file, color, size):

    sizes = [size]*len(Xs)

    #ax.set_aspect('equal', adjustable='box')
    #ax.set_yscale('log', basex=2, basey=2, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    ax.scatter (Xs, Ys, alpha=.4, marker='o', edgecolors='none',s=sizes,  c=color, cmap=plt.cm.get_cmap('plasma'))
######################################      
update_rcParams()
ax          = setup_ax()

csv_files   = open(sys.argv[1],'r').readlines()
size        = 50
Spectral=[(0.88535179460749902, 0.31903114388970766, 0.29042677143040824), (0.98731257284388818, 0.64736641446749377, 0.36424452942960406), (0.99715494057711429, 0.91180315789054422, 0.60107653281267948), (0.92887351442785826, 0.97154940577114335, 0.63806230531019326), (0.6334486913447287, 0.85213380350786094, 0.64367553065804872), (0.28004614044638243, 0.6269896416103139, 0.70242216306574201)] 
i=0
for file in csv_files: 
    color = Spectral[i%len (Spectral)]
    file = file.strip()
    # Plot:
    #      X   = % of knapsack value, in increment of 10
    #      Y'  = % of genes needed to achieve that % of value
    #      Y"  = avg degree of nodes in each % slices 
    print('')
    solution = open (file,'r')
    skip     = 50
    for i in range(skip):
        next(solution)
    Genes    = next(solution).strip().split()
    Bs       = [int(b) for b in next(solution).strip().split()]
    Ds       = [int(d) for d in next(solution).strip().split()]
    Xs       = [int(x) for x in next(solution).strip().split()]

    bIN, dIN, bOU, dOU          = [x[0] for x in zip(Bs,Xs) if x[1]==1], [x[0] for x in zip(Ds,Xs) if x[1]==1], [x[0] for x in zip(Bs,Xs) if x[1]==0], [x[0] for x in zip(Ds,Xs) if x[1]==0]
    SumBi, SumDi, SumBo, SumDo  = sum(bIN), sum(dIN), sum(bOU), sum(dOU)
    TOT_GENES                   = len(bIN)

    rows_inside, rows_outside  = {}, {}
    for g,b,d,x in zip(Genes,Bs,Ds,Xs):
        g = g.split('$')
        g, ind, oud = g[0], int(g[1]), int(g[2])
        if   x==1:
            rows_inside[g]  = [ind, oud, ind+oud, b, d, x, (float(b)/SumBi)*100, (float(d)/SumDi)*100]
        elif x==0:
            rows_outside[g] = [ind, oud, ind+oud, b, d, x, (float(b)/SumBo)*100, (float(d)/SumDo)*100]
        else:
            print("Fatal: bad solution vector")

    sorted_in = sorted(rows_inside.items(), key=lambda e: e[1][3]) #sort by 3rd element in the values, i.e. benefits
    sorted_ou = sorted(rows_outside.items(),key=lambda e: e[1][3])

    # assert uniqueness of genes
    assert len(set(rows_inside.keys())) == len((rows_inside.keys())) 

    n_resilience            = {10:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 20:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 30:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 40:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 50:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 60:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 70:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 80:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 90:{'harvest':0, 'genes_count':0, 'genes_percent':0}, 100:{'harvest':0, 'genes_count':0, 'genes_percent':0}}
    ceiling                 = {10:int(0.1*SumBi), 20:int(0.2*SumBi), 30:int(0.3*SumBi), 40:int(0.4*SumBi), 50:int(0.5*SumBi), 60:int(0.6*SumBi), 70:int(0.7*SumBi), 80:int(0.8*SumBi), 90:int(0.9*SumBi), 100:int(1*SumBi)}
    index_begin, index_end  = 0, -1

    commulative_harvests = 0
    commulative_num_genes  = 0
    commulative_num_genes_percentage = 0
    for inc in sorted(n_resilience.keys()):
        n_resilience[inc]['harvest']       = commulative_harvests
        n_resilience[inc]['genes_count']     = commulative_num_genes
        n_resilience[inc]['genes_percent'] = commulative_num_genes_percentage
        while abs(index_end)<=len(sorted_in) and n_resilience[inc]['harvest']  < ceiling[inc]:
            #print (str(inc).ljust(5,' ')+str((index_begin)).ljust(7,' ')+str((index_end)).ljust(10,' ')+str(sorted_in[index_end]))
            big_increment   = sorted_in[index_end][1][3]
            if n_resilience[inc]['harvest'] + big_increment > ceiling[inc]:
                break
            n_resilience[inc]['harvest'] += big_increment            
            index_end -= 1
            n_resilience[inc]['genes_count'] += 1
        while index_begin < len(sorted_in) and n_resilience[inc]['harvest']  < ceiling[inc]:
            #print (str(inc).ljust(5,' ')+str((index_begin)).ljust(7,' ')+str((index_end)).ljust(10,' ')+str(sorted_in[index_begin]))
            small_increment = sorted_in[index_begin][1][3]
            n_resilience[inc]['harvest'] += small_increment    
            index_begin += 1
            n_resilience[inc]['genes_count'] += 1
    
        n_resilience[inc]['genes_percent'] = (n_resilience[inc]['genes_count']/TOT_GENES) * 100
        commulative_harvests               = n_resilience[inc]['harvest']
        commulative_num_genes              = n_resilience[inc]['genes_count']
        commulative_num_genes_percentage   =  n_resilience[inc]['genes_percent'] 

    assert n_resilience[100]['harvest'] == SumBi and n_resilience[inc]['genes_count'] == len(bIN) and (index_begin+abs(index_end)) == len(bIN)+1

    for inc in sorted(n_resilience.keys()):
        print ((str(inc)+' %').ljust(5,' ')+\
               str(n_resilience[inc]['harvest']).ljust(10,' ')+\
               str(f((inc/100.0)*SumBi)).ljust(10,' ')+\
               str(n_resilience[inc]['genes_count']).ljust(10,' ')+\
               str(f(n_resilience[inc]['genes_percent']))+' %'.ljust(10,' '))
    
    Xs = [inc for inc in sorted(n_resilience.keys())]
    Ys = [n_resilience[inc]['genes_percent'] for inc in sorted(n_resilience.keys())]
    plot(ax, Xs,Ys, file, color, size)
    
print ('\nSaving .. plot.png\n')
plt.savefig("plot.png",dpi=300,bbox_inches="tight")  
    
    
    
    
    
    
    
