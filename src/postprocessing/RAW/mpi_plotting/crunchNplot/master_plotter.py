import sys, os
sys.path.insert(0, os.getenv('lib'))
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import math, time
import matplotlib.ticker as ticker
from matplotlib import rcParams
import matplotlib.patches as mpatches
import matplotlib.font_manager as font_manager
from colour import Color
import init_plotting as init, util_plotting as util, utilv4 as superutil, pickle, plotters

##################################################################
mywrite = util.mywrite
realp    = superutil.realp
log10    = math.log10
##################################################################
def update_rcParams_ETX(inches):
    k = inches/2.5
    font_path = os.getenv('HOME')+'/.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = prop.get_name()
    rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
    rcParams['grid.alpha'] = 0.1
    rcParams['axes.grid']=False
    rcParams['savefig.pad_inches']=.1
    rcParams['grid.color']='white'

    rcParams['axes.titlesize']   = 3.9*k
    rcParams['axes.titleweight'] = 'normal'
    rcParams['axes.linewidth']   = .5
    rcParams['axes.labelsize']   = 4*k
    rcParams['axes.labelpad']    = 2

    rcParams['xtick.color']        =  'black'    #  ax.tick_params(axis='x', colors='red'). This will set both the tick and ticklabel to this color. To change labels' color, use: for t in ax.xaxis.get_ticklabels(): t.set_color('red')
    rcParams['xtick.direction']    =  'out'      # ax.get_yaxis().set_tick_params(which='both', direction='out')
    rcParams['xtick.labelsize']    =  3*k
    rcParams['xtick.major.pad']    =  1
    rcParams['xtick.major.size']   =  2  # how long the tick is
    rcParams['xtick.major.width']  =  .4
    rcParams['xtick.minor.visible']=  False


    rcParams['ytick.color']        =  'black'       # ax.tick_params(axis='x', colors='red')
    rcParams['ytick.direction']    =  'out'         # ax.get_xaxis().set_tick_params(which='both', direction='out')
    rcParams['ytick.labelsize']    =  4*k
    rcParams['ytick.major.pad']    =  1
    rcParams['ytick.major.size']   =  3
    rcParams['ytick.major.width']  =  .4
    rcParams['ytick.minor.pad']    =  1
    rcParams['ytick.minor.size']   =  1
    rcParams['ytick.minor.width']  =  .25
    rcParams['ytick.minor.visible']=  True

    rcParams['legend.fontsize']    =  4*k
    rcParams['legend.handleheight']=  0.5
    rcParams['legend.handlelength']=  1.0
    rcParams['legend.frameon']     =  False
    rcParams['legend.labelspacing']=  .2
    rcParams['legend.borderaxespad']=  .1
