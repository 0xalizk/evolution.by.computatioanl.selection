import sys, os
sys.path.insert(0, os.getenv('lib'))
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
import  math, numpy as np
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
from matplotlib import rcParams
from colour import Color
import util_plotting as util, master_plotter as master
##################################################################
mywrite = util.mywrite
##################################################################
def update_rcParams():
    font_path = os.getenv('HOME')+'/.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    mpl.rcParams['font.family'] = prop.get_name() 
    rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
    rcParams['grid.alpha'] = 0.1
    rcParams['axes.grid']=False
    rcParams['savefig.pad_inches']=.1
    rcParams['grid.color']='white'

    rcParams['axes.titlesize']   = 5
    rcParams['axes.titleweight'] = 'normal'
    rcParams['axes.linewidth']   = .5
    rcParams['axes.labelsize']   = 5
    rcParams['axes.labelpad']    = 2
    
    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  4
    rcParams['xtick.major.pad']    =  1
    rcParams['xtick.major.size']   =  3  # how long the tick is
    rcParams['xtick.major.width']  =  .4 
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  4  
    rcParams['ytick.major.pad']    =  1 
    rcParams['ytick.major.size']   =  3  
    rcParams['ytick.major.width']  =  .4  
    rcParams['ytick.minor.pad']    =  1  
    rcParams['ytick.minor.size']   =  1  
    rcParams['ytick.minor.width']  =  .25 
    rcParams['ytick.minor.visible']=  False
    
    rcParams['legend.fontsize']    =  4   
    rcParams['legend.handleheight']=  0.5 
    rcParams['legend.handlelength']=  1.0 
    rcParams['legend.frameon']     =  False
    rcParams['legend.labelspacing']=  .2 
    rcParams['legend.borderaxespad']=  .1    
##################################################################
def update_rcParams_scatter():
    font_path = util.slash(os.getenv('HOME'))+'.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = prop.get_name()
    #rcParams['font.family']        = 'Adobe Caslon Pro'  # cursive, http://matplotlib.org/examples/pylab_examples/fonts_demo.html
    rcParams['font.serif']         = 'Helvetica' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']

    rcParams['axes.labelsize'] = 8
    rcParams['axes.titlesize'] = 4
    rcParams['grid.alpha'] = 0.1
    rcParams['axes.grid']=False
    rcParams['savefig.pad_inches']=.01
    rcParams['grid.color']='white'

    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  4
    rcParams['xtick.major.pad']    =  1.0
    rcParams['xtick.major.size']   =  3.0      # how long the tick is
    rcParams['xtick.major.width']  =  0.5
    rcParams['xtick.minor.pad']    =  1.0
    rcParams['xtick.minor.size']   =  2.0
    rcParams['xtick.minor.width']  =  0.5
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  4
    rcParams['ytick.major.pad']    =  1.0
    rcParams['ytick.major.size']   =  3.0
    rcParams['ytick.major.width']  =  0.5
    rcParams['ytick.minor.pad']    =  4.0
    rcParams['ytick.minor.size']   =  4
    rcParams['ytick.minor.width']  =  0.5
    rcParams['ytick.minor.visible']=  False
###################################################
def scatter_formatter(t, _):
    if float(t) <1:
        return ''
    return str(int(t-1)) # because we added 1 to Bs and Ds to avoid problems with zero values in log axis scale #
