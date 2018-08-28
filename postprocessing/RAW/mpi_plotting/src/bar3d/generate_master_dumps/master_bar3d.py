import sys, os
sys.path.insert(0, '../plot_master_dumps')
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

import matplotlib.font_manager as font_manager
font_path = util.slash(os.getenv('HOME'))+'.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
prop = font_manager.FontProperties(fname=font_path)
rcParams['font.family'] = prop.get_name() 

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

import offline_mass_plotter as plotter
default_colors   =  plotter.get_COLORS()
default_measure  =  plotter.get_MEASURES()[0]
default_norm     =  plotter.get_NORMS()[0]

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
                                    'zlabel':                 "$effective$ $total$  $benefits$",
                                    'alpha':                 .9,
                                    'wspace':                0.1,
                                    'hspace':                0.1,
                                    'projection':            None,
                                    'dpi':                   configs['dpi'],
                                    'elev':                   25, # this tilts it north-south
                                    'azim':                  -38, # this tilts it east-west
                                    'dx':                     0.3, # the bar width
                                    'dy':                     0.3, # the bar depth
                                    'bar_spacing':            1,
                                    'xticklabels':           ['100','75','50','25','20','15','10','5','1','0.1'], 
                                    'yticklabels':           ['100','75','50','25','20','15','10','5','1','0.1'],
                                    'file_extension':         '.svg'
                            }
    
    configs['master_log'] = configs['logs_dir']+"master_"+configs['timestamp']+".log"
    reporter              = open (configs['master_log'], 'a')
    reporter.write ("\n====================================\nmaster says: supervising\n====================================\n")
    print          ("\n====================================\nmaster says: supervising\n====================================\n")        
    
    available_workers, needed_workers, DONEs  = num_workers, 0, []
    configs['watchlist']      = 0
    
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            if 'done' in f.split('.'):
                #worker_xxxx_figure_0001_rows_0006_cols_0004_pos_0001.done
                DONEs.append (f[11:])
    
    AXES, FIGURES, file_no, row_no, col_no, pos = [], [], 0, 0, 0, 0

    for file in sorted(configs['input_files']):
        if needed_workers  >= available_workers:
            break
        file_no    += 1
        csv_files   = open(file.strip(), 'r').readlines()
                
        total_rows  = math.ceil(len(csv_files)/configs['columns'])
        total_cols  = configs['columns']
        PAIRS       = util.getDirsPairs (csv_files, min(len(csv_files), configs['files_per_pair']))               
        
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

    file_no, rows, cols, pos, prefix, dir_path, title, processing_bit, ZLIMS, DICT_of_AVGs = load[0], load[1], load[2], load[3], load[4], load[5], load[6], load[7], load[8], load[9]
    title = update_title(DICT_of_AVGs,title)+','+default_measure+','+default_norm
    reporter.write ("\n\tmaster says: plotting file no "+str(file_no)+", coordinates \t\t"+str(rows)+", "+str(cols)+", "+str(pos))
    print          ("\tmaster says: plotting file no "  +str(file_no)+", coordinates \t\t"+str(rows)+", "+str(cols)+", "+str(pos))
    ax = FIGURES[file_no-1].add_subplot (rows, cols, pos,  projection='3d')
    plot_next_bar3d (FIGURES[file_no-1], ax, title, ZLIMS[default_measure][default_norm], DICT_of_AVGs, configs)
    
    with open (util.slash(configs['master_dump'])+str(file_no).rjust(3,'0')+"_"+str(rows).rjust(3,'0')+"x"+str(cols).rjust(3,'0')+"x"+str(pos).rjust(3,'0')+".dump", 'wb') as f:
        pickle.dump([title, ZLIMS, DICT_of_AVGs], f)
        
    
    return True