##################################################################
def get_plotting_configs(configs):
    alpha = 1
    if 'alpha' in configs.keys():
        try:
            alpha = float(configs['alpha'])
        except:
            pass
    if configs['cruncher'] == 'sSpace':
        effectiveSearchSpacealpha = alpha
        totalSearchSpacealpha     = alpha
        if 'effectiveSearchSpacealpha' in configs.keys():
            try:
                effectiveSearchSpacealpha = float(configs['effectiveSearchSpacealpha'])
            except:
                pass
        if 'totalSearchSpacealpha' in configs.keys():
            try:
                totalSearchSpacealpha = float(configs['totalSearchSpacealpha'])
            except:
                pass

        return {
                    'fig_suptitle':          "Search space relative to total space",
                    'fig_suptitle_fontsize': 18,
                    'plot':                  "red_plot",
                    'xlabel':                "Network",
                    'ylabel':                "Search space size",
                    'cbar_label':            None,
                    'cbar_labelsize':        None,
                    'marker':                None,
                    'totalSearchSpacealpha':                 totalSearchSpacealpha,
                    'effectiveSearchSpacealpha':                 effectiveSearchSpacealpha,
                    'cbar_labelsize':        None,
                    'wspace':                0.6,
                    'hspace':                0.4,
                    'projection':            None,
                    'dpi':                   300,

                }
    return {
                'fig_suptitle':          "The Good, The Bad, and The Ugly",
                'fig_suptitle_fontsize': 18,
                'plot':                  "green_grey_red",
                'xlabel':                "B:D distribution",
                'ylabel':                "fraction",
                'cbar_label':            None,
                'cbar_labelsize':        None,
                'marker':                None,
                'alpha':                 alpha,
                'cbar_labelsize':        None,
                'wspace':                0.6,
                'hspace':                0.4,
                'projection':            None,
                'dpi':                   300,

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
    if configs['cruncher'] == 'sSpace':
        return {'fractions':[],'color':'red', 'label':'Search space:Total space'}

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
        no_csv += len(superutil.cleanPaths(file))

    if (no_csv - len(DONEs)) <0:
        mywrite(configs['master_log'],"\nOOOOOOPS: something is terribly wrong, you may have changed the number of csv's since the last run, I'm ignoring this, fingers crossed.")
    else:
        no_csv = no_csv - len(DONEs)
    files_per_pair, pairs_per_worker = 1, 1 # defaults

    return math.ceil(math.ceil(no_csv/float(configs['files_per_pair']))/float(configs['pairs_per_worker']))
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
##################################################################
def update_specifics(configs):
    if configs['cruncher'] in ['cruncher1','cruncher2','cruncher3','cruncher4', 'iSize_cruncher','sSpace']:
        configs['slices']           = get_slices(configs)
##################################################################
def palette_and_patches(configs):
    if 'iSize' in configs['cruncher']:
        patches  = []
        for key in sorted(configs['slices']['segments'].keys()):
            if configs['slices']['segments'][key]['range'] not in  [(100,0), (0,100)]:
                color = configs['slices']['segments'][key]['color']
                label = configs['slices']['segments'][key]['label']
                patches.append(mpatches.Patch(color=color, label=label))
        return None, patches, "benefit:damage ratio"

    elif 'sSpace' in configs['cruncher']:
        patches = []
        effective_color, total_color, effective_label, total_label = 'black', 'grey', 'Effective search space', 'Total search space'

        if 'effectiveSearchSpaceColor' in configs.keys():
            effective_color  = configs['effectiveSearchSpaceColor']
        if 'totalSearchSpaceColor' in configs.keys():
            total_color  = configs['totalSearchSpaceColor']
        if 'effectiveSearchSpaceLabel' in configs.keys():
            effective_label  = configs['effectiveSearchSpaceLabel']
        if 'totalSearchSpaceLabel' in configs.keys():
            total_label  = configs['totalSearchSpaceLabel']

        patches.append(mpatches.Patch(color=effective_color, label=effective_label))
        patches.append(mpatches.Patch(color=total_color, label=total_label))


        configs['effectiveSearchSpaceColor'], configs['totalSearchSpaceColor'], configs['effectiveSearchSpaceLabel'], configs['totalSearchSpaceLabel'] = effective_color, total_color, effective_label, total_label

        return None, patches, ""

    else:#if 'ETX' in configs['cruncher']:
        all_degrees       = [d for d in range(1,3000,1)]#[deg for deg in range(1,configs['max_degree']+1,1)]
        maxd              = 17# max(all_degrees)
        mind              = 1#min(all_degrees)
        start             = Color('#ff00c8')#Color("#ff33e0")
        middle1           = Color('#e999ff')#Color('#9333ff')
        middle2           = Color('#0f4dff')#Color('#cfc9f8') # #3371ff
        end               = Color('#afcecc')#Color('#33f3ff')

        jump1             = 1 # must be >= 1, larger values = less distinct colors; increase it if start and middle are far-apart colors
        jump2             = 1
        cutoff_degree     = 4#min(4,math.ceil(maxd/2.0)) # must be >= 1

        palette_size1     = math.ceil(math.log(cutoff_degree,2)) + 1
        palette_size2     = math.ceil(math.log(maxd,2)) - math.floor(math.log(cutoff_degree,2))
        #print('\nmaxd '+str(maxd))
        #print('cutoff_degree '+str(cutoff_degree))
        #print('palette_size1 '+str(palette_size1))
        #print('palette_size2 '+str(palette_size2))
        under_cutoff      = list(start.range_to   (middle1, max(1,palette_size1*jump1)))
        above_cutoff      = list(middle2.range_to (end,     max(1,palette_size2*jump2)))


        palette = {}
        for deg in all_degrees:#range (1, maxd+1,1):
            if deg <= cutoff_degree:
                index = math.ceil(math.log(deg,2)) + (jump1-1)
                palette[deg] = under_cutoff[index].rgb
            elif deg < maxd:
                index = math.ceil(math.log(maxd,2)) - math.ceil(math.log(deg,2)) + (jump2-1)
                palette[deg] = above_cutoff[index].rgb
            else:
                index = (jump2-1)
                palette[deg] = above_cutoff[index].rgb


        distinct_colors, patches, i = [], [], 1
        while True:
            distinct_colors.append(palette[i])
            current_color = palette[i]
            left = i
            i+=1
            while palette[i] == current_color:
                i+=1
                if i>maxd:
                    break
            right = i
            label = None
            if i<=maxd:
                label = str(left)
                if right-left > 1:
                    label += '-'+str(right-1)
                patches.append(mpatches.Patch(color=current_color, label=label))
            else:
                label = '>='+str(maxd)
                patches.append(mpatches.Patch(color=current_color, label=label))
                break

        #for deg in sorted(all_degrees):
        #    print (str(deg).ljust(4,' ')+str(palette[deg]))
    return palette, patches, "degree:"
##################################################################
def set_CANVAS2_XLABEL(csv_dir_path):
    # /mnt/backups/malsha17/execution_stats/Vinayagam/Vinayagam/v4_alpha0.2/v4nu_minknap_execstats_4X_both_reverse/03_execution_stats_simulation/data_points/
    if os.path.isfile(csv_dir_path):
        csv_dir_path = '/'.join(csv_dir_path.split('/')[:-1])
    csv_dir_path = util.slash(csv_dir_path)
    net     = csv_dir_path.split('/')[-6].split('_')[0]
    if net == 'Vinayagam':
        net = 'Fly-PPI_orig'
    setting = csv_dir_path.split('/')[-4].split('_')
    if 'scramble' in setting:
        #net += ' S'
        net = 'Scrambled'
    setting = [s.replace('v4','').replace('minknap', 'MI').replace('DPsolver','DP') for s in setting if s not in ['1X','4X','execstats']]
    setting[0] = setting[0].upper() # NU, NB, EU, EB
    setting[1] = '-'+setting[1].upper()
    setting[2] = setting[2][0:2].upper()+'-' # BO, SO, TA (both, source target)
    setting[3] = setting[3][0:3].lower()
    setting = ''.join(setting)
    return setting+'  '+net.rjust(10, ' ')
##################################################################
def set_CANVAS2_TITLE(configs, stamp, csv_dirs):
    title = stamp+', '+configs['cruncher']+', $t\in$'+str(sorted(configs['Ts']))
    num_instances = ', ? instances'

    if 'max_instances' in configs.keys():
        try:
            num_instances = ', '+str(util.pf(math.ceil(int(configs['max_instances']))))+' instances'
        except:
            pass
    title += num_instances
    for csv in csv_dirs:
        csv      = util.slash(csv)
        net      = csv.split('/')[-6]
        #net      = net[:min(6,len(net))] # crop it to 4 characters
        setting  = csv.split('/')[-4].split('_')
        setting  = [s.replace('v4','').replace('minknap', 'MI').replace('DPsolver','DP') for s in setting if s not in ['1X','4X','execstats']]
        setting[0] = setting[0].upper() # NU, NB, EU, EB
        setting[1] = setting[1][0:2].upper()+'-' # BO, SO, TA (both, source target)
        setting[2] = setting[2][0:3].lower()
        setting = ''.join(setting)

        title  += ', '+net+'('+setting+')'
    return title
##################################################################
def groupsByOrganismAndNetworks(csv_dirs,configs):
    Family, networks, family_keys = {}, [], [-8,-7]
    #/$bd/Bacteria/RegulonDB/RN_Bacteria-RegulonDB/v4_alpha0.2/v4nu_DPsolver_1X_both_reverse/02_raw_instances_simulation/data_points
    #        -8        -7           -6                -5  .......
    if 'zip_families_by' in configs.keys():
        try:
            FKs = [int(fk) for fk in configs['zip_families_by'].split(',')]
            if len(FKs)>0:
                family_keys = FKs
        except:
            pass
    order=1
    for csv in csv_dirs:
        key = ''
        for fk in family_keys:
            key+=util.slash(csv).split('/')[fk]+' '
        key = key.strip()
        if key not in Family.keys():
            Family[key] = {'order':order,'CSVs':[]}
            order+=1
        Family[key]['CSVs'].append(csv)
    subgrouped = {}
    id=1 # use IDs to help keep csvs in the order they appear in INPUT
    ordered_fams = [elem[0] for elem in sorted(Family.items(), key=lambda x: x[1]['order'])] # so that networks appear in the order they were in INPUT.txt
    for fam in ordered_fams: # don't use 'set', it distorts order
        subgrouped[id] = {}
        subgrouped[id]['family']   = fam
        subgrouped[id]['networks'] = []
        id+=1
    for csv in csv_dirs:
        fam    = None
        for key in ordered_fams:
            if csv in Family[key]['CSVs']:
                fam = key
        fam_id = [id for id in subgrouped.keys() if subgrouped[id]['family'] == fam ]
        assert len(fam_id)==1
        subgrouped[fam_id[0]]['networks'].append(csv)
    '''
    subgrouped = {
                   'id':   { 'family':'Human', # or 'Human ENCODE'
                             'networks':[ ENCODE_Proximal, PPI, ... ]
                            }
                 }
    '''
    #print('\n'*10)
    #print(subgrouped)
    #print('\n'*10)
    return subgrouped
##################################################################
def getCSV(csv_dir, p, t, spoint='_RAW_INSTANCES_'):
        right_csv=[]
        try:
            assert os.path.isdir(csv_dir)
        except:
            print("FATAL : invalide directory "+csv_dir+'\nExiting ..')
            sys.exit(0)
        for root, dirs, files in os.walk(csv_dir): #'file_path' is a actually a dir path
            for f in files:
                if f.split('.')[-1] == 'csv':
                    # extract p,t; Vinayagam_RAW_INSTANCES_p100.0_t001.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv
                    PT =[float(x.replace('p','').replace('t','')) for x in f.split('/')[-1].split(spoint)[-1].split('_')[0:2]]
                    current_p, current_t = PT[0], PT[1]
                    if current_p==p and current_t==t:
                        right_csv.append(os.path.join(root,f))
        assert len(right_csv) ==1
        return right_csv[0]
##################################################################
def set_CANVAS2_TICKS(BARS, locs, labels, bar_width, pad, padGroupsTill, offset):
    # groups by Ts, subgroups by Networks
    # BARS = { t=5: { 'Human' : [Human_p_t..csv, NL_Human_p_t.. csv, RN_Human ....., ... ],
    #                 'Plant' : ....
    #               }
    #        }

    TICK_LOCS={}
    group_size = 0
    for group in sorted(BARS.keys()): #Ts
        for subgroup_id in sorted(BARS[group].keys()): # organisms : Human, Plant ...
            i = 0
            for csv in BARS[group][subgroup_id]: # Human.csv, NL_Human.csv ....
                TICK_LOCS[csv] = offset
                locs.append(offset)
                labels.append(set_CANVAS2_XLABEL(csv))
                offset                 += bar_width+pad
                i+=1
            group_size = max(group_size,i)
            offset      += bar_width+pad

        if padGroupsTill > len(BARS[group].keys()):
            for i in range(padGroupsTill - len(BARS[group].keys())):
                for j in range(group_size):
                    locs.append(offset)
                    labels.append('dummyyy'+str(i+1)+str(j))
                    offset             += bar_width+pad
                offset                 += bar_width+pad

        offset      += bar_width + pad
        group_size   = 0


    return TICK_LOCS, locs, labels
##################################################################
def set_CANVAS2_BARS(configs, csv_dirs, p):
    '''
    groups             = Ts
    subgroups        = organisms (Bacteria, Human ..)
    subsubgroup        = Networks  (PPI, RegulonDB .. )
    subsubsubgroup    = variants  (real, NH, NL, RN)
    '''
    BARS = {}
    groups = configs['Ts']
    bars_per_group = 0
    for t in groups:
        BARS[t] = {}
        subgroups = groupsByOrganismAndNetworks(csv_dirs,configs) # families
        for org_id in sorted(subgroups.keys()):
            BARS[t][org_id] = []
            children = subgroups[org_id]['networks']
            # pick the right p,t csv file from each dir
            bars_per_group = max(bars_per_group, len(children))
            for child_dir in children:
                BARS[t][org_id].append(  getCSV(child_dir, p, t) )

    group_axis_length  = 1.0
    bar_width          = group_axis_length/bars_per_group
    pad, padGroupsTill = 0,0
    if 'pad' in configs.keys():
        try:
            pad = (int(configs['pad'])/100)*bar_width
            assert pad >=0
        except:
            pad = 0
    if 'padGroupsTill' in configs.keys():
        try:
            padGroupsTill = int(configs['padGroupsTill'])
            assert padGroupsTill >=0
        except:
            padGroupsTill = 0 # as a minimum, group should have the same pad as that between bars within a group
    return BARS, bar_width, pad, padGroupsTill
##################################################################
def customize_CANVAS2(AX, configs, csv_dirs, stamp, p):

    AX['ax'].tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    AX['ax'].tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='on',  labelleft='on', labelright='on') # both major and minor ticks
    AX['ax'].spines['top'].set_visible(False)
    AX['ax'].spines['right'].set_visible(True)
    if 'logify_y' in configs.keys():
        base = 10
        if str(configs['logify_y']).lower() == 'true':
            if 'base_y' in configs.keys():
                try:
                    base=int(configs['base_y'])
                except:
                    pass
            AX['ax'].set_yscale('log', basey=base)
    #if configs['cruncher'] in ['ETXcruncher2']:
    #    AX['ax'].set_yscale('log', basey=10)#, linthreshy=.1)#, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    if 'ETX' in configs['cruncher'] or 'iSize' in configs['cruncher']:# or configs['cruncher'] == 'sSpace':
        AX['ax'].yaxis.set_major_formatter(ticker.FuncFormatter(plotters.LogYformatter))
    if configs['cruncher'] not in ['runtime_cruncher','coresize_cruncher'] and configs['cruncher'] !='sSpace':
        AX['ax'].set_ylim([.05,100]) # it matters where this line is, (it has to be before ticking is done i think)

    # BARS = { t=5: { 1: {'mother': 'Human', 'children':[Human_p_t..csv, NL_Human_p_t.. csv, RN_Human ....., ... ],
    #                 2: {'mother': 'Plant', 'children':[......] : ....
    #               }
    #        }

    ##################################################################################
    BARS, bar_width, pad, padGroupsTill = set_CANVAS2_BARS(configs, csv_dirs, p)
    #import pprint
    #pp=pprint.PrettyPrinter(indent=4)
    #pp.pprint(BARS)
    ##################################################################################
    # add a dummy bar at the beginning (serves as padding away from left y-axis
    locs, labels, offset   = [],[],0#[bar_width+pad], [''], bar_width+pad
    #AX['ax'].bar(offset, 50, bar_width, color='black', align='center', edgecolor='white',linewidth=0.0) # a dummy, so that the first bar starts off one-bar-width away from the y-axis
    ################################## the heart of it ################################
    AX['TICK_LOCS'], locs, labels   = set_CANVAS2_TICKS(BARS, locs, labels, bar_width, pad, padGroupsTill, offset)
    ###################################################################################
    # add a dummy bar at the end (serves as padding away from right y-axis
    #locs.append(offset)
    #labels.append('')
    #print (str(labels)+"\n\n")
    #AX['ax'].bar(offset, .000001, bar_width, color='white', align='center', edgecolor='white',linewidth=0.0) # a dummy, so that the first bar starts off one-bar-width away from the y-axis
    #AX['ax'].xaxis.get_major_ticks()[-1].draw = lambda *args:None
    for lo,la in zip(locs,labels):
        if  'dummyyy' in la:
            AX['ax'].bar(lo,1,color='green',align='center',ecolor='white',linewidth=0.0)
    AX['ax'].set_xticks(locs)
    AX['ax'].set_xticklabels(labels)#, rotation='vertical')
    AX['BAR_WIDTH'] = bar_width-pad
    AX['ax'].set_xticklabels(labels,rotation=90)

    fig_title = "$P="+str(p)+"$\n"+set_CANVAS2_TITLE(configs, stamp, csv_dirs)
    fig_title_broken, start,end = '', 0, 200
    while end < len(fig_title):
        fig_title_broken = fig_title_broken+fig_title[start:end]+'\n'
        start=end+1
        end+=100

    AX['ax'].set_title(fig_title_broken+'\n')

    # don't draw the ticks of the dummy bars
    #AX['ax'].xaxis.get_major_ticks()[-1].tick1On = False  # for some reason this didn't work, it messes up the other ticks don't display a tick for this dummy bar
    ##AX['ax'].xaxis.get_major_ticks()[0].draw = lambda *args:None # http://stackoverflow.com/questions/19499156/removing-specific-ticks-from-matplotlib-plot
    ##AX['ax'].xaxis.get_major_ticks()[-1].draw = lambda *args:None
    AX['palette'], patches, title = palette_and_patches(configs)
    y = .35
    if 'iSize' in configs['cruncher']:
        y=0.1
    legend = AX['ax'].legend(handles=patches, loc=(1.1,y), title=title) # http://matplotlib.org/api/legend_api.html#matplotlib.legend.Legend
    legend.get_title().set_fontsize(rcParams['ytick.labelsize'] ) # this is a must, can't do this thru rcParams

    #for loc,text in zip (AX['ax'].get_xticks(), [t.get_text() for t in AX['ax'].get_xticklabels()]):
    #    print (str(loc).ljust(5,' ')+text)
    return True
