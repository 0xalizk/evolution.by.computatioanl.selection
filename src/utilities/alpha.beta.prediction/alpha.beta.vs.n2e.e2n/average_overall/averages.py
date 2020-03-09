import matplotlib.pyplot as plt, math, numpy as np, sys, os
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
sys.path.insert(0, os.getenv('lib'))
import fitting_lib
avg  =  np.average
std  =  np.std
alpha = .9
####################################################################################
def update_rcParams():
    rcParams['savefig.pad_inches'] = .2

    rcParams['axes.grid']          = True
    rcParams['axes.titlesize']     = 36
    rcParams['axes.labelsize']     = 28
    font_path = os.getenv('HOME')+'/.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = prop.get_name()

    #rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
    rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

    rcParams['figure.titleweight']    = 'bold'
    rcParams['figure.titlesize']      = 45
    rcParams['figure.subplot.hspace'] = 0.9
    rcParams['figure.subplot.wspace'] = 0.1
    rcParams['figure.subplot.left']   = 0.1
    rcParams['figure.subplot.right']  = 0.9
    rcParams['figure.subplot.top']    = 0.90 # create a space between title and subplots
    rcParams['figure.subplot.bottom'] = 0.1

    rcParams['grid.alpha']         =  1
    rcParams['grid.color']         =  '#b3cccc' #'#63cae9'
    rcParams['grid.linestyle']     =  'solid' # dashed solid dashdot dotted
    rcParams['grid.linewidth']     =  0.5
    rcParams['axes.grid.axis']     =  'y'
    rcParams['axes.grid.which']    =  'both'


    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  22
    rcParams['xtick.major.pad']    =  1.0
    rcParams['xtick.major.size']   =  10.0      # how long the tick is
    rcParams['xtick.major.width']  =  1.0
    rcParams['xtick.minor.pad']    =  1.0
    rcParams['xtick.minor.size']   =  5.0
    rcParams['xtick.minor.width']  =  1
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  22
    rcParams['ytick.major.pad']    =  4.0
    rcParams['ytick.major.size']   =  10.0
    rcParams['ytick.major.width']  =  1.0
    rcParams['ytick.minor.pad']    =  4.0
    rcParams['ytick.minor.size']   =  5
    rcParams['ytick.minor.width']  =  1
    rcParams['ytick.minor.visible']=  False


    rcParams['legend.borderaxespad']   =  0.5
    rcParams['legend.borderpad']       =  0.4
    rcParams['legend.columnspacing']   =  2.0
    rcParams['legend.edgecolor']       =  'inherit'
    rcParams['legend.facecolor']       =  'inherit'
    rcParams['legend.fancybox']        =  False
    rcParams['legend.fontsize']        =  30
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
####################################################################################
def getCOORDs (fig_inch_dims, cols, rows, w2h_ratio=0.5, ppercent= 0.25):
    COORDs    = []
    figw_inch = fig_inch_dims[0]
    figh_inch = fig_inch_dims[1]
    totp      = cols*rows

    #everything else is in % of canvas
    Xpads     = (ppercent*figw_inch)/figw_inch # as % of fig width is padding
    Ypads     = (ppercent*figh_inch)/figh_inch # as % of fig height is padding

    xpad      = Xpads/cols
    ypad      = Ypads/rows

    axw      = ((figw_inch-(Xpads*figw_inch))/cols)/figw_inch  # as a % of fig width
    axh      = (axw - axw*w2h_ratio) / w2h_ratio #((figh_inch-(Xpads*figh_inch))/cols)/figh_inch

    p, r        = 0, 0
    for i in range(int(totp)):
        x_shift  = (axw+xpad)*r
        y_shift  = (axh+ypad)*math.floor(p/cols)
        if x_shift==0:
            x_shift = xpad*.05
        if y_shift == 0:
            y_shift = ypad*.05

        COORDs.append([x_shift, y_shift, axw, axh])

        p+=1
        r+=1
        if p%cols == 0: # starting a new row, zero-out r
            r = 0
    SORTED=[]
    COORDs = COORDs[::-1]
    for i in range(0, len(COORDs), cols):
        for j in COORDs[i:i+cols][::-1]:
            SORTED.append(j)

    #print ('Xpads: '+str(Xpads)+'\tYpads: '+str(Ypads)+'\tfigw_inch: '+str(figw_inch)+'\tfigh_inch: '+str(figh_inch)+'\txpad: '+str(xpad)+'\typad: '+str(ypad)+'\taxw: '+str(axw)+'\taxh:'+str(axh))
    return  SORTED
