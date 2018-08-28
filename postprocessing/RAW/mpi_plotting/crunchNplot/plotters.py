import sys, os
sys.path.insert(0, os.getenv('lib'))
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
from matplotlib import rcParams
import matplotlib.colors as colors
from colour import Color
import  math, numpy as np
import util_plotting as util, master_plotter as master
##################################################################
mywrite = util.mywrite
##################################################################
def update_rcParams_pie():
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
def update_rcParams_bar2d():
    update_rcParams_pie()
    rcParams['axes.labelsize']   = 7
    rcParams['xtick.labelsize']    =  5
    rcParams['ytick.labelsize']    =  rcParams['xtick.labelsize']
    rcParams['ytick.major.pad']    =  0.5
    rcParams['ytick.minor.pad']    =  0.5
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
    rcParams['xtick.major.size']   =  2.5      # how long the tick is
    rcParams['xtick.major.width']  =  0.5
    rcParams['xtick.minor.pad']    =  1.0
    rcParams['xtick.minor.size']   =  2.5
    rcParams['xtick.minor.width']  =  0.5
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  4
    rcParams['ytick.major.pad']    =  2
    rcParams['ytick.major.size']   =  2.5
    rcParams['ytick.major.width']  =  0.5
    rcParams['ytick.minor.pad']    =  2.0
    rcParams['ytick.minor.size']   =  2.5
    rcParams['ytick.minor.width']  =  0.5
    rcParams['ytick.minor.visible']=  False
    return prop
###################################################
def scatter_formatter(t, _):
    if float(t) <1:
        return ''
    # because we added 1 to Bs and Ds to avoid problems with zero values in log axis scale #
    return str(int(t-1))
###################################################
def LogYformatter(y, _):
    if int(y) == float(y) and float(y)>0:
        return str(int(y))+' %'
    elif float(y) >= .0001:
        return str(y)+' %'
    else:
        return ""
###################################################
def rescale(R, a,b):
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
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='on',  labelleft='on', labelright='off') # both major and minor ticks
    ax.set_xticks(xlabels_loc)
    ax.set_xlabel('benefit:bamage ratio group')
    ax.set_ylabel('% degree makeup (log)')
    ax.set_title(title)
    ax.set_xticklabels(xlabels,rotation='vertical')
    ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    ax.set_yscale('log', basey=10)#, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    ax.set_ylim([0,100]) # it matters where this line is, (it has to be before ticking is done i think)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(LogYformatter))
    return ax
###################################################
def plot_next_bar2d(harvest, FIGURES, log):
    update_rcParams_bar2d()
    file_no, coords, pos, prefix, file_path, title, slices, worker_configs, rank = harvest['file_no'], harvest['coords'], harvest['pos'], harvest['prefix'], harvest['file_path'], harvest['title'], harvest['data'], harvest['worker_configs'], harvest['rank']
    ax = FIGURES[file_no-1].add_axes(coords)
    mywrite (log, "\n\tmaster says: plotting plot_next_bar2d of file no "+str(file_no)+" (from worker #"+str(rank)+"): "+str(title.replace('\n',' ').replace('$','')))

    DegFreqBySlice, all_degrees, group_labels = extract_stats (slices)
    palette, patches, legend_label       = master.palette_and_patches(worker_configs)
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
    legend = ax.legend(handles=patches, loc=(1.03,0.1), title='degree:') # http://matplotlib.org/api/legend_api.html#matplotlib.legend.Legend
    legend.get_title().set_fontsize(5) # this is a must, can't do this thru rcParams
    return True
