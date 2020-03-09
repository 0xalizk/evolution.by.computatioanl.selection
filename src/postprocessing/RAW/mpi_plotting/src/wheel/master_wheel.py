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
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
from colour import Color
import init_plotting as init, util_plotting as util, pickle
##################################################################
mywrite = util.mywrite
##################################################################
def update_rcParams():
    font_path = util.slash(os.getenv('HOME'))+'.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    mpl.rcParams['font.family'] = prop.get_name() 
    rcParams['axes.labelsize'] = 8
    rcParams['axes.titlesize'] = 8
    rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
    rcParams['grid.alpha'] = 0.1
    rcParams['axes.grid']=False
    rcParams['ytick.minor.pad']=0.01
    rcParams['ytick.major.pad']=0.01
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
    rcParams['ytick.major.pad']    =  2.0
    rcParams['ytick.major.size']   =  4.0
    rcParams['ytick.major.width']  =  1
    rcParams['ytick.minor.pad']    =  2.0
    rcParams['ytick.minor.size']   =  2
    rcParams['ytick.minor.width']  =  0.5
    rcParams['ytick.minor.visible']=  False
##################################################################
def get_plotting_configs(configs):
    return {
                'fig_suptitle':          "The Good, The Bad, and The Ugly", 
                'fig_suptitle_fontsize': 18,   
                'plot':                  "green_grey_red",
                'xlabel':                "B:D distribution", 
                'ylabel':                "fraction",
                'cbar_label':            None,
                'cbar_labelsize':        None,
                'marker':                None,
                'alpha':                 1,
                'cbar_labelsize':        None,
                'wspace':                0.6,
                'hspace':                0.4,
                'projection':            None,
                'dpi':                   configs['dpi'],

            }
##################################################################
def get_colors():
    return {
    
    'YlGn'   : [
              (0.95340254026300764, 0.98214532978394453, 0.7143252765431124), 
              (0.80090735519633571, 0.91955402248045981, 0.61531720862669104), 
              (0.59121877387458199, 0.82881969493978169, 0.5223068210424161), 
              (0.34540562244022593, 0.71501731802435486, 0.4107804743682637), 
              (0.17139562607980241, 0.56203001457102153, 0.29233373017872077), 
              (0.017762399946942051, 0.42205306501949535, 0.22177624351838054)],
    'BuGn'   : [
              (0.88535179460749902, 0.95621684228672699, 0.96682814499911141), 
              (0.74196079969406126, 0.90272972513647642, 0.86895810085184433), 
              (0.51607844771123401, 0.81085737382664402, 0.72735103509005383), 
              (0.31578624704304864, 0.71526337721768551, 0.53843907211341113), 
              (0.17139562607980241, 0.58492889825035543, 0.32635141365668352), 
              (0.017762399946942051, 0.44267590116052069, 0.18523645330877864)],
    
    'OrRd'   : [
              (0.9955709345200483, 0.8996539852198433, 0.76299886072383205), 
              (0.99215686321258545, 0.80292196484173051, 0.59001924781238335), 
              (0.99051134235718674, 0.65763938987956327, 0.44688967828657111), 
              (0.95864667682086724, 0.46189928428799498, 0.3103268086910248), 
              (0.87044983471141146, 0.24855056188854516, 0.16822760867721892), 
              (0.720230697183048, 0.024359862068120158, 0.01573241063777138)],
    'YlOrBr' : [
              (0.99949250291375558, 0.95847751112545243, 0.71543254291310032), 
              (0.99607843160629272, 0.85491734813241393, 0.4935178992795009), 
              (0.99607843160629272, 0.69787006798912499, 0.24727413414740096), 
              (0.95510957591673906, 0.50668205747417372, 0.11298731641442167), 
              (0.83641677253386559, 0.33900808341362898, 0.02832756745537706), 
              (0.62588237524032597, 0.21610150337219236, 0.014671281144461212)],
    'YlOrRd' : [
              (0.99949250291375558, 0.91926182718837968, 0.60613612111876991), 
              (0.99607843160629272, 0.80659747404210713, 0.41494810195530163), 
              (0.99443291075089402, 0.6371549620347865, 0.27171088778505137), 
              (0.98988081567427688, 0.40955019090689865, 0.19432526283404405), 
              (0.91864667920505294, 0.1611380281693795, 0.12573625740467334), 
              (0.76046137529260971, 0.013194925206549024, 0.14394464203540017)]
    }
