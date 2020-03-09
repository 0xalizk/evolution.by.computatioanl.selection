import sys, os
sys.path.insert(0, os.getenv('lib'))
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import  socket, math, time, numpy as np
from matplotlib import rcParams
import init_plotting as init, util_plotting as util, pickle


rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 8
rcParams['xtick.labelsize'] = 6
rcParams['ytick.labelsize'] = 6 
rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
rcParams['grid.alpha'] = 0.1
rcParams['axes.grid']=False
rcParams['ytick.minor.pad']=0.01
rcParams['ytick.major.pad']=0.01
rcParams['savefig.pad_inches']=.01
rcParams['grid.color']='white'

#-----------------------------------------------------------------
def supervise (configs_file, num_workers):

    configs                     = init.load_simulation_configs (configs_file, 0)
    configs['num_workers']      = num_workers
    configs['plotting_configs'] = {
                                    'fig_suptitle':          "Effective knapsack value", 
                                    'fig_suptitle_fontsize': 18,             
                                    'plot':                  "bar3d",
                                    'xlabel':                "$tolerance (\% edges)$", 
                                    'ylabel':                "$pressure (\% nodes)$",
                                    'zlabel':                 "Effective knapsack value (total benefits)",
                                    'alpha':                 0.7,
                                    'wspace':                0.01,
                                    'hspace':                0.01,
                                    'projection':            None,
                                    'dpi':                   300,
                                    'elev':                   25, # this tilts it north-south
                                    'azim':                  -38, # this tilts it east-west
                                    'bar_color':              (0.17139562607980241, 0.56203001457102153, 0.29233373017872077), #(0.017762399946942051, 0.42205306501949535, 0.22177624351838054)
                                    'dx':                     0.3, # the bar width
                                    'dy':                     0.3, # the bar depth
                                    'xticklabels':           ['100','75','50','25','20','15','10','5','1','0.1'], 
                                    'yticklabels':           ['100','75','50','25','20','15','10','5','1','0.1']
                            }
    
    configs['master_log'] = configs['logs_dir']+"master_"+configs['timestamp']+".log"
    reporter              = open (configs['master_log'], 'a')
    reporter.write ("\n====================================\nmaster says: supervising\n====================================\n")
    print          ("\n====================================\nmaster says: supervising\n====================================\n")        
    
    available_workers, needed_workers, number_of_plots, DONEs  = num_workers, 0,0,[]
    configs['watchlist']      = 0
    
    for file in configs['input_files']:
        number_of_plots  +=   len(open(file.strip(), 'r').readlines())
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            if 'done' in f.split('.'):
                #worker_xxxx_figure_0001_rows_0006_cols_0004_pos_0001.done
                DONEs.append (f[11:])
    
    AXES, FIGURES, file_no, row_no, col_no, pos = [], [], 0, 0, 0, 0

    for file in configs['input_files']:
        if needed_workers  >= available_workers:
            break
        file_no    += 1
        csv_files   = open(file.strip(), 'r').readlines()
                
        total_rows  = math.ceil(len(csv_files)/configs['columns'])
        total_cols  = configs['columns']
        PAIRS       = util.getDirsPairs (csv_files, configs['columns'])                
        
        #--------------------------------------------------------------------------------
        figure_size             = (12*total_cols, 3*(max(total_rows,2))) #(width, height)
        #--------------------------------------------------------------------------------
        FIGURES.append(plt.figure(figsize=figure_size))
        y = 1.2 
        if total_rows>2:
            y=1
        FIGURES[-1].suptitle('\n'+configs['plotting_configs']['fig_suptitle'], fontsize=configs['plotting_configs']['fig_suptitle_fontsize'], y=y       )  
        FIGURES[-1].subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['plotting_configs']['wspace'], hspace=configs['plotting_configs']['hspace'] )
        
        pos = 1   
        for pair in PAIRS: # a pair for each worker 
            if len(pair)>0:
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
        print ("\n\tmaster says: WARNING: available_workers < needed_workers, "+str(needed_workers - available_workers)+" subplots will not be plotted ")
        reporter.write("\n\nmaster says: WARNING: available_workers < needed_workers,"+str(needed_workers - available_workers)+" subplots will not be plotted ")

    next_ax=0
    for rank in range(1, min(available_workers, len(AXES))+1, 1): # num_workers == num pairs
        with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'wb') as f:               
            configs['AXES']  = [AXES[next_ax]]
            pickle.dump(configs, f)
            f.close()
            next_ax+=1
    
    #send empty AXES to these extra workers
    if available_workers > len(AXES) :
        for rank in range(len(AXES)+1, available_workers+1,1):
            with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'wb') as f:   
                configs['AXES']= []
                pickle.dump(configs, f)
                f.close()
    print ("\n\tmaster says: WORKERS:  avail "+str(available_workers)+", assigned: "+str(next_ax)+", needed: "+str(needed_workers)+", len(AXES) "+str(len(AXES))+", len(DONEs) "+str(len(DONEs))+"\n")
    reporter.write("\n\tmaster says: WORKERS:  avail "+str(available_workers)+", assigned: "+str(next_ax)+", needed: "+str(needed_workers)+", len(AXES) "+str(len(AXES))+", len(DONEs) "+str(len(DONEs))+"\n")
    
    configs['master_dump'] = util.slash(configs['output_dir'])+"master_dump/"
    if not os.path.isdir(configs['master_dump']):
        try:
            os.makedirs(configs['master_dump'])
        except:
            print          ("\n\tOoops: couldn't create master_dump (a message from master.supervise()). This may cause problems later in master.havest()")
            reporter.write ("\n\tOoops: couldn't create master_dump (a message from master.supervise()). This may cause problems later in master.havest()")
            pass
    
    #not serializable, append it after pickle dump
    #configs['plotting_configs']['cmap'] = plt.cm.get_cmap('plasma')
    #configs['plotting_configs']['marker'] = mpl.markers.MarkerStyle(marker='+', fillstyle=None)

    reporter.flush()
    reporter.close()

    watch (configs, FIGURES, AXES)
