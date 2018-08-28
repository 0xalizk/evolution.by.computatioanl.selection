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

rcParams['axes.labelsize'] = 8
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
                                'wspace':                0.4,
                                'hspace':                0.4,
                                'projection':            None,
                                'dpi':                   500,

                            }
   
    configs['slices']       = {     'interval':10,
                                    'segments':{
                                                 1  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                                                 2  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(90,10)},
                                                 3  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'80:20', 'range':(80,20)},
                                                 4  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'70:30', 'range':(70,30)},
                                                 5  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'60:40', 'range':(60,40)},
                                                 6  :{'fractions':[], 'count':0, 'color':'red', 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},                               
                                                 7  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'40:60', 'range':(40,60)},
                                                 8  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'30:70', 'range':(30,70)},
                                                 9  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'20:80', 'range':(20,80)},
                                                 10 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(10,90)}, 
                                                 11 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},                             
                               
                                                 12 :{'fractions':[], 'count':0, 'color':'black', 'avg':0, 'std':0, 'label':'0:0', 'range':(0,0)}
                                               }
                             }
    '''
    configs['slices']          = {   'interval':25,
                                     'segments':{
                                                  1 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                                                  2 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'75:25', 'range':(75,25)},
                                                  3 :{'fractions':[],  'count':0, 'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},
                                                  4 :{'fractions':[],  'count':0, 'color':None, 'avg':0, 'std':0, 'label':'25:75', 'range':(25,75)},
                                                  5 :{'fractions':[],  'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},
                               
                                                  6 :{'fractions':[], 'count':0, 'color':'black', 'avg':0, 'std':0, 'label':'0:0', 'range':(0,0)}
                                        }
                                  }     
    '''  
    configs['master_log'] = configs['logs_dir']+"master_"+configs['timestamp']+".log"
    reporter              = open (configs['master_log'], 'a')
    reporter.write ("\n====================================\nmaster says: supervising\n====================================\n")
    print          ("\n====================================\nmaster says: supervising\n====================================\n")        
    
    needed_workers            = 0
    assigned_workers          = 0
    available_workers         = num_workers
    DONEs =[]
    for root, dirs, files in os.walk(configs['DUMP_DIR']):
        for f in files:
            if 'done' in f.split('.'):
                #worker_xxxx_figure_0001_rows_0006_cols_0004_pos_0001.done
                DONEs.append (f[11:])
    for file in configs['input_files']:
        needed_workers  +=   len(open(file.strip(), 'r').readlines())
    #-------------------------------------------
    needed_workers = needed_workers - len(DONEs)
    #-------------------------------------------
    if available_workers < needed_workers:
        print ("\n\tmaster says: WARNING: available_workers < needed_workers, "+str(needed_workers - available_workers)+" subplots will not be plotted ")
        reporter.write("\n\nmaster says: WARNING: available_workers < needed_workers,"+str(needed_workers - available_workers)+" subplots will not be plotted ")

   
    AXES      = []
    FIGURES   = []
    file_no   = 0      #an index to a svg files
    row_no    = 0      #an index to a row
    col_no    = 0      #an index to a column
    for file in configs['input_files']:
        if assigned_workers >= available_workers:
            break
        file_no    += 1
        csv_files   = open(file.strip(), 'r').readlines()
                
        total_rows  = math.ceil(len(csv_files)/configs['columns'])
        total_cols  = configs['columns']
        PAIRS       = util.getPairs (csv_files, configs['columns'])                
        
        figure_size             = (5*total_cols, 3*(max(total_rows,2))) #(width, height)
        FIGURES.append(plt.figure(figsize=figure_size))
        y = 1.2 
        if total_rows>2:
            y=1
        FIGURES[-1].suptitle('\n'+configs['plotting_configs']['fig_suptitle'], fontsize=configs['plotting_configs']['fig_suptitle_fontsize'], y=y       )  
        FIGURES[-1].subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['plotting_configs']['wspace'], hspace=configs['plotting_configs']['hspace'] )
        
        pos = 1
        for pair in PAIRS: 
            if assigned_workers >= available_workers:
                break
            for tuple in pair:
                #configs['DUMP_DIR'] + "worker_"+str(rank).rjust(4,'0')+ "_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(rows).rjust(4,'0')+ "_cols_"+str(cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')
                #worker_0001_figure_0001_rows_0006_cols_0004_pos_0001.done
                if ("_figure_"+str(file_no).rjust(4,'0')+ "_rows_"+str(total_rows).rjust(4,'0')+ "_cols_"+str(total_cols).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')+'.done') not in DONEs:
                    AXES.append((file_no, total_rows, total_cols, pos, tuple[0], tuple[1], tuple[2]))
                    assigned_workers += 1
                    if assigned_workers >= available_workers:
                        break
                pos    += 1
    #avail 23, assigned: 23, needed: 19, len(AXES) 23
    print ("\n\tmaster says: WORKERS:  avail "+str(available_workers)+", assigned: "+str(assigned_workers)+", needed: "+str(needed_workers)+", len(AXES) "+str(len(AXES))+", len(DONEs) "+str(len(DONEs))+"\n")
    reporter.write("\n\tmaster says: WORKERS:  avail "+str(available_workers)+", assigned: "+str(assigned_workers)+", needed: "+str(needed_workers)+", len(AXES) "+str(len(AXES))+", len(DONEs) "+str(len(DONEs))+"\n")
    next_ax=0
    for rank in range(1, assigned_workers+1, 1): # num_workers == num pairs
        with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'w') as f:   
            
            configs['AXES']  = [AXES[next_ax]]
            json.dump(configs, f)
            f.close()
            next_ax+=1

    #send empty AXES to these extra workers
    if available_workers > assigned_workers:
        for rank in range(assigned_workers+1, available_workers+1, 1):
            with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'w') as f:   
                configs['AXES']= []
                json.dump(configs, f)
                f.close()
    configs['watchlist'] = len(DONEs) + assigned_workers      
    #not serializable, append it after json dump
    configs['plotting_configs']['cmap'] = plt.cm.get_cmap('plasma'),
    configs['num_workers'] = assigned_workers
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
    
    load=''
    with open(file,'r') as f:
        load = json.load(f)

    file_no, rows, cols, pos, prefix, file_path, title, slices = load[0], load[1], load[2], load[3], load[4], load[5], load[6], load[7]
    print ("\tmaster says: plotting file no "+str(file_no)+", coordinates \t\t"+str(rows)+", "+str(cols)+", "+str(pos))
    ax = FIGURES[file_no-1].add_subplot(rows, cols, pos)
    slices = assign_colors(slices)            
    
    
    return plot_next_pie(slices, ax, title)
