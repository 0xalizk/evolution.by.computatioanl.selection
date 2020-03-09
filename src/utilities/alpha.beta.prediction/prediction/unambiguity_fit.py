import matplotlib.pyplot as plt, math, numpy as np, sys, os
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
sys.path.insert(0, os.getenv('lib'))
import fitting_lib
log10=math.log10
ceil,floor =math.ceil,math.floor
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
def update_rcParams():
    rcParams['savefig.pad_inches'] = .2

    rcParams['axes.grid']          = True
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
    rcParams['axes.grid.axis']     =  'both'
    rcParams['axes.grid.which']    =  'both'
    rcParams['axes.titlesize']     = 36
    rcParams['axes.labelsize']     = 28
    rcParams['axes.labelpad']      = 0.1

    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  22
    rcParams['xtick.major.pad']    =  1.0
    rcParams['xtick.major.size']   =  10.0      # how long the tick is
    rcParams['xtick.major.width']  =  1.0
    rcParams['xtick.minor.pad']    =  1.0
    rcParams['xtick.minor.size']   =  5.0
    rcParams['xtick.minor.width']  =  1
    rcParams['xtick.minor.visible']=  True


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  22
    rcParams['ytick.major.pad']    =  4.0
    rcParams['ytick.major.size']   =  10.0
    rcParams['ytick.major.width']  =  1.0
    rcParams['ytick.minor.pad']    =  4.0
    rcParams['ytick.minor.size']   =  5
    rcParams['ytick.minor.width']  =  1
    rcParams['ytick.minor.visible']=  True


    rcParams['legend.borderaxespad']   =  0.5
    rcParams['legend.borderpad']       =  0.4
    rcParams['legend.columnspacing']   =  2.0
    rcParams['legend.edgecolor']       =  'inherit'
    rcParams['legend.facecolor']       =  'inherit'
    rcParams['legend.fancybox']        =  False
    rcParams['legend.fontsize']        =  28
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
    #for key in rcParams.keys():
    #    if 'pad' in key:
    #        print(key.ljust(30,' ')+str(rcParams[key]))
####################################################################################
def percentages_formatter(x, y):
    if float(x)>=1:
        return str(int(x))+"%"
    else:
        if x>=0.001:
            return str(x)+"%"
        else:
            return ""
####################################################################################
def log_formatter(x, y):
    if float(x)>=1:
        return str(int(x))
    else:
        return ""
####################################################################################
def verify(unity):
    try:
        assert unity >=.99999
    except:
        print(" WARNING: unity != 1; unity = "+l(unity))
        pass
####################################################################################
def plot(actualXY, predictedXY, title, ax,Alpha,Beta, e2n, n2e):

    predicted_color = '#0B6300'#'#0087ff'#'forestgreen'#'#e1035e'#'#FF5733'  # '#f5883f'
    actual_color    = '#ff12b7'#'#fc0202'#'#4cc1e7'   # '#63cae9'

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    annot  = title.replace('-',' ').replace(' Iso','-Iso').replace(' ','\n')
    #annot += '\n$n2e$='+str(round(n2e,2))+', $e2n$='+str(round(e2n,2))+'\n$\\alpha$='+str(Alpha)+', $\\beta$='+str(Beta)
    
    ax.text(.05,.25,annot, horizontalalignment='left',transform=ax.transAxes, fontdict={'weight': 'bold', 'size': 30})# fontdict={'family': 'serif',         'color':  'darkred'}) # https://matplotlib.org/users/text_props.html
    #ax.text(.27,.2,'PPI (Fly)',horizontalalignment='center', transform=ax.transAxes, size=35)
    ax.set_xlabel("degree")
    ax.set_ylabel("frequency (% nodes)")
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks
    ax.set_xscale('log')
    ax.set_yscale('log')

    ##########################################################################
    ax.scatter(actualXY[0]   , actualXY[1],    color=actual_color,     marker='_', linewidth=5, edgecolors='', alpha=.8, s=[200]*len(actualXY[1]))#
    ax.scatter(predictedXY[0], predictedXY[1], color=predicted_color,  marker='|', linewidth=5, edgecolors='', alpha=.7, s=[200]*len(predictedXY[1])) #
    ##########################################################################


    ax.xaxis.set_major_formatter(ticker.FuncFormatter(log_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(percentages_formatter))

    ap   =  mpatches.Patch(color=actual_color,    label='actual')
    pp   =  mpatches.Patch(color=predicted_color, label='predicted')


    legend = plt.legend(handles=[ap, pp], loc=(.6, .6), frameon=True) # see rcParams above to make changes
    frame = legend.get_frame()
    frame.set_linewidth(0)
    frame.set_facecolor('white')
    ########################################
    #print(max(actualXY[0]))
    o = max(actualXY[0])
    x = max(10,o)
    x = log10(x)
    x = floor(x)
    x = 10**x
    x = x * ceil(o/x)
    #print(x)
    ax.set_xlim([0.5,x])
    ax.set_ylim([min(actualXY[1])/2, 100])
    ########################################
    ax.set_axisbelow(True) # draw the grid lines in the background (scatter dots in the foreground)
    return ax
####################################################################################
if __name__ == '__main__':

    ###########################################################
    networks =    fitting_lib.networks
    ###########################################################

    target_families = ['DB-sourced']#,'Regulatory','DB-sourced']#,'PPIs_orig'] #optional, default: all families

    update_rcParams()

    nets        = [elem[0] for elem in sorted(networks().items(), key=lambda x: x[1]['ID'])]#[n for n in networks().keys() ]#[0:]
    if len(target_families)>0:
        nets        = [n for n in nets if networks()[n]['Family'] in target_families]
    cols        = min(3,len(nets))
    rows        = math.ceil(len(nets)/cols)

    figure_size = (10*cols,10*cols)
    fig         = plt.figure(figsize=figure_size)
    COORDs      = getCOORDs (figure_size, cols, rows, w2h_ratio=0.6, ppercent= 0.2)
    pos         = 0

    for key in nets:
        print(key)

        deg, freq, e2n, n2e, Beta, Alpha = networks()[key]['deg'], networks()[key]['freq'], networks()[key]['edge2node'], networks()[key]['node2edge'], networks()[key]['edge2node_adj'], networks()[key]['node2edge_adj']

        X    =  [x for x in range (1,max(deg)+1, 1)]
        actual = [f*100 for f in freq]
        predicted  = [fitting_lib.unambiguity_score(deg,Alpha,Beta)*100 for deg in X]

        plot([deg,actual], [X,predicted], key , fig.add_axes(COORDs[pos]),Alpha,Beta, e2n, n2e)

        pos+=1
    population = nets[0]
    if len(nets) > 1:
        population+='_et.al.'
    if len(target_families)>0:
        population='_'.join(target_families)
    name = 'predicted_'+population+'_'+networks.__name__+'.png'
    print('saving ..'+name)
    plt.savefig(name,dpi=300, bbox_inches="tight")