##################################################################
def assign_colors_small(slices):
    
    colors = get_colors()
    
    green_cmap = colors['YlGn']
    red_cmap   = colors['YlOrRd']

    # after JSON dumping, int keys become str
    slices['segments'][1]['color'] = green_cmap[-2]
    slices['segments'][2]['color'] = green_cmap[-3]
    slices['segments'][3]['color'] = green_cmap[-4]
    slices['segments'][4]['color'] = green_cmap[-5]
    slices['segments'][5]['color'] = green_cmap[-6]
    
    slices['segments'][6]['color'] = 'grey'
    
    slices['segments'][7]['color'] = red_cmap[1]
    slices['segments'][8]['color'] = red_cmap[2]
    slices['segments'][9]['color'] = red_cmap[3]
    slices['segments'][10]['color']= red_cmap[4]
    slices['segments'][11]['color']= red_cmap[5]    
    
    slices['segments'][12]['color']= 'black' 
    
    return slices
##################################################################
def assign_colors_big(slices):
    
    colors = get_colors()

    green_cmap = colors['YlGn']
    red_cmap   = colors['YlOrRd']
    
    # after JSON dumping, int keys become str
    slices['segments'][1]['color'] = green_cmap[-2]
    slices['segments'][2]['color'] = green_cmap[-5]
    
    slices['segments'][3]['color'] = 'grey'
    
    slices['segments'][4]['color'] = red_cmap[1]
    slices['segments'][5]['color'] = red_cmap[4]

    slices['segments'][6]['color'] = 'black'


    return slices
##################################################################
def get_slices(configs):
    if configs['cruncher'] == 'cruncher4':
        return assign_colors_small ({    'interval':10,
                                         'segments':{
                                                 1  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                                                 2  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(90,10)},
                                                 3  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'80:20', 'range':(80,20)},
                                                 4  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'70:30', 'range':(70,30)},
                                                 5  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'60:40', 'range':(60,40)},
                                                 6  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},                               
                                                 7  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'40:60', 'range':(40,60)},
                                                 8  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'30:70', 'range':(30,70)},
                                                 9  :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'20:80', 'range':(20,80)},
                                                 10 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(10,90)}, 
                                                 11 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},                             
                                                 12 :{'degree_freq':{},  'color':None, 'avg':0, 'std':0, 'label':'0:0',   'range':(0,0)}
                                                }
                                })
    
    return assign_colors_small ({   'interval':10,
                                    'segments':{
                                                 1  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                                                 2  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(90,10)},
                                                 3  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'80:20', 'range':(80,20)},
                                                 4  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'70:30', 'range':(70,30)},
                                                 5  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'60:40', 'range':(60,40)},
                                                 6  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},                               
                                                 7  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'40:60', 'range':(40,60)},
                                                 8  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'30:70', 'range':(30,70)},
                                                 9  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'20:80', 'range':(20,80)},
                                                 10 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(10,90)}, 
                                                 11 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},                             
                                                 12 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:0', 'range':(0,0)}
                                                }
                                })
    '''
    return assign_colors_big ({      'interval':25,
                                     'segments':{
                                                  1 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                                                  2 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'75:25', 'range':(75,25)},
                                                  3 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},
                                                  4 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'25:75', 'range':(25,75)},
                                                  5 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},
                                                  6 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:0', 'range':(0,0)}
                                                }
                              })
    '''
##################################################################
def calculate_needed(DONEs, configs):
    no_csv = 0.0
    for file in configs['input_files']:
        no_csv += len(open(file.strip(), 'r').readlines())
    
    
    if (no_csv - len(DONEs)) <0:
        print("\nOOOOOOPS: something is terribly wrong, you may have changed the number of csv's since the last run, I'm ignoring this, fingers crossed.")
    else:
        no_csv = no_csv - len(DONEs)
    files_per_pair, pairs_per_worker = 1, 1 # defaults
    if 'files_per_pair' in configs.keys():
        files_per_pair = configs['files_per_pair']
        try:
            assert type(1) == type(files_per_pair) # make sure it's an integer
        except:
            files_per_pair = 1 # default
    if 'pairs_per_worker' in configs.keys():
        pairs_per_worker = configs['pairs_per_worker']
        try:
            assert type(1) == type(pairs_per_worker) # make sure it's an integer
        except:
            pairs_per_worker = 1 # default 
    
    return math.ceil(math.ceil(no_csv/float(files_per_pair))/float(pairs_per_worker))    