###################################################
def plot_sSpace_bar2d(harvest, FIGURES, log):
    update_rcParams_bar2d()

    Ps                 = sorted(list(set([float(pt[0]) for pt in harvest['data'].keys()])), reverse=True)
    Ts                 = sorted(list(set([float(pt[1]) for pt in harvest['data'].keys()])), reverse=True)
    COLORS             = getCOLORS("")
    alpha_eff = harvest['worker_configs']['plotting_configs']['effectiveSearchSpacealpha']
    alpha_tot = harvest['worker_configs']['plotting_configs']['totalSearchSpacealpha']
    for p in Ps:
        AX        = FIGURES[harvest['file_no']-1]['AX'][p]
        bar_width = 0.9*AX['BAR_WIDTH']

        eff_color, tot_color = harvest['worker_configs']['effectiveSearchSpaceColor'], harvest['worker_configs']['totalSearchSpaceColor']
        for t in Ts:           # SORTED, important
            csv       = harvest['data'][(p,t)]['csv'] #util.slash('/'.join(harvest['data'][(p,t)]['csv'].split('/')[:-1]))
            offset    = AX['TICK_LOCS'][csv]
            bottom    = 0
            mywrite (log, "\n\tplotting plot_sSpace_bar2d of "+csv.split('/')[-1]+"("+ str(harvest['data'][(p,t)]['num_instances'])+" instances)"+" @ axis location "+str(offset))

            ##################################################################################
            #sSpace_avg = np.average(harvest['data'][(p,t)]['STATS']['fractions'])
            #sSpace_std = np.std(harvest['data'][(p,t)]['STATS']['fractions'])
            #color      = harvest['data'][(p,t)]['STATS']['color']
            #print('\n'+str(harvest['data'][(p,t)]['STATS']['fractions'])+'\n')
            #print('\n'+AX['ax'].get_yscale()+'\n')

            avg_total_search_space     = np.average([s[0] for s in harvest['data'][(p,t)]['STATS']['fractions']])
            avg_effective_search_space = np.average([s[1] for s in harvest['data'][(p,t)]['STATS']['fractions']])
            std_total_search_space     = np.std([s[0] for s in harvest['data'][(p,t)]['STATS']['fractions']])
            std_effective_search_space = np.std([s[1] for s in harvest['data'][(p,t)]['STATS']['fractions']])
            #total_space  = np.average([s[1] for s in harvest['data'][(p,t)]['STATS']['fractions']])
            ##################################################################################
            #try: # yerr=sSpace_std,
            #AX['ax'].bar(offset, search_space, bar_width,  color='red', align='center', alpha=0.75, edgecolor='white',linewidth=0.0)
            AX['ax'].bar(offset, avg_total_search_space, bar_width,     yerr=std_total_search_space,     color=tot_color,   align='center', alpha=alpha_tot, edgecolor='none',linewidth=0.0)
            AX['ax'].bar(offset, avg_effective_search_space, .6*bar_width, yerr=std_effective_search_space, color=eff_color, align='center', alpha=alpha_eff, edgecolor='none',linewidth=0.0)
            #except ValueError:
            #    pass
    return True
###################################################
def plot_iSize_bar2d(harvest, FIGURES, log):
    update_rcParams_pie()
    #mywrite (log, "\n\tmaster says: plotting instance size of file no "+str(harvest['file_no'])+" (from worker #"+str(harvest['rank'])+"): "+str(harvest['title'].replace('\n',' ').replace('$','')))

    Ps                 = sorted(list(set([float(pt[0]) for pt in harvest['data'].keys()])), reverse=True)
    Ts                 = sorted(list(set([float(pt[1]) for pt in harvest['data'].keys()])), reverse=True)
    COLORS             = getCOLORS("")

    for p in Ps:
        AX        = FIGURES[harvest['file_no']-1]['AX'][p]
        bar_width = AX['BAR_WIDTH']
        for t in Ts:           # SORTED, important
            csv       = harvest['data'][(p,t)]['csv'] #util.slash('/'.join(harvest['data'][(p,t)]['csv'].split('/')[:-1]))
            offset    = AX['TICK_LOCS'][csv]
            bottom    = 0
            mywrite (log, "\n\tplotting plot_iSize_bar2d of "+csv.split('/')[-1]+"("+ str(harvest['data'][(p,t)]['num_instances'])+" instances)"+" @ axis location "+str(offset))

            #########################################
            slices = harvest['data'][(p,t)]['STATS']
            #########################################

            normalizer = 0
            #------------------------------------------------------------------------------------------------
            sorted_keys   = [key for key in sorted([int(key) for key in slices['segments'].keys()])]
            #------------------------------------------------------------------------------------------------

            for key in sorted_keys:
                slices['segments'][key]['avg'] = np.average (slices['segments'][key]['fractions'])
                slices['segments'][key]['std'] = np.std     (slices['segments'][key]['fractions'])
                normalizer          += slices['segments'][key]['avg']
                #patch_labels.append(str(slices['segments'][key]['label']))

            sizes         = [(slices['segments'][key]['avg']/normalizer)*100 for key in sorted_keys]
            colors        = [slices['segments'][key]['color']          for key in sorted_keys]

            i=0
            for key in sorted_keys:
                if slices['segments'][key]['range'] not in [(100,0), (0,100)]:
                    next_stack =  sizes[i]
                    next_color =  colors[i]
                    if next_stack > 0:
                        # important: alpha must be 1 because legend patches are alpha 1 (don't know how to change that in palette_and_patches())
                        AX['ax'].bar(offset, next_stack, bar_width, color=next_color, align='center', alpha=1, edgecolor='white',linewidth=0.0,bottom=bottom)#, yerr=womenStd)
                        bottom += next_stack
                i+=1
    return True
