import sys, os
sys.path.insert(0, os.getenv('lib'))
from scipy import stats as scipy_stats
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm 
import matplotlib.colors as mcolors
import  socket, math, time, numpy as np
from multiprocessing import Process
from matplotlib import rcParams
import init_plotting as init, util_plotting as util, json
import matplotlib.font_manager as font_manager
#-----------------------------------------------------------------
alpha=.7
#-----------------------------------------------------------------
mywrite = util.mywrite # writes to both file and screen
#-----------------------------------------------------------------
def update_rcParams():
    font_path = util.slash(os.getenv('HOME'))+'.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = prop.get_name()
    #rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
    rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

    rcParams['axes.labelsize'] = 8
    rcParams['axes.titlesize'] = 8
    rcParams['grid.alpha'] = 0.1
    rcParams['axes.grid']=False
    rcParams['savefig.pad_inches']=.01
    rcParams['grid.color']='white'

    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  8
    rcParams['xtick.major.pad']    =  1.0
    rcParams['xtick.major.size']   =  3.0      # how long the tick is
    rcParams['xtick.major.width']  =  0.5
    rcParams['xtick.minor.pad']    =  1.0
    rcParams['xtick.minor.size']   =  2.0
    rcParams['xtick.minor.width']  =  0.5
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  8
    rcParams['ytick.major.pad']    =  1.0
    rcParams['ytick.major.size']   =  3.0
    rcParams['ytick.major.width']  =  0.5
    rcParams['ytick.minor.pad']    =  4.0
    rcParams['ytick.minor.size']   =  4
    rcParams['ytick.minor.width']  =  0.5
    rcParams['ytick.minor.visible']=  False
#-----------------------------------------------------------------
def supervise (configs_file, num_workers):
    update_rcParams()
    configs                     = init.load_simulation_configs (configs_file, 0)
    configs['num_workers']      = num_workers
    configs['master_log']       = configs['logs_dir']+"master_"+configs['timestamp']+".log"
    log                         = configs['master_log']
    mywrite(log, "\n====================================\nmaster says: supervising\n====================================\n")
    mywrite(log, '\n\t' + '\n\t'.join([str(key).ljust(25,' ') + '= '+str(configs[key]) for key in configs.keys()]))
    
    configs['plotting_configs'] = {
                                    'fig_suptitle':          "Benefit vs Damage plot", 
                                    'fig_suptitle_fontsize': 18,             
                                    'plot':                  "scatter_BD",
                                    'xlabel':                "Damage", 
                                    'ylabel':                "Benefit",
                                    'alpha':                 1,
                                    'cbar_labelsize':        5,
                                    'wspace':                0.02, # it was 0.2
                                    'hspace':                0.4,  # it was 0.4
                                    'projection':            None,
                                    'dpi':                   configs['dpi']
                            }
    
    
    available_workers, needed_workers, DONEs  = num_workers, 0, []
    configs['watchlist']      = 0
    
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            if 'done' in f.split('.'):
                #worker_xxxx_figure_0001_rows_0006_cols_0004_pos_0001.done
                DONEs.append (f[11:])
    
    AXES      = []
    FIGURES   = []
    file_no   = 0      #an index to a svg files
    row_no    = 0      #an index to a row
    col_no    = 0      #an index to a column
    pos       = 0

    for file in sorted(configs['input_files']):
        file_no    += 1
        csv_files   = open(file.strip(), 'r').readlines()
                
        total_rows  = math.ceil(len(csv_files)/configs['columns'])
        total_cols  = configs['columns']
        PAIRS       = util.getPairs (csv_files, min(len(csv_files), configs['files_per_pair']))                
        
        
        figure_size             = (6*total_cols, 4*(max(total_rows,2))) #(width, height), it was 5x4
        FIGURES.append(plt.figure(figsize=figure_size))
        y = 1.2 
        if total_rows>2:
            y=1
        FIGURES[-1].suptitle('\n'+configs['plotting_configs']['fig_suptitle'], fontsize=configs['plotting_configs']['fig_suptitle_fontsize'], y=y       )  
        FIGURES[-1].subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['plotting_configs']['wspace'], hspace=configs['plotting_configs']['hspace'] )

        pos = 1  
        pair_counter = 1  
        for pair in PAIRS: # a pair for each worker 
            if len(pair)>0:
                pair_counter+=1
                tmp=[]
                if needed_workers  >= available_workers:
                    break
                #worker_0001_figure_0001_rows_0006_cols_0004_pos_0001.done
                for tuple in pair:
                    if ("_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(total_rows).rjust(4,'0')+ "_cols_"+str(total_cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')+'.done') not in DONEs:
                        tmp.append((file_no, total_rows, total_cols, pos, tuple[0], tuple[1], tuple[2], 1))
                    else:
                        tmp.append((file_no, total_rows, total_cols, pos, tuple[0], tuple[1], tuple[2], 0))
                
                    configs['watchlist'] += 1
                    pos                  += 1
            
                processing_bits = [b[7] for b in tmp] #b[7]=0 => don't process this file, it's done
                if sum(processing_bits)  > 0:
                    AXES.append([t for t in tmp])
                    needed_workers += 1
            

    if available_workers < needed_workers:
        mywrite(log, "\n\n\nmaster says: WARNING: available_workers < needed_workers,"+str(needed_workers - available_workers)+" subplots will not be plotted ")

    next_ax=0
    for rank in range(1, min(available_workers, len(AXES))+1, 1): # num_workers == num pairs
        with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'w') as f:               
            configs['AXES']  = [AXES[next_ax]]
            json.dump(configs, f)
            f.close()
            next_ax+=1
    
    #send empty AXES to these extra workers
    if available_workers > len(AXES) :
        for rank in range(len(AXES)+1, available_workers+1,1):
            with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'w') as f:   
                configs['AXES']= []
                json.dump(configs, f)
                f.close()
    mywrite(log, "\n\n\tmaster says: WORKERS:  avail "+str(available_workers)+", assigned: "+str(next_ax)+", needed: "+str(needed_workers)+", len(AXES) "+str(len(AXES))+", len(DONEs) "+str(len(DONEs))+"\n")
      
    #not serializable, append it after json dump
    configs['plotting_configs']['cmap'] = plt.cm.get_cmap('plasma')
    configs['plotting_configs']['marker'] = mpl.markers.MarkerStyle(marker='+', fillstyle=None)

    watch (configs, FIGURES, AXES)