###################################################
def canvas2(configs, file, stamp, file_no, augPAIRS, FIGURES):

    log         = configs['master_log']
    clean_paths = superutil.cleanPaths(file)
    csv_dirs    = [util.slash(realp(line)) for line in clean_paths ]

    PAIRS          = util.getDirsPairs (csv_dirs, min(len(csv_dirs), configs['files_per_pair']))
    total_cols     = 1


    total_rows     = len(configs['Ps'])
    '''
    if configs['needed_workers'] > configs['available_workers']:
        total_plots = configs['available_workers'] * (min(len(csv_dirs), configs['files_per_pair'])) * configs['pairs_per_worker']
        total_rows  = math.ceil(float(total_plots)/total_cols)
        while total_rows*total_cols > total_plots:
            total_cols -= 1
    '''
    dim           = max(total_rows,total_cols)
    inches        = dim*5# dim*math.log(max(10, configs['dpi']), 10) # in inch
    fig_dims      = (inches, inches) # enforce square canvas always (makes life easier)
    figure_size   = (fig_dims) #(width, height)

    update_rcParams_ETX(inches)

    COORDs = getCOORDs (fig_dims, dim, dim,  w2h_ratio = 0.65,ppercent= 0.29)
    FIGURES.append({'fig':plt.figure(figsize=figure_size), 'AX':{}})

    XY, xy_loc = [], 0 # we always create a rectangle canvas (so propostions of text to axes don't get messed up depending on the number of axes) so we need to jump over unnecessary coordinates. fig.savefig(tightbox) will take care of removing extra white space
    for r in range(total_rows):
        for c in range(total_cols):
            XY.append(COORDs[xy_loc])
            xy_loc +=1
        #jump over excess cols
        for i in range(dim-total_cols):
            xy_loc +=1

    assert len(XY) == len(configs['Ps'])

    for p, coord in zip(configs['Ps'], XY):
        FIGURES[-1]['AX'][p]       = {}
        FIGURES[-1]['AX'][p]['ax'] = FIGURES[-1]['fig'].add_axes(coord)
        FIGURES[-1]['AX'][p]['annotation_text_size'] = rcParams['ytick.labelsize']/2.0
        customize_CANVAS2(FIGURES[-1]['AX'][p], configs, csv_dirs, stamp, p)

    pos = 1
    for pair in PAIRS: # a pair for each worker

        if len(pair)>0:
            tmp=[]
            if configs['assigned_workers']  >= configs['available_workers']:# or pos > (total_cols*total_rows):
                break
            #worker_0001_figure_0001_rows_0006_cols_0004_pos_0001.done
            for tuple in pair:
                if ("_figure_"+str(file_no).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')+'.done') not in configs['DONEs']:
                    processing_bit = 1
                    mywrite(log, "\n\tmaster assigns: "+tuple[1])
                else:
                    processing_bit = 0
                    mywrite(log, "\n\tmaster skips  : "+tuple[1])
                tmp.append({'file_no':file_no, 'pos':pos, 'prefix':tuple[0], 'file_path':tuple[1],'title': tuple[2], 'processing_bit':processing_bit})
                configs['watchlist'] += 1
                pos                  += 1
            if sum([dict['processing_bit'] for dict in tmp])  > 0:
                augPAIRS.append([t for t in tmp])
                configs['assigned_workers'] = float(len(augPAIRS))/configs['pairs_per_worker']
    return augPAIRS
##################################################################
def canvas1(configs, file, file_no, augPAIRS, FIGURES):
    log = configs['master_log']
    clean_paths = superutil.cleanPaths(file)
    csv_files   = [realp(line) for line in clean_paths ]

    PAIRS = None

    PAIRS          = util.getPairs (csv_files, min(len(csv_files), configs['files_per_pair']))

    total_cols     = configs['columns']
    total_rows     = math.ceil(len(csv_files)/configs['columns'])

    if configs['needed_workers'] > configs['available_workers']:
        total_plots = configs['available_workers'] * (min(len(csv_files), configs['files_per_pair'])) * configs['pairs_per_worker']
        total_rows  = math.ceil(float(total_plots)/configs['columns'])
        while total_rows*total_cols > total_plots:
            total_cols -= 1

    dim       = max(total_rows,total_cols)
    inches    = dim*math.log(max(10, configs['dpi']), 10) # in inch
    fig_dims  = (inches, inches) # enforce square canvas always (makes life easier)

    figure_size             = (fig_dims) #(width, height)

    FIGURES.append(plt.figure(figsize=figure_size))

    #FIGURES[-1].suptitle('\n'+configs['plotting_configs']['fig_suptitle'], fontsize=configs['plotting_configs']['fig_suptitle_fontsize'], y=y       )
    #FIGURES[-1].subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['plotting_configs']['wspace'], hspace=configs['plotting_configs']['hspace'] )
    w2h_r = 0.5
    if configs['cruncher'] == 'cruncher4':
        w2h_r = .65
    COORDs = getCOORDs (fig_dims, dim, dim,  w2h_ratio = w2h_r)

    XY, xy_loc = [], 0 # we always create a rectangle canvas (so propostions of text to axes don't get messed up depending on the number of axes) so we need to jump over unnecessary coordinates. fig.savefig(tightbox) will take care of removing extra white space
    for r in range(total_rows):
        for c in range(total_cols):
            XY.append(COORDs[xy_loc])
            xy_loc +=1
        #jump over excess cols
        for i in range(dim-total_cols):
            xy_loc +=1
    pos = 1
    for pair in PAIRS: # a pair for each worker

        if len(pair)>0:
            tmp=[]
            if configs['assigned_workers']  >= configs['available_workers'] or pos > (total_cols*total_rows):
                break
            #worker_0001_figure_0001_rows_0006_cols_0004_pos_0001.done
            for tuple in pair:
                if ("_figure_"+str(file_no).rjust(4,'0')+ "_pos_"+str(pos).rjust(4,'0')+'.done') not in configs['DONEs']:
                    processing_bit = 1
                    mywrite(log, "\n\tmaster assigns: "+tuple[1].split('/')[-1])
                else:
                    processing_bit = 0
                    mywrite(log, "\n\tmaster skips  : "+tuple[1].split('/')[-1])
                tmp.append({'file_no':file_no, 'coords':XY[pos-1], 'pos':pos, 'prefix':tuple[0], 'file_path':tuple[1],'title': tuple[2], 'processing_bit':processing_bit})
                configs['watchlist'] += 1
                pos                  += 1

            if sum([dict['processing_bit'] for dict in tmp])  > 0:
                augPAIRS.append([t for t in tmp])
                configs['assigned_workers'] = float(len(augPAIRS))/configs['pairs_per_worker']

    return augPAIRS
##################################################################
def workload_splitter(configs):
    log = configs['master_log']
    configs['group_size']={}
    configs['assigned_workers'], file_no, augPAIRS, FIGURES = 0, 0, [], []
    PAIRS,XY=None,None
    for file,stamp in zip(configs['input_files'],configs['stamps']):
        file_no    += 1
        total_cols, total_rows =0,0
        if 'ETXcruncher' in configs['cruncher'] or  configs['cruncher'] in ['coresize_cruncher','runtime_cruncher','iSize_cruncher','sSpace']:
           augPAIRS = canvas2(configs, file, stamp, file_no, augPAIRS, FIGURES)
        else:
            augPAIRS = canvas1(configs, file, file_no, augPAIRS, FIGURES)

    return [configs, augPAIRS, FIGURES]
##################################################################
def workload_dumper(arg):
    configs, augPAIRS, FIGURES = arg[0],arg[1], arg[2]
    log=configs['master_log']
    WORK_LOAD = []
    sys.stdout.flush()
    while len(augPAIRS)>0:
        WORK_LOAD.append([pair for pair in augPAIRS[0:configs['pairs_per_worker']]])
        augPAIRS = augPAIRS[configs['pairs_per_worker']:]
    if configs['available_workers'] < configs['needed_workers']:
        mywrite(log, "\n\n\tmaster says: WARNING: available_workers < needed_workers,"+str((configs['needed_workers'] - configs['available_workers'])*configs['pairs_per_worker']*configs['files_per_pair'])+" subplots will not be plotted ")
    next_ax=0

    for rank in range(1, len(WORK_LOAD)+1, 1): # num_workers == num pairs
        with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'wb') as f:
            configs['WORK_LOAD']  = WORK_LOAD[next_ax]
            pickle.dump(configs, f)
            f.close()
            next_ax+=1
    #send empty augPAIRS to these extra workers
    if configs['available_workers'] > len(WORK_LOAD) :
        for rank in range(len(WORK_LOAD)+1, configs['available_workers']+1,1):
            with open (os.path.join(configs['configs_dir'], "configs_"+str(rank).rjust(4,'0')),'wb') as f:
                configs['WORK_LOAD']= []
                pickle.dump(configs, f)
                f.close()
    #print ("assigned_workers "+str(assigned_workers)+", next_ax "+str(next_ax))
    assert math.ceil(configs['assigned_workers']) == next_ax
    mywrite(log, "\n\n\tmaster says: WORKERS:  avail "+str(configs['available_workers'])+", assigned: "+str(next_ax)+", needed: "+str(configs['needed_workers'])+", len(WORK_LOAD) "+str(len(WORK_LOAD))+", len(DONEs) "+str(len(configs['DONEs']))+"\n")
    return [configs, FIGURES, WORK_LOAD]