###################################################
def plot_next_pie(harvest, FIGURES, log):

    update_rcParams_pie()
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
    font_prop = update_rcParams_scatter()

    file_no, coords, pos, prefix, file_path, title, data, configs, rank = harvest['file_no'], harvest['coords'], harvest['pos'], harvest['prefix'], harvest['file_path'], harvest['title'], harvest['data'], harvest['worker_configs'], harvest['rank']
    Bs, Ds, frequency, cbar_label, xlim, ylim = data['Bs'], data['Ds'], data['frequency'], data['cbar_label'], data['xlim'], data['ylim']
    #if pos==1:
    #    with open('harvest','wb') as f:
    #        import pickle
    #        pickle.dump(harvest,f)
    mywrite (log, "\n\tmaster says: plotting scatter of file no "+str(file_no)+" (from worker #"+str(rank)+"): "+str(title.replace('\n',' ').replace('$',''))+" "+str(xlim)+","+str(ylim))

    ax = FIGURES[file_no-1].add_axes(coords)

    title    = title.split('\n')
    title[0] = title[0]+", max(min) freq = "+str(util.f2(max(frequency)))+"("+str(util.f3(min(frequency)))+") %"
    title    = '\n'.join(title)

    #print('\nleft'+str(ax.spines['left'].get_linewidth() ))
    #print('\nbottom'+str(ax.spines['bottom'].get_linewidth() ))
    ax.spines['left'].set_linewidth  (ax.spines['bottom'].get_linewidth()/2.0)
    ax.spines['bottom'].set_linewidth(ax.spines['bottom'].get_linewidth()/2.0)
    ax.set_aspect('equal', adjustable='box')

    for i in range(len(Bs)):
        Bs[i]+=1 # zero values cause problems with log scale, increment everything by 1 and change ticklabels accordingly
    for i in range(len(Ds)):
        Ds[i]+=1 # zero values cause problems with log scale, increment everything by 1 and change ticklabels accordingly
    sizes=None
    if configs['mode']=='count':
        sizes        = rescale( [2**f for f in frequency], 1,100)
    else:
        sizes        =[f*20 for f in frequency]
    sc = None
    #-----------------------------------------------------------------
    cmap    = plt.cm.get_cmap('Set1')
    bounds  = [.001,.1, 1, 5, 10, 15, 20, 25, 30, 35]#, 50, 60]#, 70, 80, 90, 100] # Im assuming that freq's <=60 for all networks; check subplot titles to make sure this is the case (below I appended max/min freqs in the title)
    norm    = colors.BoundaryNorm(bounds, ncolors=cmap.N)
    if 'log_axis' in configs.keys():
        if str(configs['log_axis']).lower() == 'false':
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            sc      = ax.scatter (Ds, Bs, alpha=.7, marker='o', edgecolors='none',  c=frequency, s=[5]*len(frequency), cmap=cmap, norm=norm)

            ax.set_xlim([-1, xlim])
            ax.set_ylim([-1, ylim])
            xTks, yTks = ax.get_xticks(), ax.get_yticks()
            ax.set_xlim([0, xTks[-1] - xTks[-2] + xTks[-1]])
            ax.set_ylim([0, yTks[-1] - yTks[-2] + yTks[-1]])
            ax.tick_params(axis='x', which='both', left='off', right='off', bottom='off', top='on',  labelbottom='off', labeltop='on') # both major and minor ticks
            ax.tick_params(axis='y', which='both', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on') # both major and minor ticks
            ax.set_title(title)
            #ax.text(0.5, 0, title, horizontalalignment='center')#, transform = ax.transAxes)
    if sc == None: # alpha is smaller here because sizes is set, and some dots are so big they overlap with neighbours
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xscale('log', basex=2)
        ax.set_yscale('log', basey=2)

        sc      = ax.scatter (Ds, Bs, alpha=.7, marker='o', edgecolors='none',  c=frequency, s=sizes, cmap=cmap, norm=norm)

        ax.set_xlim([.5, xlim])#2**int(math.log(xlim, 2)+1)])
        ax.set_ylim([.5, ylim])#2**int(math.log(ylim, 2)+1)])
        ax.set_xticks([x for x in ax.get_xticks() if x>=.5 and x <= xlim])
        ax.set_yticks([y for y in ax.get_yticks() if y>=.5 and y <= xlim])

        ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
        ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks
        ax.set_title(title)
    #-----------------------------------------------------------------
    #mpl.markers.MarkerStyle(marker='+', fillstyle=None)
    print ("max D "+str(max(Ds))+" max B "+str(max(Bs)))
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(scatter_formatter))
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(scatter_formatter))

    cbar = FIGURES[file_no-1].colorbar(sc, shrink=0.4, pad=0.1, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label(cbar_label)
    cbar_ax = cbar.ax
    cbar_ax.tick_params(axis='both', which='minor', bottom='off', top='off', left='off', right='off', labelleft='off', labelright='off')
    cbar_ax.tick_params(axis='y',    which='major', bottom='off', top='off', left='off', right='on',  labelleft='off', labelright='on', pad=.4, width=.2, length=1) #http://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.tick_params.html
    cbar_ax.tick_params(axis='both', which='major', labelsize=4)
    cbar_ax_ylabel = cbar_ax.yaxis.label
    font =  mpl.font_manager.FontProperties(family=font_prop.get_name(), style='italic', size=rcParams['ytick.labelsize']*2)
    cbar_ax_ylabel.set_font_properties(font)

    # cbar.set_ticks([mn,md,mx])
    # cbar.set_ticklabels([mn,md,mx])
    # cbar_ax.get_yaxis().set_tick_params(which='major', direction='out',pad=.1,width=.2, right='on')
    # http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.tick_params

    #ax.set_xlim([-2,xlim])
    #ax.set_ylim([-2,ylim])


    ax.set_xlabel ("benefit")
    ax.set_ylabel ("damage")

    return True
###################################################
def ETXplotter_aggr(harvest, FIGURES, log):
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
                                                    'STATS' :       {
                                                                       'bin2binPLUSbou': {'AsF':0.0,'CsF':0}
                                                                       'bin2binPLUSdin': {'AsF':0.0,'CsF':0}
                                                                       'bin2din'       : {'AsF':0.0,'CsF':0}
                                                                       'Sbin2bin'      : {'AsF':0.0,'CsF':0}
                                                                    }
                    }

    Note:
        AsF means Average-so-Far
        CsF means Count-so-Far
    '''
    ########################
    plot_key = harvest['worker_configs']['plot_key'] #'Sbin2bin'#'bin2din'#'bin2binPLUSbou'#'bin2binPLUSdin'
    #######################
    Ps                 = sorted(list(set([float(pt[0]) for pt in harvest['data'].keys()])), reverse=True)
    Ts                 = sorted(list(set([float(pt[1]) for pt in harvest['data'].keys()])), reverse=True)

    for p in Ps:
        AX        = FIGURES[harvest['file_no']-1]['AX'][p]
        bar_width = AX['BAR_WIDTH']
        for t in Ts:           # SORTED, important
            csv       = harvest['data'][(p,t)]['csv']#util.slash('/'.join(harvest['data'][(p,t)]['csv'].split('/')[:-1]))
            offset    = AX['TICK_LOCS'][csv] #AX['TICK_LOCS'][t][csv]
            mywrite (log, "\n\tplotting ETXplotter_gain of "+csv.split('/')[-1]+"("+ str(harvest['data'][(p,t)]['num_instances'])+" instances)"+" @ axis location "+str(offset))
            AX['ax'].bar(offset, harvest['data'][(p,t)]['STATS'][plot_key]['AsF'], bar_width, color='forestgreen', align='center', alpha=.75, edgecolor='white',linewidth=0.0)#, yerr=womenStd)
    return True
###################################################
def ETXplotter(harvest, FIGURES, log): # plots the output of ETXcrucher1
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
                                                    'STATS' (ETXcruncher1,3) :       {
                                                                                        'deg': {
                                                                                                'bin':{'CsF':0.0,'AsF':0.0},
                                                                                                'din':{'CsF':0.0,'AsF':0.0},
                                                                                                'bou':{'CsF':0.0,'AsF':0.0},
                                                                                                'dou':{'CsF':0.0,'AsF':0.0},
                                                                                                }
                                                                                            ..
                                                                                            ..
                                                                                          }

                                                    'STATS' (ETXcruncher2) :          {
                                                                                        'deg': {
                                                                                                'bin2din':{'CsF':0.0,'AsF':0.0},
                                                                                                'bou2dou':{'CsF':0.0,'AsF':0.0}
                                                                                                }
                                                                                            ..
                                                                                            ..
                                                                                          }
                    }

    Note:
        AsF means Average-so-Far
        CsF means Count-so-Far
    '''
    #mywrite (log, "\n\tmaster says: plotting ETXplotter of file no "+str(harvest['file_no'])+" (from worker #"+str(harvest['rank'])+"): "+str(harvest['title'].replace('\n',' ').replace('$','')))
    if 'ETXcruncher_aggr' in harvest['worker_configs']['cruncher']:
        return ETXplotter_aggr(harvest, FIGURES, log)

    plot_key = harvest['worker_configs']['plot_key']
    '''
    plot_key = None
    try:
        assert len(harvest['worker_configs']['plot_key']) > 0
        plot_key = harvest['worker_configs']['plot_key']
    except:
        if harvest['worker_configs']['cruncher'] in ['ETXcruncher1','ETXcruncher3', 'ETXcruncher4', 'ETXcruncher5', 'ETXcruncher_gTB', 'ETXcruncher1b']:
            plot_key = 'bin' # default
        elif harvest['worker_configs']['cruncher'] in ['ETXcruncher2a' , 'ETXcruncher2b']:
            plot_key = 'bin2din' # default
        else:
            mywrite(log,'\nFATAL in ETXplotter() in plotters.py: I dont recognize this cruncher: '+str(harvest['worker_configs']['cruncher'])+'\nExiting ..')
            sys.exit(1)

    '''
    Ps                 = sorted(list(set([float(pt[0]) for pt in harvest['data'].keys()])), reverse=True)
    Ts                 = sorted(list(set([float(pt[1]) for pt in harvest['data'].keys()])), reverse=True)

    COLORS             = getCOLORS("")

    for p in Ps:
        AX        = FIGURES[harvest['file_no']-1]['AX'][p]
        bar_width = AX['BAR_WIDTH']
        for t in Ts:           # SORTED, important
            csv       = harvest['data'][(p,t)]['csv']#util.slash('/'.join(harvest['data'][(p,t)]['csv'].split('/')[:-1]))
            offset    = AX['TICK_LOCS'][csv] #AX['TICK_LOCS'][t][csv]
            mywrite (log, "\n\tplotting ETXplotter("+plot_key+") of "+csv.split('/')[-1]+"("+ str(harvest['data'][(p,t)]['num_instances'])+" instances)"+" @ axis location "+str(round(offset,4)))
            bottom    = 0
            for deg in sorted(harvest['data'][(p,t)]['STATS'].keys(), reverse=True):
                next_stack =  harvest['data'][(p,t)]['STATS'][deg][plot_key]['AsF']
                if next_stack > 0:
                    # important: alpha must be 1 because legend patches are alpha 1 (don't know how to change that in palette_and_patches())
                    AX['ax'].bar(offset, next_stack, bar_width, color=AX['palette'][deg], align='center', alpha=1, edgecolor='white',linewidth=0.0,bottom=bottom)#, yerr=womenStd)
                    bottom += next_stack
    return True
