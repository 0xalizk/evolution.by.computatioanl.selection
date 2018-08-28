import matplotlib as mpl # it's important to import this before importing master_bar3d because master_bar3d mpl.use('Agg') 
from sys import platform
if platform == "linux" or platform == "linux2":
    mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import os, sys, numpy as np, pickle
sys.path.insert(0, os.getenv('lib'))
import util_plotting as util
sys.path.insert(0, '../generate_master_dumps' )
import master_bar3d as master
#----------------------------------------------------------------------------------------------------
def get_ARGV            ():
    dir = None
    try:
        dir = util.slash (sys.argv[1])
    except:
        print ("Usage: python3 offline_mass_plotter.py /path/to/master_dump/directory/ \nExiting..\n")
        sys.exit(1)
    try:
        assert os.path.isdir(dir)
    except:
        print ("Error: this is not a valid directory: "+dir+"\nExiting")
        sys.exit(1)
    return dir
#----------------------------------------------------------------------------------------------------
def get_MEASURES        ():
    return ['Bin', 'Din', 'Bou', 'Dou','Sbin', 'Sdin', 'Sbou', 'Sdou']
#----------------------------------------------------------------------------------------------------
def get_COLORS          ():
        
    colors        = {}
    colors['Bin'] = '#47ab5b'#'#2f67b1' 
    colors['Bou'] = '#91cd91'#'#a5d169'#'#69ccdd' 
    colors['Din'] = '#f47621'#'#783229' 
    colors['Dou'] = '#f9b565'#'#f8a99d'  
    
    cmap            = plt.get_cmap("YlGn") # YlOrRd (Din)
    colors['Sbin']  = [cmap(i) for i in range(cmap.N)] # extract all colors from the  cmap, 256 colors
    colors['Sdou']   = [cmap(i) for i in range(cmap.N)]
    cmap            = plt.get_cmap("YlOrRd")
    colors['Sbou']  = [cmap(i) for i in range(cmap.N)]
    colors['Sdin']  = [cmap(i) for i in range(cmap.N)]    
    
    return colors
    
    '''
    #727272 * grey,    Bou
    #f1595f * green,   Bin
    #79c36a * reddish, Din
    #599ad3 * Blueish, Dou
    
    #f9a65a * orange/brown-ish
    #9e66ab * brown
    #cd7058 * purple 
    #d77fb3 * light purple
    #ff8000 * orange
    #ffa500 * light orange
    #ffd300 * super light orange
    #0080ff * blue
    #a5d169 * greenish
    #75ccd0 * blue-greyish
    #9ebbe2 * blue-greyish
    
    #783229 #c75342 * brown and light-brown
    
    #47ab5b  green-ish
    
    #2f67b1 69ccdd * blue and light-blue
    '''
    
    '''
    start       = 0
    skip        = 0
    distinction = 13       # the higher the more distinct the colors will be
    
    #http://matplotlib.org/users/colormaps.html      
    iter01 = iter(cm.GnBu     (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter02 = iter(cm.YlOrBr   (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter03 = iter(cm.YlGn     (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter04 = iter(cm.Spectral (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter05 = iter(cm.Blues    (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter06 = iter(cm.Dark2    (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter07 = iter(cm.Paired   (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter08 = iter(cm.Set1     (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter09 = iter(cm.jet      (np.linspace(0,1,  (distinction*(skip+1))+start)))
    iter10 = iter(cm.cool     (np.linspace(0,1,  (distinction*(skip+1))+start)))
    '''
#----------------------------------------------------------------------------------------------------
def get_NORMS           ():
    return ['TOT', 'EFF']
#----------------------------------------------------------------------------------------------------
def get_CONFIGS         ():
    configs = {}
    configs['plotting_configs'] = {
                                    'fig_suptitle':          "Effective knapsack value", 
                                    'fig_suptitle_fontsize': 18,             
                                    'plot':                  "bar3d",
                                    'xlabel':                "$tolerance (\% edges)$", 
                                    'ylabel':                "$pressure (\% nodes)$",
                                    'zlabel':                 "$effective$ $total$  $benefits$",
                                    'alpha':                 .9,
                                    'wspace':                0.1,
                                    'hspace':                0.1,
                                    'projection':            None,
                                    'dpi':                   300,
                                    'elev':                   25, #10, # this tilts it north-south, default 25
                                    'azim':                  -38, #-1.5, # this tilts it east-west, default -38
                                    'dx':                     0.3, # the bar width
                                    'dy':                     0.3, # the bar depth
                                    'bar_spacing':            1,
                                    'xticklabels':           ['100','75','50','25','20','15','10','5','1','0.1'], 
                                    'yticklabels':           ['100','75','50','25','20','15','10','5','1','0.1'],
                                    'file_extension':         '.png'
                            }
    return configs