##################################################################
def harvest(file, FIGURES, log):
    harvest=None
    with open(file,'rb') as f:
        harvest = pickle.load(f)
    return plotters.plot(harvest, FIGURES, log)
##################################################################
def savename(configs,i):
    name  = util.slash(configs['plots_dir'])
    name += str(i).rjust(3,'0')
    cruncher, mode, interval, plot_key = "", "", "", ""
    try:
        cruncher = configs['cruncher']
        cruncher = '_'+cruncher
    except:
        pass
    try:
        if configs['cruncher'] == 'scatter':
            mode = configs['mode']
            mode = '_'+mode
    except:
        pass
    try:
        interval = '_'+str(configs['slices']['interval'])
        interval +="-interval"
    except:
        pass
    try:
        plot_key =  '_'+str(configs['plot_key'])
    except:
        pass
    name += cruncher+plot_key+mode+interval+'_'+configs['timestamp']+"."+configs['file_extension']
    return name
##################################################################
def watch (arg):
    configs, FIGURES, WORK_LOAD = arg[0], arg[1], arg[2]
    log = configs['master_log']
    t0 = time.time()

    if len (WORK_LOAD) == 0:
        mywrite(log, "\n\tmaster says: len(WORK_LOAD)==0, I will re-harvest what's done previously anyway ")
    mywrite (log, "\n\tmaster says: watching "+str(configs['watchlist']) +"  subplots")
    harvested_files, counter  = [], 0
    while counter < configs['watchlist']:
        for root, dirs, fs in os.walk(configs['DUMP_DIR']):
            confirmation = False
            for f in fs: # skip directories recently modified (1 minutes), workers may still be writing to them
                if 'done' in f.split('.') and f not in harvested_files:
                    confirmation = harvest (os.path.join(root, f), FIGURES, log)
                    if confirmation == True:
                        harvested_files.append(f)
                        counter += 1
                        mywrite(log, "\n\tmaster says: successfully plotted ("+str(counter).rjust(3,'0')+"): "+f.split('/')[-1])
                    else:
                        mywrite(log, "\n\tmaster says: failed to harvested ("+str(counter).rjust(3,'0')+"): "+f.split('/')[-1])
        time.sleep (5)
    i=1
    for fig in FIGURES:
        if not isinstance(fig, mpl.figure.Figure): # FIGURES of canvas2 are dictionaries, FIGURE[i]= {'fig': plt.figure(..), 'AXES':[....]}
            fig = fig['fig']
        #fig.tight_layout()
        name = savename(configs,i)
        dpi=None
        if 'dpi' in configs.keys():
            try:
                dpi = configs['dpi']
                assert dpi>0
            except:
                dpi = configs['plotting_configs']['dpi']
        mywrite (log, "\n\tmaster says: saving figure no. "+str(i)+" (dpi="+str(dpi)+"): "+name)

        fig.savefig(name , dpi=dpi, bbox_inches="tight")
        i+=1

    t1 = time.time()
    mywrite(log, "\n\tmaster says: harvested "+str(counter)+" plots in "+str(int(t1-t0))+" seconds\n")
##################################################################

def supervise (configs_file, num_workers):

    configs                        = init.load_simulation_configs (configs_file, 0)
    update_specifics(configs)
    configs['master_log']          = configs['logs_dir']+"master_"+configs['timestamp']+".log"
    configs['num_workers']         = num_workers
    configs['plotting_configs']    = get_plotting_configs(configs)
    configs['watchlist']           = 0
    configs['DONEs']               = getDONEs(configs)
    configs['needed_workers']      = calculate_needed(configs['DONEs'], configs)
    configs['available_workers']   = num_workers

    mywrite(configs['master_log'], "\n====================================\nmaster says: supervising\n====================================\n")

    watch(       workload_dumper(        workload_splitter(configs)   )    )

##################################################################
