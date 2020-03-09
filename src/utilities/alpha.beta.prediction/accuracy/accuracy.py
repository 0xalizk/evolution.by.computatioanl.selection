import matplotlib.pyplot as plt, math, numpy as np, sys, os
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
sys.path.insert(0, os.getenv('lib'))
import fitting_lib
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
    rcParams['legend.fontsize']        =  2
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
def handle_tickers(ax,bars,Ts,location='inside_bar'):
    ax.set_yticks([x for x in range(0,101,10)])
    
    if location=='inside_bar':
        ax.set_xticklabels(['']*len(Ts)) # no xticks, instead we will annotate them inside bars
        for b,t in zip(bars,Ts):
             #print(str(b.get_height()))
             xloc = b.get_x()+(bar_width/1.6)
             yloc = 5#b.get_height()/2 # bars always start at 0
             fontsize = 24
             ax.text(xloc, yloc, t, rotation=90, horizontalalignment='center', verticalalignment='bottom', color='white', weight='bold', clip_on=True, fontsize=fontsize)
        # dont draw ticks
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1On = False
    else:
        ax.set_xticklabels(Ts,rotation=-90)
#################################################################################### 
def setfam(fam):
    if 'ppi' in fam.lower():
        return "Protein-protein interaction networks"
    if 'regulatory' in fam.lower():
        return "Regulatory networks"
    if 'db-' in fam.lower():
        return "Database-sourced networks"
    return fam
####################################################################################  
def plot(Ys, Xs, Ts, Ylims, ax, bar_width,fam):
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #ax.text(.2,.2,title+': '+str(n2e)+'/'+str(e2n), horizontalalignment='center', transform=ax.transAxes, size=35)
    
    
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on') # both major and minor ticks
    ax.set_ylabel("% accuracy")
    ax.yaxis.set_label_position("right")
    ax.set_xlabel(setfam(fam))
    ####################################################################################
    bars = ax.bar(Xs, Ys,  bar_width, tick_label=Ts, color='#0B6300', linewidth=0, alpha=.8) # color=['forestgreen','blue']*(int(len(Ts)/2))
    ####################################################################################
    ax.set_xticks([x+(bar_width/2.0) for x in ax.get_xticks()])
    #labels,i = [],0
    #for t in ax.get_xticklabels():
        #if tick>0 and tick <= len(Ts):
        #    labels.append(Ts[i])
        #    i+=1
        #else:
        #    labels.append('')
    handle_tickers(ax,bars, Ts, location='inside_bar')
    ax.set_ylim(Ylims)
    #ax.set_xlim([0,len(Ts)+1])
    return ax
####################################################################################
if __name__ == '__main__':

    ###########################################################
    networks =    fitting_lib.networks
    ###########################################################

    update_rcParams()
    figure_size = (20,20)
    
    
    ALL_NETS       = [elem[0] for elem in sorted(networks().items(), key=lambda x: x[1]['ID'])]# sorted([key for key in networks().keys()])
    target_families = ['DB-sourced','PPIs', 'Regulatory']#,'DB-sourced','PPIs_orig'] 
    for fam in target_families:
        COORDs      = getCOORDs (figure_size, 1,1 , w2h_ratio=0.6, ppercent= 0.5)
        fig         = plt.figure(figsize=figure_size)
        #if len(target_families)>0:
        NETS = []
        NETS       = [n for n in ALL_NETS if networks()[n]['Family'] == fam]
        #NETS=['Bacteria-PPI', 'Bacteria-PPI_orig', 'Fly-PPI', 'Fly-PPI_orig', 'Human-PPI', 'Human-PPI_orig', 'Human-PPI-Iso', 'Human-PPI-Iso_orig',  'Plant-PPI', 'Plant-PPI_orig', 'Worm-PPI', 'Worm-PPI_orig', 'Yeast-PPI', 'Yeast-PPI_orig']
        ACCURACY   = []
        TITLES     = []
        for key in NETS:
            ACCURACY.append(networks()[key]['abs_accuracy'])
            TITLES.append(key.replace('--','-').replace('-',' ').replace('Human ENCODE','ENCODE'))#.replace('Vinayagam','Fly_orig')).replace('_orig','').replace('TRRUST','HumanReg') )

        bar_width = .5
        locs      = [ 1+x-(bar_width/2) for x in range(len(NETS))]
        YLIMS     = [0,100]
        print('plotting ..')
        plot(ACCURACY, locs, TITLES, YLIMS, fig.add_axes(COORDs[0]), bar_width,fam)

        #file_name = 'accuracy_'+networks.__name__+'_'+'_'.join(target_families)+'.png'
        file_name = 'accuracy_'+fam+'.png'
        print('saving ..  '+file_name)
        plt.savefig(file_name,dpi=300, bbox_inches="tight")
    #plt.clf()