#-----------------------------------------------------------------
def watch (configs, FIGURES, AXES):
    t0 = time.time()
    reporter = open (configs['master_log'], 'a')
    if len (AXES) == 0:
        print         ("\tmaster says: len(AXES)==0, I'm exiting, goodnight")
        reporter.write("\n\tmaster says: len(AXES)==0, Im exiting, goodnight")
        reporter.flush()
    else:    
        total_plots = configs['watchlist']
        print ("\tmaster says: watching "+str(total_plots) +" subplots")
        reporter.write ("\n\tmaster says: watching "+str(total_plots) +"  subplots")
        reporter.flush()
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
                            reporter.write("\n\tmaster says: harvesting ("+str(counter).rjust(3,'0')+"): "+f.split('/')[-1])
                            reporter.flush()                            
        i=1
        for fig in FIGURES:
            #fig.tight_layout()
            print ("\n\tmaster says: saving figure no. "+str(i)+": "+util.slash(configs['plots_dir'])+str(i).rjust(3,'0')+"_"+configs['timestamp']+"."+configs['file_extension'])
            reporter.write("\n\tmaster says: saving "+str(i))
            fig.savefig(util.slash(configs['plots_dir'])+str(i).rjust(3,'0')+"_"+configs['timestamp']+"."+configs['file_extension'], dpi=configs['plotting_configs']['dpi'], bbox_inches="tight")
            i+=1
        
        t1 = time.time()
        reporter = open (configs['master_log'], 'a')
        reporter.write ("\n\tmaster says: harvested "+str(counter)+" plots in "+str(int(t1-t0))+" seconds")
        reporter.flush()
        reporter.close()
        print ("\tmaster says: harvested "+str(counter)+" files in "+str(int(t1-t0))+" seconds")           
#-----------------------------------------------------------------
def harvest(configs, file, AXES, FIGURES):
    reporter = open (configs['master_log'], 'a')
    load=''
    with open(file,'rb') as f:
        load = pickle.load(f)

    file_no, rows, cols, pos, prefix, dir_path, title, processing_bit, zlim, Bin_dict = load[0], load[1], load[2], load[3], load[4], load[5], load[6], load[7], load[8], load[9]
    reporter.write ("\n\tmaster says: plotting file no "+str(file_no)+", coordinates \t\t"+str(rows)+", "+str(cols)+", "+str(pos))
    print          ("\tmaster says: plotting file no "  +str(file_no)+", coordinates \t\t"+str(rows)+", "+str(cols)+", "+str(pos))
    ax = FIGURES[file_no-1].add_subplot (rows, cols, pos,  projection='3d')
    plot_next_bar3d (FIGURES[file_no-1], ax, title, zlim, Bin_dict, configs)
    
    with open (configs['master_dump']+str(file_no).rjust(3,'0')+"_"+str(rows).rjust(3,'0')+"x"+str(cols).rjust(3,'0')+"x"+str(pos).rjust(3,'0')+".dump", 'wb') as f:
        pickle.dump([title, zlim, Bin_dict], f)
        
    
    return True