####################################################################################
def plot(Ys, Xs, patch_labels, colors, ax, bar_width):

    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['right'].set_visible(True)

    #ax.text(.2,.2,title+': '+str(n2e)+'/'+str(e2n), horizontalalignment='center', transform=ax.transAxes, size=35)
    #ax.set_ylabel("frequency (% nodes)")
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='on',  labelleft='on', labelright='on') # both major and minor ticks
    
    avg_n2e, std_n2e = avg([y[0] for y in Ys[0]]), std([y[0] for y in Ys[0]])
    avg_e2n, std_e2n = avg([y[1] for y in Ys[0]]), std([y[1] for y in Ys[0]])
    avg_alp, std_alp = avg([y[0] for y in Ys[1]]), std([y[0] for y in Ys[1]])
    avg_bet, std_bet = avg([y[1] for y in Ys[1]]), std([y[1] for y in Ys[1]])    
    ####################################################################################
    ax.bar(Xs[0], avg_n2e,  bar_width, color=colors[0][0], linewidth=0, alpha=alpha,yerr=std_n2e, ecolor='black') #
    ax.bar(Xs[1], avg_alp,  bar_width, color=colors[0][1], linewidth=0, alpha=alpha,yerr=std_alp, ecolor='black') #
    ax.bar(Xs[2], avg_e2n,  bar_width, color=colors[1][0], linewidth=0, alpha=alpha,yerr=std_e2n, ecolor='black') #
    ax.bar(Xs[3], avg_bet,  bar_width, color=colors[1][1], linewidth=0, alpha=alpha,yerr=std_bet, ecolor='black') #
    ####################################################################################
        
    n2e   = mpatches.Patch(color =colors[0][0], label=patch_labels[0])
    alp   = mpatches.Patch(color =colors[0][1], label=patch_labels[1])
    e2n   = mpatches.Patch(color =colors[1][0], label=patch_labels[2])
    bet   = mpatches.Patch(color =colors[1][1], label=patch_labels[3])

    legend = plt.legend(handles=[n2e, alp, e2n, bet], loc=(.05, .7), frameon=True) # see rcParams above to make changes
    frame = legend.get_frame()
    frame.set_linewidth(0)
    frame.set_facecolor('white')
    ax.set_ylim([0,4])
    
    #ax.set_xlim([0.5,100])
    return ax
####################################################################################
def setfamlabel(fams):
    labels=[]
    for f in fams:
        if 'ppi' in f.lower():
            labels.append("Protein-protein interaction\n networks")
        elif 'regulatory' in f.lower():
            labels.append("Regulatory\n networks")
        elif 'db-' in f.lower():
            labels.append("Database-sourced\n networks")
        else:
            labels.append(f)
    return labels
####################################################################################
if __name__ == '__main__':

    ###########################################################
    networks =    fitting_lib.networks
    ###########################################################

    update_rcParams()
    figure_size = (30,30)
    fig         = plt.figure(figsize=figure_size)
    COORDs      = getCOORDs (figure_size, 2, 1, w2h_ratio=0.6, ppercent= 0.15)
    pos         = 0

    ungrouped       = [elem[0] for elem in sorted(networks().items(), key=lambda x: x[1]['ID'])]# sorted([key for key in networks().keys()])
    target_families = ['PPIs', 'Regulatory','DB-sourced']#,'PPIs_orig'] #optional, default: all families
    NETS = []
    for f in target_families:
        NETS.append([n for n in ungrouped if networks()[n]['Family'] == f])
    
    N2EsE2Ns     = []
    ALPHAs_BETAs = []
    LOCS         = []
    COLORS       = []
    LABELS       = []
    TITLES       = []
    bar_width    = 1
    x            = 1
    xticks       = []
    i=0
    for group in NETS:                   
        COLORS.append([   ['#e54002', '#e59202'],          ['#0274e5', '#59aeec']               ])
        LABELS.append([   '$n2e$','$\\alpha$', '$e2n$','$\\beta}$' ]     )
        LOCS.append([2*bar_width+x,3*bar_width+x, 4*bar_width+x, 5*bar_width+x])  
        xticks = xticks + [(4*bar_width+x)]   
        x            += bar_width*5
        N2EsE2Ns.append([])
        ALPHAs_BETAs.append([])
        for key in group:
            N2EsE2Ns[-1].append(     [   networks()[key]['node2edge'],      networks()[key]['edge2node']       ])
            ALPHAs_BETAs[-1].append( [   networks()[key]['node2edge_adj'],  networks()[key]['edge2node_adj']   ])
    
    #print('N2EsE2Ns: '+str(N2EsE2Ns))
    #print('\nALPHAs_BETAs'+str(ALPHAs_BETAs))
    #print('\nLOCS'+str(LOCS))
    #print('\nTITLES'+str(TITLES))
    #print('\nLABELS'+str(LABELS)) 
    #print('\nxticks'+str(xticks))  
    ax = fig.add_axes(COORDs[0])
    for i in range(len(NETS)):
        Ys, Xs, Ps, Cs = [N2EsE2Ns[i], ALPHAs_BETAs[i]], LOCS[i], LABELS[i],  COLORS[i]  
        plot(Ys, Xs, Ps, Cs, ax, bar_width)
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(setfamlabel(target_families))
    ax.set_xlabel("Networks")
    ax.set_ylabel("Average")
    file_name = 'alpha.beta.n2e.e2n_averages'+'_'.join(target_families)+'.png'
    print('saving ..  '+file_name)
    plt.savefig(file_name,dpi=300, bbox_inches="tight")
    #plt.clf()