#-----------------------------------------------------------------
def plot_next_pie(slices, ax, title):
    normalizer = 0 
    patch_labels = []
    
    #-------JSON serialization/deserialization results in all 'int' keys becoming 'str' -------------
    sorted_keys   = [str(key) for key in sorted([int(key) for key in slices['segments'].keys()])]
    #------------------------------------------------------------------------------------------------
    
    print ("sorted_keys: "+str(sorted_keys))
    for key in sorted_keys:
        slices['segments'][key]['avg'] = np.average (slices['segments'][key]['fractions'])
        slices['segments'][key]['std'] = np.std     (slices['segments'][key]['fractions'])
        normalizer          += slices['segments'][key]['avg']
        patch_labels.append(str(slices['segments'][key]['range']))
    
    #print ("\n\nnormalizer: "+str(normalizer))
    #patch_labels  = ['$b>0, d=0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b=0, d>0$']
    
    
    sizes         = [slices['segments'][key]['avg']/normalizer for key in sorted_keys]
    colors        = [slices['segments'][key]['color']          for key in sorted_keys]
    explode       = [0]*len(sorted_keys)  # only "explode" the 2nd slice (i.e. 'Hogs')
    print ("sizes: "+str(sizes))
    #-------------------------------------------------------------------------------------- 
    # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie
    patches, texts, autotexts = ax.pie (sizes, explode=explode, colors=colors,
                                         autopct='%1.1f%%', shadow=False, startangle=0, frame=False,
                                         wedgeprops = { 'linewidth': 0 },
                                         textprops={'color':'black', 'fontsize':8,'weight':'bold'} )
            
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

    for T in  autotexts:
        #T.set_text (str(T.get_text())+'\n\u00B1'+str(round(slices[sorted_keys[i]]['std'],2))+'%')
        T.set_text('')
    
    ax.legend(patches, updated_patch_labels, loc=(0.9,0.1), frameon=False, fontsize=8)    
    #--------------------------------------------------------------------------------------        
    ax.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
    
    ax.set_xticks([])
    #ax.set_xticklabels([title])
    ax.set_xlabel (title) 
    #ax.text(.1, .5, "setosa", size=16, color='red')
    return True
#-----------------------------------------------------------------
def assign_colors(slices):
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
#-----------------------------------------------------------------