#-----------------------------------------------------------------
def plot_next_bar3d (fig, ax, title, zlim, Bin_dict, configs):
    # Bin_dict = {(p,t):Bin}
    dim1= len ( set([pt[0] for pt in sorted(Bin_dict.keys())]) )
    dim2= len ( set([pt[1] for pt in sorted(Bin_dict.keys())]) )
    
    ax, dx, dy, xcoordinates, ycoordinates = init_ax(ax, title, zlim, dim1, dim2, configs)

    dz = []
    for pt in sorted(Bin_dict.keys(),reverse=True):
        dz.append(Bin_dict[pt])
    
    dz                                = (np.array(dz)).reshape(dim1, dim2)
    zcoordinates                      = [0.0]*dim1*dim2 # can be non-zero if you want to stack slices of bars on top of each other    
    xcoordinates, ycoordinates        = np.meshgrid (xcoordinates, ycoordinates )               
    dz, ycoordinates, xcoordinates    = dz.flatten(), ycoordinates.flatten(), xcoordinates.flatten()
       
    #-----------------------------------------------------------------------------------------------------------------------------------------------------
    ax.bar3d (xcoordinates, ycoordinates, zcoordinates, dx, dy, dz , alpha=configs['plotting_configs']['alpha'], color=configs['plotting_configs']['bar_color'], edgecolor='')  #
    #----------------------------------------------------------------------------------------------------------------------------------------------------- 
    '''
    # Note: np.meshgrid gives arrays in (ny, nx) so we use 'F' to flatten xpos,
    # ypos in column-major order. For numpy >= 1.7, we could instead call meshgrid
    # with indexing='ij'.
    '''
    return True
#-----------------------------------------------------------------      
def init_ax(ax, title, zlim, dim1, dim2, configs):
    '''
    x  = [1,2,3]  			# x coordinates of each bar
    y  = [0,0,0]  			# y coordinates of each bar
    z  = [0,0,0]  			# z coordinates of each bar
    dx = [0.5, 0.5, 0.5]  	# width of each bar
    dy = [0.5, 0.5, 0.5]  	# depth of each bar
    dz = [z1,   z2,  z3]        	# height of each bar
    '''      
    ax.set_title(title)
    dx = [configs['plotting_configs']['dx']]*(dim1*dim2)     #bar_width
    dy = [configs['plotting_configs']['dy']]*(dim1*dim2)     #bar length
    
    xcoordinates, ycoordinates = get_xy_coordinates(dim1, dim2, configs) 
    ax.set_xticks (  xcoordinates  )
    ax.set_yticks (  ycoordinates  )
    #ax.set_zticks (  range(5,int(zlim)+1,math.ceil(float(zlim+1)/5.0))         )
 
    ax.set_xticklabels (configs['plotting_configs']['xticklabels'], rotation=-45, verticalalignment='baseline', horizontalalignment='right')    #ax.w_xaxis.set_ticklabels(['0.1','1','5','10','15','20','25','50','75','100'])
    ax.set_yticklabels (configs['plotting_configs']['yticklabels'] , rotation=-45, verticalalignment='baseline', horizontalalignment='left')    #ax.w_yaxis.set_ticklabels(['100','75','50','25','20','15','10','5','1','0.1'])    
    #ax.set_zticklabels ([str(zl) for zl in range(5,int(zlim)+1,5)])

    ax.set_xlabel (configs['plotting_configs']['xlabel'])
    ax.set_ylabel (configs['plotting_configs']['ylabel'])
    ax.set_zlabel (configs['plotting_configs']['zlabel'])
                
    ax.tick_params (axis='x', pad=0.1, width=1,length=1,labelsize=8,direction='in') #valid keywords: ['size', 'width', 'color', 'tickdir', 'pad', 'labelsize', 'labelcolor', 'zorder', 'gridOn', 'tick1On', 'tick2On', 'label1On', 'label2On', 'length', 'direction', 'left', 'bottom', 'right', 'top', 'labelleft', 'labelbottom', 'labelright', 'labeltop']
    ax.tick_params (axis='y', pad=0.1, width=1,length=1,labelsize=8,direction='in')
    ax.tick_params (axis='z', pad=0.1, width=1,length=1,labelsize=8,direction='in')
                
    ax.set_zlim   (top=zlim)
    ax.view_init  (elev=configs['plotting_configs']['elev'],azim=configs['plotting_configs']['azim'])
    return ax, dx, dy, xcoordinates, ycoordinates
#-------------------------------------------------------------------------------------- 
def get_xy_coordinates(dim1, dim2, configs):
    xcoordinates = [x+float(configs['plotting_configs']['dx'])/2 for x in range(dim1)]        # [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
    ycoordinates = [y-float(configs['plotting_configs']['dx'])/2 for y in range(dim2, 0, -1)] # [9.5, 8.5, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5, 0.5]
    return xcoordinates, ycoordinates
#--------------------------------------------------------------------------------------  