#----------------------------------------------------------------------------------------------------
def get_COLS            (measure):
    if measure in ['Bin', 'Din', 'Bou', 'Dou']:
        return len(get_NORMS())
    else:
        return 1
#----------------------------------------------------------------------------------------------------
def get_ROWS    (DUMP_DIR):
    rows = 0
    for r,ds,fs in os.walk(DUMP_DIR.strip()):
        for file in fs:
            if file.split('.')[-1]=='dump':
                rows += 1
    return rows
#----------------------------------------------------------------------------------------------------
def get_DUMPS   (DUMP_DIR):
    MASTER_DUMPS = []
    for r, d, dumps in os.walk(DUMP_DIR.strip()):
        for file in dumps:
            if file.split('.')[-1]=='dump':
                MASTER_DUMPS.append(os.path.join(r,file))
    return MASTER_DUMPS            
#----------------------------------------------------------------------------------------------------
def stdwrite(out):
    sys.stdout.write (out) 
    sys.stdout.flush()
#----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    dump_dir              = get_ARGV    ()
    configs               = get_CONFIGS ()
    colors                = get_COLORS  () 
    master_dumps          = get_DUMPS   (dump_dir)
    rows                  = get_ROWS    (dump_dir)    
    NORMS                 = get_NORMS()
    for measure in get_MEASURES():
        stdwrite("\nNow plottting "+measure+": ")
        cols                  = get_COLS    (measure)
        fig_width             = cols*10
        fig_height            = rows*6
        fig = plt.figure(figsize=(fig_width, fig_height), frameon=True) # matplotlib.pyplot.gcf().set_size_inches(12*cols, 3*rows)
        fig.suptitle("\n\n"+measure)
        fig.subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['plotting_configs']['wspace'], hspace=configs['plotting_configs']['hspace'] )
        current_pos = 1                    
        for master_dump in sorted(master_dumps):        
            current_dump = None
            with open (master_dump,'rb') as f:
                current_dump = pickle.load(f)
                f.close()
            #****************************************************************************************************
            title, ZLIMS, DICT_of_AVGs    =    current_dump[0], current_dump[1], current_dump[2]
            #**************************************************************************************************** 
            
            if measure in ['Sbin','Sdin','Sbou','Sdou']:
                stdwrite (str(current_pos)+',') 
                ax = fig.add_subplot (rows, cols, current_pos,  projection='3d')
                # IF YOU WANT TO IMPOSE A GLOBAL ZLIM, UN-COMMENT THE FOLLOWING LINE (otherwise use zlim = ZLIMS[measure]):
                zlim = 750 # Perrimon = 750, Suratanee = 400,  IntAct = 950 
                configs['plotting_configs']['elev'], configs['plotting_configs']['azim'], configs['dx'], configs['dy']= 10, -1.75, 0.8, 0.1
                master.plot_next_stacked_bar3d(fig, ax, title, zlim, DICT_of_AVGs, configs, measure=measure, colors=get_COLORS())
                current_pos+=1
            else:
                for norm in NORMS:
                    stdwrite(norm+'-'+str(current_pos)+', ')  
                    ax = fig.add_subplot (rows, cols, current_pos,  projection='3d')
                    # IF YOU WANT TO IMPOSE A GLOBAL ZLIM, UN-COMMENT THE FOLLOWING LINE (otherwise use zlim = ZLIMS[measure]):
                    zlim = ZLIMS[measure][norm] # Perrimon = 750, Suratanee = 400,  IntAct = 950                                         
                    master.plot_next_bar3d (fig, ax, title+', '+norm, zlim, DICT_of_AVGs, configs, measure=measure, norm=norm, colors=get_COLORS())
                    current_pos+=1
            #for a in [-1.5]:#[4,-4,15,-15,20,-20]:#range(,5,1):
            #    for e in range(0,25,2):
            #        ax.azim=a
            #        ax.elev=e
            #        fig.savefig(dump_dir+measure+str(a)+"_"+str(e)+configs['plotting_configs']['file_extension'], dpi=configs['plotting_configs']['dpi'], bbox='tight')          
        fig.savefig(dump_dir+measure+configs['plotting_configs']['file_extension'], dpi=configs['plotting_configs']['dpi'], bbox='tight')  
        colors = None
    stdwrite("\n\nDone")
#----------------------------------------------------------------------------------------------------