##################################################################   
def getDONEs(configs):
    DONEs = []
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            if 'done' in f.split('.'):
                #worker_xxxx_figure_0001_rows_0006_cols_0004_pos_0001.done
                DONEs.append (f[11:])
    return DONEs
##################################################################   
def supervise (configs_file, num_workers):
    update_rcParams()
    configs                     = init.load_simulation_configs (configs_file, 0)
    configs['num_workers']      = num_workers
    configs['master_log']       = configs['logs_dir']+"master_"+configs['timestamp']+".log"
    log                         = configs['master_log']
    configs['plotting_configs'] = get_plotting_configs(configs)
    configs['slices']           = get_slices(configs)
    configs['watchlist']        = 0
    DONEs                       = getDONEs(configs)
    needed_workers              = calculate_needed (DONEs, configs)
    available_workers           = num_workers
    mywrite(log, "\n====================================\nmaster says: supervising\n====================================\n")       
    
    assigned_workers, file_no, row_no, col_no, pos, augPAIRS, FIGURES = 0, 0, 0, 0, 0, [], []

    for file in sorted(configs['input_files']):
        file_no    += 1
        csv_files   = open(file.strip(), 'r').readlines()
                
        PAIRS          = util.getPairs (csv_files, min(len(csv_files), configs['files_per_pair']))            
        
        total_cols     = configs['columns']
        total_rows     = math.ceil(len(csv_files)/configs['columns'])
        if needed_workers > available_workers:
            total_plots = available_workers * (min(len(csv_files), configs['files_per_pair'])) * configs['pairs_per_worker']
            total_rows  = math.ceil(total_plots/configs['columns'])
            while total_rows*total_cols > total_plots:
                total_cols -= 1
        figure_size             = (5*total_cols, 3*(max(total_rows,2))) #(width, height)
        if configs['cruncher'] == 'cruncher4':
            figure_size             = (10*total_cols, 4*total_rows)
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
                if assigned_workers  >= available_workers or pos > (total_cols*total_rows):
                    break
                #worker_0001_figure_0001_rows_0006_cols_0004_pos_0001.done
                for tuple in pair:
                    if ("_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(total_rows).rjust(4,'0')+ "_cols_"+str(total_cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')+'.done') not in DONEs:
                        tmp.append((file_no, total_rows, total_cols, pos, tuple[0], tuple[1], tuple[2], 1))
                        print("yes: "+tuple[1].split('/')[-1])
                    else:
                        tmp.append((file_no, total_rows, total_cols, pos, tuple[0], tuple[1], tuple[2], 0))
                        print("no: "+tuple[1].split('/')[-1])
                
                    configs['watchlist'] += 1
                    pos                  += 1
            
                processing_bits = [b[7] for b in tmp] #b[7]=0 => don't process this file, it's done
                if sum(processing_bits)  > 0:
                    augPAIRS.append([t for t in tmp])
                    assigned_workers = float(len(augPAIRS))/configs['pairs_per_worker']
    WORK_LOAD = []
    while len(augPAIRS)>0:
        WORK_LOAD.append([pair for pair in augPAIRS[0:configs['pairs_per_worker']]])
        augPAIRS = augPAIRS[configs['pairs_per_worker']:]
    if available_workers < needed_workers:
        mywrite(log, "\n\tmaster says: WARNING: available_workers < needed_workers,"+str((needed_workers - available_workers)*configs['pairs_per_worker']*configs['files_per_pair'])+" subplots will not be plotted ")
    next_ax=0
    for rank in range(1, len(WORK_LOAD)+1, 1): # num_workers == num pairs
        with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'wb') as f:               
            configs['WORK_LOAD']  = WORK_LOAD[next_ax]
            pickle.dump(configs, f)
            f.close()
            next_ax+=1
    
    #send empty augPAIRS to these extra workers
    if available_workers > len(WORK_LOAD) :
        for rank in range(len(WORK_LOAD)+1, available_workers+1,1):
            with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'wb') as f:   
                configs['WORK_LOAD']= []
                pickle.dump(configs, f)
                f.close()
    #print ("assigned_workers "+str(assigned_workers)+", next_ax "+str(next_ax))
    assert math.ceil(assigned_workers) == next_ax 
    mywrite(log, "\n\tmaster says: WORKERS:  avail "+str(available_workers)+", assigned: "+str(next_ax)+", needed: "+str(needed_workers)+", len(WORK_LOAD) "+str(len(WORK_LOAD))+", len(DONEs) "+str(len(DONEs))+"\n")

    #not serializable, append it after pickle dump
    configs['plotting_configs']['cmap'] = plt.cm.get_cmap('plasma')
    configs['plotting_configs']['marker'] = mpl.markers.MarkerStyle(marker='+', fillstyle=None)

    watch (configs, FIGURES, WORK_LOAD)