#-----------------------------------------------------------------
def plot_next_bar3d (fig, ax, title, zlim, DICT_of_AVGs, configs, colors=default_colors, measure=default_measure, norm=default_norm):
    #  DICT_of_AVGs   = { (p,t): {'Bin': {'TOT':0,'EFF':0}, 'Bou':{'TOT':0,'EFF':0}, 'Din':{'TOT':0,'EFF':0}, 'Dou':{'TOT':0,'EFF':0}    }    } 
    #  ZLIMS          =          {'Bin': {'TOT':0,'EFF':0}, 'Bou':{'TOT':0,'EFF':0}, 'Din':{'TOT':0,'EFF':0}, 'Dou':{'TOT':0,'EFF':0}    }

    Measure_dict = {}
    for p,t in DICT_of_AVGs.keys():
        Measure_dict[(p,t)] = DICT_of_AVGs[(p,t)][measure][norm] 
    
    
    dim1 = len ( set([pt[0] for pt in sorted(Measure_dict.keys())]) )
    dim2 = len ( set([pt[1] for pt in sorted(Measure_dict.keys())]) )
    
    ax, dx, dy, xcoordinates, ycoordinates = init_ax(ax, title, zlim, dim1, dim2, configs)

    dz = []
    for pt in sorted(Measure_dict.keys(),reverse=True):
        dz.append(Measure_dict[pt])
    
    dz                                = (np.array(dz)).reshape(dim1, dim2)
    zcoordinates                      = [0.0]*dim1*dim2 # can be non-zero if you want to stack slices of bars on top of each other    
    xcoordinates, ycoordinates        = np.meshgrid (xcoordinates, ycoordinates )               
    dz, ycoordinates, xcoordinates    = dz.flatten(), ycoordinates.flatten(), xcoordinates.flatten()
       
    #c = next(colors[measure])
    c = colors[measure]
    #-----------------------------------------------------------------------------------------------------------------------------------------------------
    ax.bar3d (xcoordinates, ycoordinates, zcoordinates, dx, dy, dz , alpha=configs['plotting_configs']['alpha'], color=c, edgecolor='')  #
    #----------------------------------------------------------------------------------------------------------------------------------------------------- 

    return True
#-----------------------------------------------------------------      
def plot_next_stacked_bar3d (fig, ax, title, zlim, DICT_of_AVGs, configs, colors=default_colors, measure=default_measure, norm=default_norm):
    #  DICT_of_AVGs   = { (p,t): {'SBin': {b: frequency}    }    } 
    title = update_title(DICT_of_AVGs, title)
    num_instances_dict  = {}
    Measure_dict        = {}
    distinct_increments = []
    for p,t in DICT_of_AVGs.keys():
        Measure_dict[(p,t)]       = DICT_of_AVGs[(p,t)][measure] # DICT_of_AVGs[(p,t)][measure] = {key:contrib}, contrib is before normalizing by no. instances
        num_instances_dict[(p,t)] = DICT_of_AVGs[(p,t)]['num_instances']
        distinct_increments += ([k for k in DICT_of_AVGs[(p,t)][measure].keys()])
       
    distinct_increments = sorted(list(set(distinct_increments)))

    dim1 = len ( set([pt[0] for pt in sorted(Measure_dict.keys())]) )
    dim2 = len ( set([pt[1] for pt in sorted(Measure_dict.keys())]) )  
    ax, dx, dy, xcoordinates, ycoordinates = init_ax(ax, title, zlim, dim1, dim2, configs)   
    xcoordinates, ycoordinates        = np.meshgrid (xcoordinates, ycoordinates )               
    ycoordinates, xcoordinates        = ycoordinates.flatten(), xcoordinates.flatten()    
    c             = colors[measure]
    interval      = 1
    if len(distinct_increments) > len(c):
        c += c[-1]*(distinct_increments-len(c)) # if there are more slices than there are colors, make more clones of the last (darkest) color
    else:
        interval      = math.floor(float(len(c))/len(distinct_increments))
    colors_steps  = [i for i in range(len(c)) if i%interval==0]
    '''
    print (str("\n\ncolors_steps "+str(colors_steps)))
    print ("interval "+str(interval))
    print ("len(c) "+str(len(c)))
    print ("len(colors_steps) "+str(len(colors_steps)))
    print ("len(distinct_increments) "+str(len(distinct_increments)))
    '''
    
    i, zcoordinates                      = 0, [0.0]*dim1*dim2 # can be non-zero if you want to stack slices of bars on top of each other 
    sys.stdout.write (" \n\tslice("+str(len(distinct_increments))+"): ")
    sys.stdout.flush()
    for inc in distinct_increments:
        sys.stdout.write (str(inc)+'>')
        sys.stdout.flush()
        dz = []   
        for pt in sorted(Measure_dict.keys(),reverse=True):
            if inc in Measure_dict[pt].keys():
                value      = inc
                frequency  = Measure_dict[pt][inc]
                normalizer = num_instances_dict[pt] 
                dz.append((value*frequency)/normalizer)
            else:
                dz.append(0)
        dz  = (np.array(dz)).reshape(dim1, dim2)
        dz  = dz.flatten()
        #print("\n\n"+str(dz))
        #-----------------------------------------------------------------------------------------------------------------------------------------------------
        ax.bar3d (xcoordinates, ycoordinates, zcoordinates, dx, dy, dz , alpha=1, color=c[colors_steps[i]], edgecolor='',linewidth=0.0)  #
        #----------------------------------------------------------------------------------------------------------------------------------------------------- 
        zcoordinates = [float(delta[0])+float(delta[1]) for delta in zip(dz, zcoordinates)]
        i+=1
    
    return True