###################################################
def runtime_plotter(harvest, FIGURES, log):
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
                                                    'STATS'  :       { 'coresize': {'avg':[],'std':[]},
                                                                       'Ctime_s':  {'avg':[],'std':[]},
                                                                       'Pytime_s': {'avg':[],'std':[]},
                                                                     }
                    }

    Note:
        AsF means Average-so-Far
        CsF means Count-so-Far


    plot_key = None
    if harvest['worker_configs']['cruncher'] in ['ETXcruncher1','ETXcruncher3']:
        plot_key = 'bin' # or din, bou, dou
    elif harvest['worker_configs']['cruncher'] == 'ETXcruncher2':
        plot_key = 'bin2din'
    else:
        mywrite(log,'FATAL in ETXplotter() in plotters.py: I dont recognize this cruncher: '+str(harvest['worker_configs']['cruncher'])+'\nExiting ..')
        sys.exit(1)
    '''
    mywrite (log, "\n\tmaster says: plotting runtime_plotter() of file no "+str(harvest['file_no'])+" (from worker #"+str(harvest['rank'])+"): "+str(harvest['title'].replace('\n',' ').replace('$','')))

    #bar_key = 'Ctime_s'
    bar_key = 'Pytime_s'
    Ps                 = sorted(list(set([float(pt[0]) for pt in harvest['data'].keys()])), reverse=True)
    Ts                 = sorted(list(set([float(pt[1]) for pt in harvest['data'].keys()])), reverse=True)
    COLORS             = getCOLORS("")

    for p in Ps:
        AX        = FIGURES[harvest['file_no']-1]['AX'][p]
        AX['ax'].set_ylabel('execution time (milliseconds)')
        #AX['ax'].set_title(harvest['title']) # will show actual number of instances processed, as opposed to what was specified in params
        bar_width = AX['BAR_WIDTH']
        for t in Ts:           # SORTED, important
            csv       = util.slash('/'.join(harvest['data'][(p,t)]['csv'].split('/')[:-1]))
            offset    = AX['TICK_LOCS'][t][csv]
            next_bar =  (harvest['data'][(p,t)]['STATS'][bar_key]['avg'])*1000
            next_yerr =  (harvest['data'][(p,t)]['STATS'][bar_key]['std'])
            #if next_bar > 0:
            bar = AX['ax'].bar(offset, next_bar, bar_width, color='#02619b', align='center', alpha=.7, edgecolor='white',linewidth=0.0,yerr=next_yerr, ecolor='black', capsize=bar_width/2.0)# ecolor & capsize are for error bar (yerr)
            #AX['ax'].text(offset, bar[0].get_height()+1, harvest['data'][(p,t)]['bar_text'], ha="center", va="bottom", rotation=90, size=AX['annotation_text_size'])#, xy=(2, 1), arrowprops=dict(facecolor='black', shrink=0.05),

    return True
###################################################
def coresize_plotter(harvest, FIGURES, log):
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
                                                    'STATS'  :       { 'coresize': {'avg':[],'std':[]},
                                                                       'Ctime_s':  {'avg':[],'std':[]},
                                                                       'Pytime_s': {'avg':[],'std':[]},
                                                                     }
                    }

    Note:
        AsF means Average-so-Far
        CsF means Count-so-Far
    '''
    mywrite (log, "\n\tmaster says: plotting coresize_plotter() of file no "+str(harvest['file_no'])+" (from worker #"+str(harvest['rank'])+"): "+str(harvest['title'].replace('\n',' ').replace('$','')))
    bar_key = 'coresize'

    Ps                 = sorted(list(set([float(pt[0]) for pt in harvest['data'].keys()])), reverse=True)
    Ts                 = sorted(list(set([float(pt[1]) for pt in harvest['data'].keys()])), reverse=True)
    COLORS             = getCOLORS("")

    for p in Ps:
        AX        = FIGURES[harvest['file_no']-1]['AX'][p]
        AX['ax'].set_ylabel('coresize (% of instance size)')
        #AX['ax'].set_title(harvest['title']) # will show actual number of instances processed, as opposed to what was specified in params

        bar_width = AX['BAR_WIDTH']
        for t in Ts:           # SORTED, important
            csv       = util.slash('/'.join(harvest['data'][(p,t)]['csv'].split('/')[:-1]))
            offset    = AX['TICK_LOCS'][t][csv]
            next_bar  =  (harvest['data'][(p,t)]['STATS'][bar_key]['avg'])
            next_yerr =  (harvest['data'][(p,t)]['STATS'][bar_key]['std'])
            #if next_bar > 0:
            AX['ax'].bar(offset, next_bar, bar_width, color='#9b6a02', align='center', alpha=.7, edgecolor='white',linewidth=0.0, yerr=next_yerr, ecolor='black', capsize=bar_width/2.0)# ecolor & capsize are for error bar (yerr)
            AX['ax'].text(offset, next_bar+(.25*next_bar), harvest['data'][(p,t)]['bar_text'], ha="center", va="center", rotation=90, size=AX['annotation_text_size'])#, xy=(2, 1), arrowprops=dict(facecolor='black', shrink=0.05),
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
    elif 'ETXcruncher' in harvest['worker_configs']['cruncher']:
        return ETXplotter(harvest, FIGURES, log)
    elif harvest['worker_configs']['cruncher'] == 'runtime_cruncher':
        return runtime_plotter(harvest, FIGURES, log)
    elif harvest['worker_configs']['cruncher'] == 'coresize_cruncher':
        return coresize_plotter(harvest, FIGURES, log)
    elif harvest['worker_configs']['cruncher'] == 'iSize_cruncher':
        return plot_iSize_bar2d(harvest, FIGURES, log)
    elif harvest['worker_configs']['cruncher'] == 'sSpace':
        return plot_sSpace_bar2d(harvest, FIGURES, log)
    else:
        mywrite(log, "\n\tplotters says: There is plotter for this cruncher .. moving on ..")
        return True
###################################################
