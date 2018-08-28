import matplotlib as mpl
import matplotlib.pyplot as plt, math, os
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
##################################################################
def update_rcParams(total_plots):
    font_path = os.getenv('HOME')+'/.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    mpl.rcParams['font.family'] = prop.get_name() 
    rcParams['axes.labelsize'] = 8-math.log(totp)
    rcParams['axes.titlesize'] = 8-math.log(totp)
    rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
    rcParams['grid.alpha'] = 0.1
    rcParams['axes.grid']=False
    rcParams['ytick.minor.pad']=0.01
    rcParams['ytick.major.pad']=0.01
    rcParams['savefig.pad_inches']=.1
    rcParams['grid.color']='white'
    
    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  8-math.log(total_plots)
    rcParams['xtick.major.pad']    =  1.0
    rcParams['xtick.major.size']   =  max(.1, 3.0-math.log(total_plots))      # how long the tick is
    rcParams['xtick.major.width']  =  max(.01, 3.5-math.log(total_plots))
    rcParams['xtick.minor.pad']    =  1.0
    rcParams['xtick.minor.size']   =  max(.1, 2.0-math.log(total_plots))
    rcParams['xtick.minor.width']  =  max(.01, 0.5-math.log(total_plots))
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  8-math.log(total_plots)
    rcParams['ytick.major.pad']    =  2.0
    rcParams['ytick.major.size']   =  4.0-math.log(total_plots)
    rcParams['ytick.major.width']  =  max(.1, 1-math.log(total_plots))
    rcParams['ytick.minor.pad']    =  max(.1, 2.0-math.log(total_plots))
    rcParams['ytick.minor.size']   =  max(.1, 2-math.log(total_plots))
    rcParams['ytick.minor.width']  =  max(.1, 0.5-math.log(total_plots))
    rcParams['ytick.minor.visible']=  False
##################################################################
def getCOORDs (fig_inch_dims, cols, rows, w2h_ratio=0.5):
    COORDs    = []
    figw_inch = fig_inch_dims[0]
    figh_inch = fig_inch_dims[1]
    ppercent  = .2 # percentage of area to be used for padding 
    totp      = cols*rows

    #everything else is in % of canvas
    Xpads     = (ppercent*figw_inch)/figw_inch # 10% of fig width is padding
    Ypads     = (ppercent*figh_inch)/figh_inch # 10% of fig height is padding

    xpad      = Xpads/cols
    ypad      = Ypads/rows
    
    axw      = ((figw_inch-(Xpads*figw_inch))/cols)/figw_inch  # as a % of fig width
    axh      = (axw - axw*w2h_ratio) / w2h_ratio #((figh_inch-(Xpads*figh_inch))/cols)/figh_inch      
    
    p, r        = 0, 0
    for i in range(int(totp)): 
        x_shift  = (axw+xpad)*r
        y_shift  = (axh+ypad)*math.floor(p/cols)
        if x_shift==0:
            x_shift = xpad*.2
        if y_shift == 0:
            y_shift = ypad*.2
        
        COORDs.append([x_shift, y_shift, axw, axh])
        
        p+=1
        r+=1
        if p%cols == 0: # starting a new row, zero-out r
            r = 0
            
    print ('Xpads: '+str(Xpads)+'\tYpads: '+str(Ypads)+'\tfigw_inch: '+str(figw_inch)+'\tfigh_inch: '+str(figh_inch)+'\txpad: '+str(xpad)+'\typad: '+str(ypad)+'\taxw: '+str(axw)+'\taxh:'+str(axh))
    return COORDs

##################################################################
if __name__ == '__main__':
    figw_inch = 10.0 #* w2h_ratio     
    figh_inch = 10.0 #* (1-w2h_ratio) 
    fig_dims  = (figw_inch, figh_inch)
    cols      = 10.0
    rows      = 1.0
    w2h_ratio = 0.6 # 0.5 => square
    fig = plt.figure(figsize=fig_dims)
    totp=cols*rows
    update_rcParams(totp)
    i=1
    for coords in getCOORDs(fig_dims,cols,rows, w2h_ratio):
        ax = fig.add_axes(coords)
        ax.text(0.1, 0.1, 'axes'+str(i), ha='left', va='center', size=10-math.log(totp), alpha=.5)
        i+=1
        print ('ax '+str(i)+':\t'+str(coords))

    plt.savefig('y.png', bbox_inches='tight', pad_inches=.1, dpi=300)