#-----------------------------------------------------------------
def watch (configs, FIGURES, AXES):
    log = configs['master_log']
    t0  = time.time()

    if len (AXES) == 0:
        mywrite(log, "\n\tmaster says: len(AXES)==0, Im exiting, goodnight")
        
    else:    
        total_plots = configs['watchlist']
        mywrite(log, "\n\tmaster says: watching "+str(total_plots) +"  subplots")
        
        harvested_files  = [] 
        counter          = 0
        while counter < total_plots:
            time.sleep (30)
            for root, dirs, fs in os.walk(configs['DUMP_DIR']):
                confirmation = False
                for f in fs: # skip directories recently modified (1 minutes), workers may still be writing to them
                    if 'done' in f.split('.') and f not in harvested_files:
                        
                        confirmation = harvest (configs, os.path.join(root, f), AXES, FIGURES)
                        if confirmation == True:
                            harvested_files.append(f)
                            counter += 1
                            mywrite(log, "\n\tmaster says: harvesting ("+str(counter).rjust(3,'0')+"): "+f.split('/')[-1])
                            
                            
        i=1
        for fig in FIGURES:
            #fig.tight_layout()
            mywrite(log, "\n\tmaster says: saving figure no. "+str(i)+": "+util.slash(configs['plots_dir'])+str(i).rjust(3,'0')+"_"+configs['timestamp']+"."+configs['file_extension'])
            fig.savefig(util.slash(configs['plots_dir'])+"scatter_"+str(i).rjust(3,'0')+"."+configs['file_extension'], dpi=configs['plotting_configs']['dpi'], bbox_inches="tight")
            i+=1
        
        t1 = time.time()
        mywrite(log, "\n\tmaster says: harvested "+str(counter)+" plots in "+str(int(t1-t0))+" seconds\n")            
#-----------------------------------------------------------------
def harvest(configs, file, AXES, FIGURES):
    log = configs['master_log']
    load=''
    with open(file,'r') as f:
        load = json.load(f)

    file_no, rows, cols, pos, prefix, file_path, title, xlim, ylim, Bs, Ds, frequency, cbar_label = load[0], load[1], load[2], load[3], load[4], load[5], load[6], load[7], load[8], load[9], load[10], load[11], "$Frequency \quad (log_2)$"
    if len(load)>=13: # old versions of workers don't provide this parameter
        cbar_label = load[12]
    mywrite(log,"\n\tmaster says: plotting file no "+str(file_no)+", coordinates \t\t"+str(rows)+", "+str(cols)+", "+str(pos))
    ax = FIGURES[file_no-1].add_subplot(rows, cols, pos)
    plot_next_scatter(FIGURES[file_no-1], ax, title, xlim, ylim, Bs, Ds, frequency, cbar_label, configs)
    
    return True
#-----------------------------------------------------------------
def plot_next_scatter(fig, ax, title, xlim, ylim, Bs, Ds, frequency, cbar_label, configs):
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    sizes, max_f, min_f=[], max(frequency), min(frequency)
    #print ('\n\n Frequency (sorted) '+str(configs['mode'])+': '+str(sorted(frequency))+'\n\n')
    #if len(frequency)>0:
    #    for f in frequency: # rescale frequencies to the interval [25,50]
    #        sizes.append(  ((f - min_f) / (max_f - min_f) + 1 )*25)       
    #s=sizes
    #-----------------------------------------------------------------
    sc = ax.scatter (Ds, Bs, alpha=alpha, marker='o', edgecolors='none',  c=frequency, cmap=configs['plotting_configs']['cmap'])                      
    #-----------------------------------------------------------------

    cbar = fig.colorbar(sc, shrink=0.4, pad=0.01, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label(cbar_label)
    cbar_ax = cbar.ax
    cbar_ax.tick_params(axis='both', which='minor', bottom='off', top='off', left='off', right='off', labelleft='off', labelright='off') 
    cbar_ax.tick_params(axis='y',    which='major', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on', pad=.4, width=1, length=1) #http://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.tick_params.html
    cbar_ax.tick_params(axis='both', which='major', labelsize=configs['plotting_configs']['cbar_labelsize'])
    # cbar.set_ticks([mn,md,mx])
    # cbar.set_ticklabels([mn,md,mx])
    # cbar_ax.get_yaxis().set_tick_params(which='major', direction='out',pad=.1,width=.2, right='on')
    # http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params
    
    ax.set_xlim([-2,xlim])
    ax.set_ylim([-2,ylim])
    
    ax.set_title(title)
    ax.set_xlabel (configs['plotting_configs']['xlabel'])
    ax.set_ylabel (configs['plotting_configs']['ylabel'])
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks          

    return True
#-----------------------------------------------------------------