################################################### 
def palette_and_patches(all_degrees):
    maxd              = max(all_degrees)
    mind              = min(all_degrees)
    start             = Color('#ff00c8')#Color("#ff33e0") 
    middle1           = Color('#e999ff')#Color('#9333ff') 
    middle2           = Color('#afcecc')#Color('#cfc9f8') # #3371ff
    end               = Color('#0f4dff')#Color('#33f3ff')
    
    jump1             = 1 # must be >= 1, larger values = less distinct colors; increase it if start and middle are far-apart colors
    jump2             = 1
    cutoff_degree     = min(4,math.ceil(maxd/2.0)) # must be >= 1

    palette_size1     = math.ceil(math.log(cutoff_degree,2)) + 1
    palette_size2     = math.ceil(math.log(maxd,2)) - math.floor(math.log(cutoff_degree,2)) 
    #print('\nmaxd '+str(maxd))
    #print('cutoff_degree '+str(cutoff_degree))
    #print('palette_size1 '+str(palette_size1))
    #print('palette_size2 '+str(palette_size2))       
    under_cutoff      = list(start.range_to   (middle1, max(1,palette_size1*jump1)))
    above_cutoff      = list(middle2.range_to (end,     max(1,palette_size2*jump2)))


    palette = {}
    for deg in range (1, maxd+1,1):
        if deg <= cutoff_degree:
            index = math.ceil(math.log(deg,2)) + (jump1-1)
            palette[deg] = under_cutoff[index].rgb
        else:
            index = math.ceil(math.log(maxd,2)) - math.ceil(math.log(deg,2)) + (jump2-1)
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
################################################### 
def formatter(y, _):
    if int(y) == float(y) and float(y)>0:
        return str(int(y))+' %' 
    elif float(y) >= .1:
        return str(y)+' %'
    else:
        return ""
################################################### 
def rescale (R, a,b):
    scaled = []
    minv = min(R)
    maxv = max(R)
    numerator = maxv-minv
    for r in R:
        scaled.append((((b-a)*(r-minv))/numerator) + a)
    return scaled
################################################### 
def cFactory(start_color='white',end_color='black', num_colors=256):
    start = Color(start_color)
    end   = Color(end_color)
    return [c.rgb for c in start.range_to(end, num_colors)]
################################################### 
def getCOLORS(csv):
    
    '''
    #Vinayagam_RAW_INSTANCES_p100.0_t001.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02
    net_name = csv.split('/')[-1].split('_RAW_INSTANCES_')[0].lower()
    mode     = csv.split('/')[-1].split('_RAW_INSTANCES_')[1].split('_')[-2].lower() # reverse or scrambled
    key      = net_name+'-'+mode

    COLORS = {
               'vinayagam-reverse'    :cFactory(start_color='#c40092',end_color='#bbc400',num_colors=60),  
               'vinayagam-scramble'   :cFactory(start_color='#0800fe',end_color='#a6fdfd',num_colors=60), 
               'er_vinayagam-reverse' :cFactory(start_color='black',  end_color='white',  num_colors=60), 
               'er_vinayagam-scramble':cFactory(start_color='#ff9e00',end_color='#ffdda5',num_colors=60), 
               'default'              :cFactory(start_color='#c40092',end_color='#bbc400',num_colors=55)
    }
    if key in COLORS.keys():
        sys.stdout.flush()
        return COLORS[key]
    return #COLORS['default']
    '''
    return cFactory(start_color='#c40092',end_color='#bbc400',num_colors=55) 
################################################### 
def normalize(slices):
    for slice_id in slices.keys():
        total = sum(slices[slice_id].values())
        for degree in slices[slice_id].keys():
            slices[slice_id][degree] = (slices[slice_id][degree]/total)*100
################################################### 
def extract_stats(slices):
    slices2 = {}
    all_degrees = []
    group_labels = []
    for slice_id in sorted(slices['segments'].keys()):
        if slices['segments'][slice_id]['range']==(0,0):# skip 0:0 slice
            continue
        slices2[slice_id] = {}
        group_labels.append(slices['segments'][slice_id]['label'])
    for slice_id in slices2.keys():
        for degree in sorted(slices['segments'][slice_id]['degree_freq'].keys()):
            freq = slices['segments'][slice_id]['degree_freq'][degree]['avg_so_far']
            slices2[slice_id][degree] =  freq
            all_degrees.append(degree)
    all_degrees = sorted(list(set(all_degrees)), reverse=True)
    return slices2, all_degrees, group_labels
