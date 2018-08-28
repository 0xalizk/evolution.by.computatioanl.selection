#!/usr/bin/env python
# a stacked bar plot with errorbars
import numpy as np, sys, os, math, matplotlib as mpl, matplotlib.font_manager as font_manager, matplotlib.pyplot as plt, SLICES 
from matplotlib import rcParams
import matplotlib.patches as mpatches
from colour import Color
import matplotlib.ticker as ticker

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
################################################### 
def getCOORDs (fig_inch_dims, cols, rows, w2h_ratio=0.5):
    COORDs    = []
    figw_inch = fig_inch_dims[0]
    figh_inch = fig_inch_dims[1]
    ppercent  = .25 # percentage of area to be used for padding 
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
################################################### 
def palette_and_patches(all_degrees):
    maxd              = max(all_degrees)
     
    start             = Color('#ff00c8')#Color("#ff33e0") 
    middle1           = Color('#e999ff')#Color('#9333ff') 
    middle2           = Color('#afcecc')#Color('#cfc9f8') # #3371ff
    end               = Color('#0f4dff')#Color('#33f3ff')
    
    jump1             = 1 # must be >= 1, larger values = less distinct colors; increase it if start and middle are far-apart colors
    jump2             = 1
    cutoff_degree     = 4 # must be >= 1
    
    palette_size1     = math.ceil(math.log(cutoff_degree,2)) + 1
    palette_size2     = math.ceil(math.log(maxd,2)) - math.floor(math.log(cutoff_degree,2)) 
       
    under_cutoff      = list(start.range_to   (middle1, palette_size1*jump1))
    above_cutoff      = list(middle2.range_to (end, palette_size2*jump2)) 

    print ('under_cutoff: '+str(len(under_cutoff)))
    print ('above_cutoff: '+str(len(above_cutoff)))

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
def customize_bar(ax, xlabels, xlabels_loc):
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks             
    ax.set_xticks(xlabels_loc)
    ax.set_xlabel('benefit:bamage ratio group')
    ax.set_ylabel('% degree makeup (log)')
    ax.set_title('Degree makeup of genes in each \nbenefit:damage ratio group\n')
    ax.set_xticklabels(xlabels,rotation='vertical')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yscale('log', basey=10)#, subsx=[0,2,4,8,16], subsy=[0,2,4,8,16])
    ax.set_ylim([0,100]) # it matters where this line is, (it has to be before ticking is done i think)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    return ax
###################################################    
def plot_next_bar2d(slices, ax, title, configs):
    DegFreqBySlice, all_degrees, group_labels = extract_stats (SLICES.slices)
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
    
    
    ax   = customize_bar(ax, group_labels, tickloc) # IMPORTANT: should be called after ax.bar is done
    legend = ax.legend(handles=patches, loc=(.99,0.35), title='degree:') # http://matplotlib.org/api/legend_api.html#matplotlib.legend.Legend 
    legend.get_title().set_fontsize(5) # this is a must, can't do this thru rcParams
    #ax.plot([0., max(tickloc)+(width/2.)], [25, 25], "--", color='black', linewidth=1) # linestyle='-/--/-./:'
###################################################    
configs={'dpi':300}
configs['plotting_configs'] = get_plotting_configs(configs)
C = [1]
R = [1]

for rows,cols in zip(R,C):
	no_plots = rows*cols
	dim = max(rows,cols)
	inches = dim*math.log(max(10, configs['dpi']), 10) # in inch
	fig_dims  = (inches, inches) # enforce square canvas always (makes life easier)

	fig = plt.figure(figsize=fig_dims) #width, height

	#fig.suptitle('\n'+configs['plotting_configs']['fig_suptitle'], fontsize=configs['plotting_configs']['fig_suptitle_fontsize'], y=1   )  
	#fig.subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['plotting_configs']['wspace'], hspace=configs['plotting_configs']['hspace'] )

	update_rcParams(no_plots)

	COORDs = getCOORDs (fig_dims, max(rows,cols), max(rows,cols),  w2h_ratio = 0.65) 

	xy_loc = 0 # first element in COORDs is bottom-left axes
	for r in range(rows):
		for c in range(cols):
			ax = fig.add_axes(COORDs[xy_loc])
			plot_next_bar2d(SLICES.slices, ax, "title", {})
			#plt.axes(COORDs[xy_loc])
			#plt.text(0.1, 0.1, 'axes '+str(xy_loc+1), ha='left', va='center', size=16, alpha=.5)
			xy_loc +=1
		#jump excess cols
		for i in range(dim-cols):
			xy_loc +=1

	plt.savefig('bar_'+str(rows)+'-'+str(cols)+'.png', bbox_inches='tight', pad_inches=.1, dpi=300) # bbox_inches='tight' removes white spaces




























#plt.show()
#ax.text(1, .78, 'Degree') # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.text
#ax.set_yticks(np.arange(0, 81, 10))
#ax.legend((p1[0], p2[0]), ('Men', 'Women'), frameon=False)
# We need to draw the canvas, otherwise the labels won't be positioned and 
# won't have values yet.
#fig.canvas.draw()
#labels = [item.get_text() for item in ax.get_xticklabels()]
#labels[1] = 'Test'
#ax.set_xticklabels(labels)
'''
for s in DegFreqBySlice.keys():
    print (str(SLICES.slices['segments'][s]['label'])+'\t'+str(DegFreqBySlice[s])+'\n')

print (str(tickloc))
print (str(all_degrees))
print('')
for deg in palette.keys():
    print(str(deg).ljust(5,' ')+str(palette[deg]))
'''
###################################################    