#-----------------------------------------------------------------      
def init_ax(ax, title, zlim, dim1, dim2, configs):
   
    ax.set_title(title)
    dx = [configs['plotting_configs']['dx']]*(dim1*dim2)     #bar_width
    dy = [configs['plotting_configs']['dy']]*(dim1*dim2)     #bar length
    
    xcoordinates, ycoordinates = get_xy_coordinates(dim1, dim2, configs) 
    ax.set_xticks (  xcoordinates  )
    ax.set_yticks (  ycoordinates  )
    #ax.set_zticks (  range(5,int(zlim)+1,math.ceil(float(zlim+1)/5.0))         )
 
    ax.set_xticklabels (configs['plotting_configs']['xticklabels'], rotation=-45, verticalalignment='baseline', horizontalalignment='right')    #ax.w_xaxis.set_ticklabels(['0.1','1','5','10','15','20','25','50','75','100'])
    ax.set_yticklabels (configs['plotting_configs']['yticklabels'], rotation=-45, verticalalignment='baseline', horizontalalignment='left')    #ax.w_yaxis.set_ticklabels(['100','75','50','25','20','15','10','5','1','0.1'])    
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
    
    xcoordinates = [float(x)+float(configs['plotting_configs']['dx']) for x in range(dim1)]        # [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
    ycoordinates = [float(y)-float(configs['plotting_configs']['dx']) for y in range(dim2, 0, -1)] # [9.5, 8.5, 7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 1.5, 0.5] 
    
    return xcoordinates, ycoordinates
#--------------------------------------------------------------------------------------  
def update_title(DICT_of_AVGs,title):
    num_instances = []
    for p,t in DICT_of_AVGs.keys():
        num_instances.append(int(DICT_of_AVGs[(p,t)]['num_instances']))
    num_instances=list(set(num_instances))
    if len(num_instances)>1:
        smallest = util.pf(min(num_instances))
        biggest  = util.pf(max(num_instances))
        title    = title+','+str(smallest)+'-'+str(biggest)+' instances'
    else:
        if len(num_instances)==1:
            title    = title+','+str(util.pf(num_instances[0]))+' instances'
    return title
#--------------------------------------------------------------------------------------  