################################################### 
def customize_bar2d(ax, xlabels, xlabels_loc, title):
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.set_xticks(xlabels_loc)
    ax.set_xlabel('benefit:bamage ratio group')
    ax.set_ylabel('% degree makeup (log)')
    ax.set_title(title)
    ax.set_xticklabels(xlabels,rotation='vertical')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yscale('log', basey=10)#, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    ax.set_ylim([0,100]) # it matters where this line is, (it has to be before ticking is done i think)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    return ax
################################################### 
def customize_ETXbar2d(ax):
    update_rcParams()
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yscale('log', basey=10)#, linthreshy=.1)#, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    #ax.set_ylim([0,101]) # it matters where this line is, (it has to be before ticking is done i think)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    return ax
###################################################    
def plot_next_bar2d(harvest, FIGURES, log):
    update_rcParams()
    file_no, coords, pos, prefix, file_path, title, slices, worker_configs, rank = harvest['file_no'], harvest['coords'], harvest['pos'], harvest['prefix'], harvest['file_path'], harvest['title'], harvest['data'], harvest['worker_configs'], harvest['rank']
    ax = FIGURES[file_no-1].add_axes(coords)
    mywrite (log, "\n\tmaster says: plotting plot_next_bar2d of file no "+str(file_no)+" (from worker #"+str(rank)+"): "+str(title.replace('\n',' ').replace('$','')))

    DegFreqBySlice, all_degrees, group_labels = extract_stats (slices)
    palette, patches       = palette_and_patches(all_degrees)
    normalize(DegFreqBySlice) ### normalize to 0-100%  ####


    N          = len(DegFreqBySlice.keys())
    tickloc    = [t for t in range(1,N+1,1)]
    width      = .9      # the width of the bars: can also be len(x) sequence
    bottom = [0]*N
    #ax.set_xticklabels(group_labels)
    for deg in sorted(all_degrees, reverse=True): #all_degrees are increasingly sorted, this makes a nice log-scale bar
        next_stack     = []
        for slice_id in sorted(DegFreqBySlice.keys()):        
            if deg in DegFreqBySlice[slice_id].keys():
                next_stack.append(DegFreqBySlice[slice_id][deg])
            else:
                next_stack.append(0)
        ax.bar(tickloc, next_stack, width, color=palette[deg], align='center', alpha=.9, edgecolor='white',linewidth=0.1, bottom=bottom)#, yerr=womenStd)
        bottom = [b+m for b,m in zip(bottom, next_stack)]
    
    #ax.plot([0., max(tickloc)+(width/2.)], [25, 25], "--", color='black', linewidth=1) # linestyle='-/--/-./:'   
    ax   = customize_bar2d(ax, group_labels, tickloc, title) # IMPORTANT: should be called after ax.bar is done
    legend = ax.legend(handles=patches, loc=(.99,0.35), title='degree:') # http://matplotlib.org/api/legend_api.html#matplotlib.legend.Legend 
    legend.get_title().set_fontsize(5) # this is a must, can't do this thru rcParams
    return True
###################################################    
def plot_next_pie(harvest, FIGURES, log):
    update_rcParams()
    file_no, coords, pos, prefix, file_path, title, slices, configs, rank = harvest['file_no'], harvest['coords'], harvest['pos'], harvest['prefix'], harvest['file_path'], harvest['title'], harvest['data'], harvest['worker_configs'], harvest['rank']
    ax = FIGURES[file_no-1].add_axes(coords)
    mywrite (log, "\n\tmaster says: plotting plot_next_pie of file no "+str(file_no)+" (from worker #"+str(rank)+"): "+str(title.replace('\n',' ').replace('$','')))

    normalizer = 0 
    patch_labels = []
    
    #-------JSON serialization/deserialization results in all 'int' keys becoming 'str' -------------
    sorted_keys   = [key for key in sorted([int(key) for key in slices['segments'].keys()])]
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
                                         textprops={'family':family, 'color':'white', 'weight':'bold', 'fontsize':5} ) # , 'family':family,
            
    centre_circle = plt.Circle((0,0),0.3,color=None, fc='white',linewidth=0)    
    ax.add_artist(centre_circle)
 
    updated_patch_labels = []
    i=0 
    #with standard dev.
    for p,t in zip(patch_labels,autotexts):
        updated_patch_labels.append( p.ljust(8,' ') + ' ('+t.get_text()+'\u00B1'+str(round(slices['segments'][sorted_keys[i]]['std'],2))+')')
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
    
    ax.legend(patches, updated_patch_labels, loc=(.99,0.001), frameon=False)    
    #--------------------------------------------------------------------------------------        
    ax.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
    
    ax.set_xticks([])
    #ax.set_xticklabels([title])
    ax.set_xlabel (title) 
    #ax.text(.1, .5, "setosa", size=16, color='red')
    del slices
    return True