##################################################################
def watch (configs, FIGURES, WORK_LOAD):
    log = configs['master_log']
    t0 = time.time()

    if len (WORK_LOAD) == 0:
        mywrite(log, "\n\tmaster says: len(WORK_LOAD)==0, I will re-harvest what's done previously anyway ")
    #else:    
    total_plots = configs['watchlist']
    mywrite (log, "\n\tmaster says: watching "+str(total_plots) +"  subplots")

    harvested_files  = [] 
    counter          = 0
    while counter < total_plots:
        time.sleep (30)
        for root, dirs, fs in os.walk(configs['DUMP_DIR']):
            confirmation = False
            for f in fs: # skip directories recently modified (1 minutes), workers may still be writing to them
                if 'done' in f.split('.') and f not in harvested_files:       
                    confirmation = harvest (configs, os.path.join(root, f), FIGURES)
                    if confirmation == True:
                        harvested_files.append(f)
                        counter += 1
                        mywrite(log, "\n\tmaster says: harvesting ("+str(counter).rjust(3,'0')+"): "+f.split('/')[-1])
                        
    i=1
    mode = ""
    try:
        mode = configs['cruncher']
    except:
        pass
    for fig in FIGURES:
        #fig.tight_layout()
        mywrite (log, "\n\tmaster says: saving figure no. "+str(i)+": "+util.slash(configs['plots_dir'])+str(i).rjust(3,'0')+"_"+configs['timestamp']+"."+configs['file_extension'])
        fig.savefig(util.slash(configs['plots_dir'])+"wheel_"+str(i).rjust(3,'0')+"_"+mode+"_"+str(configs['slices']['interval'])+"-interval_"+configs['timestamp']+"."+configs['file_extension'], dpi=configs['plotting_configs']['dpi'], bbox_inches="tight")
        i+=1
    
    t1 = time.time()
    mywrite (log, "\n\tmaster says: harvested "+str(counter)+" plots in "+str(int(t1-t0))+" seconds\n")         
##################################################################
def harvest(configs, file, FIGURES):
    log = configs['master_log']
    load=None
    with open(file,'rb') as f:
        load = pickle.load(f)

    file_no, rows, cols, pos, prefix, file_path, title, slices = load[0], load[1], load[2], load[3], load[4], load[5], load[6], load[7]
    mywrite (log, "\n\tmaster says: plotting file no "+str(file_no)+", coordinates \t\t"+str(rows)+", "+str(cols)+", "+str(pos))
    ax = FIGURES[file_no-1].add_subplot(rows, cols, pos)    
    if configs['cruncher'] == 'cruncher4':
        return plot_next_bar2d(slices, ax, title, configs)
    else:
        return plot_next_pie(slices, ax, title, configs)