###################################################    
def plot_next_scatter(harvest, FIGURES, log):
    update_rcParams_scatter()

    file_no, coords, pos, prefix, file_path, title, data, configs, rank = harvest['file_no'], harvest['coords'], harvest['pos'], harvest['prefix'], harvest['file_path'], harvest['title'], harvest['data'], harvest['worker_configs'], harvest['rank']
    Bs, Ds, frequency, cbar_label, xlim, ylim = data['Bs'], data['Ds'], data['frequency'], data['cbar_label'], data['xlim'], data['ylim']  
    if pos==1:
        with open('harvest','wb') as f:
            import pickle
            pickle.dump(harvest,f)
    mywrite (log, "\n\tmaster says: plotting plot_next_pie of file no "+str(file_no)+" (from worker #"+str(rank)+"): "+str(title.replace('\n',' ').replace('$','')))

    ax = FIGURES[file_no-1].add_axes(coords)
    ax.set_xscale('log', basex=2)
    ax.set_yscale('log', basey=2)
        
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')

    for i in range(len(Bs)):
        Bs[i]+=1 # zero values cause problems with log scale, increment everything by 1 and change ticklabels accordingly
    for i in range(len(Ds)):
        Ds[i]+=1 # zero values cause problems with log scale, increment everything by 1 and change ticklabels accordingly     
    sizes=None
    if configs['mode']=='count':
        print('rescaling')
        sizes        = rescale( [2**f for f in frequency], 1,100)
    else:
        sizes        =[f*20 for f in frequency]

    #-----------------------------------------------------------------
    sc = ax.scatter (Ds, Bs, alpha=.5, marker='o', edgecolors='none',  c=frequency, s=sizes, cmap=plt.cm.get_cmap('winter'))                      
    #-----------------------------------------------------------------
    #mpl.markers.MarkerStyle(marker='+', fillstyle=None)
    ax.set_xlim([.5,xlim])
    ax.set_ylim([.5,ylim])
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(scatter_formatter))
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(scatter_formatter))  
    
    cbar = FIGURES[file_no-1].colorbar(sc, shrink=0.4, pad=0.01, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label(cbar_label)
    cbar_ax = cbar.ax
    cbar_ax.tick_params(axis='both', which='minor', bottom='off', top='off', left='off', right='off', labelleft='off', labelright='off') 
    cbar_ax.tick_params(axis='y',    which='major', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on', pad=.4, width=.2, length=1) #http://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.tick_params.html
    cbar_ax.tick_params(axis='both', which='major', labelsize=4)
    
    
    # cbar.set_ticks([mn,md,mx])
    # cbar.set_ticklabels([mn,md,mx])
    # cbar_ax.get_yaxis().set_tick_params(which='major', direction='out',pad=.1,width=.2, right='on')
    # http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params

    #ax.set_xlim([-2,xlim])
    #ax.set_ylim([-2,ylim])
    
    ax.set_title(title) 
    ax.set_xlabel ("benefit")
    ax.set_ylabel ("damage")
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks          

    return True
###################################################     
def plot_next_ETX(harvest, FIGURES, log):
    '''
        harvest  = 
                    {   
                        'file_path'      : ...
                        'file_no'        : ...
                        'prefix'         : ...
                        'title'          : ...
                        'rank'           : ...
                        'worker_configs' : ...
                        'processing_bit' : ...
                        'pos'            : ...           
                        'data'           : (p,t):{  'csv'          : path_to_pt_csv 
                                                    'num_instances : N
                                                    'DEGREES'        : {
                                                                            'deg': 
                                                                                { 'din': {'AsF': 0.0, 'CsF': 2.0}, 
                                                                                  'bou': {'AsF': 1.7222222222222223, 'CsF': 18.0}, 
                                                                                  'bin': {'AsF': 1.5, 'CsF': 2.0}, 
                                                                                  'dou': {'AsF': 2.0555555555555554, 'CsF': 18.0}
                                                                                }
                                                                                ..
                                                                                ..
                                                                     }
                    }
    
    Note:
        AsF means Average-so-Far
        CsF means Count-so-Far
    figures            = 1
    axes   per figure  = Ps    ax = FIGURES[file_no-1].add_axes(a coordinate based on P) #ignore axes set by supervisor, use the value of Ps to determine axes location
    groups per figure  = Ts
    bars   per group   = networks, use pos as network id, use title.split('\n')[0] as net name    
    '''
    # FIGURES[-1] = {'fig':plt.figure(figsize=figure_size), 'AXES':[ax0,ax1, .. axp]}
    update_rcParams()
    Ps                 = sorted(list(set([float(pt[0]) for pt in harvest['data'].keys()])), reverse=True)
    Ts                 = sorted(list(set([float(pt[1]) for pt in harvest['data'].keys()])), reverse=True)
    fig_index          = harvest['file_no']-1
    network_order      = harvest['pos']
    cols               = 1
    rows               = len(Ps)
    coords             = master.getCOORDs ((5,5*rows), cols, rows, w2h_ratio=0.7)
    bars_per_group     = harvest['worker_configs']['group_size'][harvest['file_no']]+1 # +1 as pads before  each group 
    group_axis_length  = 1.0
    num_groups         = len(Ts)

    bar_width          = group_axis_length/bars_per_group
    
    for p in range(len(Ps)):          # 0, 1, ... |Ps|-1
        for t in range(len(Ts)):           # 0, 1, ... |Ts|-1
            COLORS             = getCOLORS(harvest['data'][(Ps[p],Ts[t])]['csv'])
            #                 tick                  back to beginning of group       forward to the right bar
            offset = (t+1)*group_axis_length    -   (bar_width*bars_per_group)    +  harvest['pos']*bar_width
            bottom = 0
            ax = customize_ETXbar2d(FIGURES[fig_index]['AXES'][p])
            for deg in sorted(harvest['data'][(Ps[p], Ts[t])]['DEGREES'].keys(), reverse=True):
                next_stack =  harvest['data'][(Ps[p], Ts[t])]['DEGREES'][deg]['bin']['AsF'] #{'bou': {'AsF': 0.4285189390910202, 'CsF': 20.0}, 'bin': {'AsF': 0.4259386262615833, 'CsF': 20.0}, 'dou': {'AsF': 0.4286861575337804, 'CsF': 20.0}, 'din': {'AsF': 0.42819968024408767, 'CsF': 20.0}}
                ax.bar(offset, next_stack, bar_width, color=COLORS[deg-1], align='center', alpha=.7, edgecolor='white',linewidth=0.1, bottom=bottom)#, yerr=womenStd)
                bottom += next_stack
                #print (str(deg).ljust(5,' ')+str(next_stack))
    return True
###################################################     
def plot(harvest, FIGURES, log):
    if harvest['worker_configs']['cruncher'] in ['cruncher1','cruncher2','cruncher3','cruncher4']:
        if harvest['worker_configs']['cruncher'] == 'cruncher4':
            return plot_next_bar2d(harvest, FIGURES, log)
        else:
            return plot_next_pie(harvest, FIGURES, log)
    elif harvest['worker_configs']['cruncher'] == 'scatter':
        return plot_next_scatter(harvest, FIGURES, log)
    elif harvest['worker_configs']['cruncher'] == 'ETXcruncher1':
        return plot_next_ETX(harvest, FIGURES, log)
    else:
        mywrite(log, "\n\tplotters says: There is plotter for this cruncher .. moving on ..")
        return True  
###################################################