##################################################################
def plot_next_pie(slices, ax, title, configs):
    log = configs['master_log']
    normalizer = 0 
    patch_labels = []
    
    #-------JSON serialization/deserialization results in all 'int' keys becoming 'str' -------------
    sorted_keys   = [str(key) for key in sorted([int(key) for key in slices['segments'].keys()])]
    #------------------------------------------------------------------------------------------------
    explode_index,i = 0,0
    for key in sorted_keys:
        slices['segments'][key]['avg'] = np.average (slices['segments'][key]['fractions'])
        slices['segments'][key]['std'] = np.std     (slices['segments'][key]['fractions'])
        normalizer          += slices['segments'][key]['avg']
        patch_labels.append(str(slices['segments'][key]['label']))
        if slices['segments'][key]['range'][0] == 50:
            explode_index = i
        i+=1
    #mywrite (log, "\n\nnormalizer: "+str(normalizer))
    #patch_labels  = ['$b>0, d=0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b=0, d>0$']
    
    
    sizes         = [slices['segments'][key]['avg']/normalizer for key in sorted_keys]
    colors        = [slices['segments'][key]['color']          for key in sorted_keys]
    
    explode       = [0]*len(sorted_keys)  # only "explode" the 2nd slice (i.e. 'Hogs')
    explode [explode_index] = .15
    #mywrite (log, "\nsizes: "+str(sizes))
    #-------------------------------------------------------------------------------------- 
    # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie
    #http://matplotlib.org/users/text_props.html
    font_path = util.slash(os.getenv('HOME'))+'.fonts/merriweather/Merriweather-Bold.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    family = prop.get_name() 
    patches, texts, autotexts = ax.pie (sizes, explode=explode, colors=colors,
                                         autopct='%1.1f%%', shadow=False, startangle=0, frame=False,
                                         wedgeprops = { 'linewidth': 0 },
                                         textprops={'family':family,'color':'white', 'fontsize':8,'weight':'bold'} )
            
    centre_circle = plt.Circle((0,0),0.3,color=None, fc='white',linewidth=0)    
    ax.add_artist(centre_circle)
 
    updated_patch_labels = []
    i=0 
    #with standard dev.
    for p,t in zip(patch_labels,autotexts):
        updated_patch_labels.append( p.ljust(8,' ') + ' ('+t.get_text().ljust(8,' ')+'\u00B1'+str(round(slices['segments'][sorted_keys[i]]['std'],2))+')')
        i+=1
    #without std. dev. 
    #updated_patch_labels=[p.ljust(8,' ') + ' '+t.get_text() for p,t in zip(patch_labels,autotexts)]

    i=0
    for T in  autotexts:
        #T.set_text (str(T.get_text())+'\n\u00B1'+str(round(slices[sorted_keys[i]]['std'],2))+'%')
        #if i not in [0,5,10]:
        if sizes[i] <0.1:# and i != 5:
            T.set_text('')
        i+=1
    
    ax.legend(patches, updated_patch_labels, loc=(1.02,0.1), frameon=False, fontsize=8)    
    #--------------------------------------------------------------------------------------        
    ax.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
    
    ax.set_xticks([])
    #ax.set_xticklabels([title])
    ax.set_xlabel (title) 
    #ax.text(.1, .5, "setosa", size=16, color='red')
    del slices
    return True
##################################################################
def palette_and_patches(all_degrees):
    mind              = min(all_degrees)
    maxd              = int(math.ceil(math.log(max(all_degrees),2)))
    start             = Color("#ff00ff") #0080ff # good pairs: (0080ff, e6e600), (#66ccff, #ff0066)
    middle            = Color('white') 
    end               = Color('#3399ff')
    jump              = 1
    cutoff_degree     = 8
    
    under_cutoff      = list(start.range_to(middle, (cutoff_degree *jump)+1))
    above_cutoff      = list(middle.range_to  (end, (maxd          *jump)+1))
    
    palette = {}
    for deg in range (1, max(all_degrees)+1,1):
        index = math.ceil(math.log(deg,2))
        if deg <= cutoff_degree:
            palette[deg] = under_cutoff[index].rgb
        else:
            palette[deg] = above_cutoff[index].rgb
    
    distinct_colors = []
    for deg in sorted(all_degrees):
        if palette[deg] not in distinct_colors:
            distinct_colors.append(palette[deg] )
    patches         = []
    for color in distinct_colors:
        current_range = []
        for deg in sorted(all_degrees):
            if palette[deg] == color:
                current_range.append(deg)
        label=None
        if len(current_range) > 1:
            label = str(min(current_range))+'-'+str(max(current_range))
        else:
            label = str(current_range[0])
        patches.append(mpatches.Patch(color=color, label=label))
    return palette, patches
##################################################################
def formatter(y, _):
    if int(y) == float(y) and float(y)>0:
        return str(int(y))+' %' 
    elif float(y) >= .1:
        return str(y)+' %'
    else:
        return ""
##################################################################
def normalize(slices):
    for slice_id in slices.keys():
        total = sum(slices[slice_id].values())
        for degree in slices[slice_id].keys():
            slices[slice_id][degree] = (slices[slice_id][degree]/total)*100
##################################################################
def extract_stats(slices):
    slices2 = {}
    all_degrees = []
    group_labels = []
    for slice_id in slices['segments'].keys():
        if slices['segments'][slice_id]['range']==(0,0):# skip 0:0 slice
            continue
        slices2[int(slice_id)] = {}
        group_labels.append(slices['segments'][slice_id]['label'])
    for slice_id in slices2.keys():
        for degree in sorted(slices['segments'][slice_id]['degree_freq'].keys()):
            freq = slices['segments'][slice_id]['degree_freq'][degree]['avg_so_far']
            slices2[slice_id][degree] =  freq
            all_degrees.append(degree) # pickle converts them to str
    all_degrees = sorted(list(set(all_degrees)), reverse=True)
    return slices2, all_degrees, group_labels
##################################################################
def customize_bar(slices, ax, title, xlabels):
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks
    ax.set_xticks(range(1,len(xlabels)+1,1))
    ax.set_xticklabels(xlabels)
    ax.set_xlabel('benefit:bamage ratio group')
    ax.set_ylabel('degree makeup of involved nodes (log)')
    ax.set_title(title+'\n')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yscale('log', basey=10)#, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    return ax
##################################################################
def plot_next_bar2d(slices, ax, title, configs):
    DegFreqBySlice, all_degrees, group_labels = extract_stats (slices)
    palette, patches       = palette_and_patches(all_degrees)
    normalize(DegFreqBySlice) ### normalize to 0-100%  ####


    N          = len(DegFreqBySlice.keys())
    tickloc    = [t for t in range(1,N+1,1)]
    width      = .9       # the width of the bars: can also be len(x) sequence
    bottom = [0]*N
    for deg in all_degrees: #all_degrees are decreasingly sorted, this makes a nice log-scale bar
        next_stack     = []
        for slice_id in sorted(DegFreqBySlice.keys()):        
            if deg in DegFreqBySlice[slice_id].keys():
                next_stack.append(DegFreqBySlice[slice_id][deg])
            else:
                next_stack.append(0)
        ax.bar(tickloc, next_stack, width, color=palette[deg], align='center', alpha=.9, edgecolor='white',linewidth=0.1, bottom=bottom)#, yerr=womenStd)
        bottom = [b+m for b,m in zip(bottom, next_stack)]

    ax   = customize_bar(slices, ax, title, group_labels) # IMPORTANT: should be called after ax.bar is done
    ax.legend(handles=patches, loc=(.99,0.35), frameon=False,handlelength=1.5,handleheight=1.5, labelspacing=.5, fontsize=10, title='degree', borderaxespad=1) # http://matplotlib.org/api/legend_api.html#matplotlib.legend.Legend 

    return True
##################################################################
def assign_colors_archive(slices):
    start       = 2
    skip        = 2
    distinction = len([key for key in slices['segments'].keys() if slices['segments'][key]['color']==None]) # the higher the more distinct the colors will be            
    colors  = [         iter(cm.GnBu     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.YlOrBr   (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.YlGn     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Spectral (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Blues    (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Dark2    (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Paired   (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Set1     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.jet      (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.cool     (np.linspace(0,1,  (distinction*(skip+1))+start))),    
                ] #http://matplotlib.org/users/colormaps.html    
    c = colors[4]
    for i in range(start):
        next(c)
        
    for key in sorted(slices['segments'].keys(), reverse=True):
        if slices['segments'][key]['color'] == None:
            for i in range(skip):
                next(c)
            slices['segments'][key]['color'] = next(c)
    return slices
##################################################################
