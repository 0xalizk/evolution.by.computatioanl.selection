import sys, os
sys.path.insert(0, os.getenv('lib'))
from scipy import stats as scipy_stats
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm 
import matplotlib.colors as mcolors
import  socket, math, time, numpy as np
from multiprocessing import Process
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import init_plotting as init, util_plotting as util, json
from collections import OrderedDict
font_path = util.slash(os.getenv('HOME'))+'.fonts/adobe/Adobe_Caslon_Pro_Regular.ttf'

##########################################################################################################################################
def setup(plasmid, fractions, bases_colors): 
    
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
    prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = prop.get_name() 
    
    configs                        = {}
    configs['plotting_configs']    = {
                                    'fig_suptitle':          "Schematic of Plasmid", 
                                    'fig_suptitle_fontsize': 18,   
                                    'plot':                  "green_grey_red",
                                    'xlabel':                "Circular Plasmid", 
                                    'ylabel':                "",
                                    'cbar_label':            None,
                                    'cbar_labelsize':        None,
                                    'marker':                None,
                                    'alpha':                 1,
                                    'cbar_labelsize':        None,
                                    'wspace':                0.4,
                                    'hspace':                0.4,
                                    'projection':            None,
                                    'dpi':                   300,
                                    'file_extension':        'png'

                                } 
    configs['base_color']          = bases_colors
    configs['plasmid_sequence']    = plasmid
    configs['slices']              = {} # a slice for each base + 2 big slices: amplicon, rest of plasmid

    # I want the primer region to be 10% of the whole circle: 
    primer_fraction, ampilicon_fraction, the_rest = fractions[0], fractions[1], fractions[2]
    primer_segment_length                             = float(len([b for b in configs['plasmid_sequence'] if b in ['c','g','t','a']]))
    pie_size                                          = primer_segment_length/primer_fraction

    for i in range(len(configs['plasmid_sequence'])):
        base, mag = configs['plasmid_sequence'][i], 0
        if base in ['c','g','a','t']:
            mag = (primer_fraction * pie_size)/primer_segment_length
            #print (str(mag))
        elif base == 'X': # 70% of what remains of the circle
            mag = ampilicon_fraction*(1-primer_fraction)*pie_size
            #print ("X "+str(mag))
        elif base == 'Y': # 30% of what remains of the circle
            mag      =  the_rest*(1-primer_fraction)*pie_size
            #print ("Y "+str(mag))
        
        else:
            print ("I don't recognize this plasmid segment: "+configs['plasmid_sequence'][i]+"\nExiting .. ")
            sys.exit(1)
        
        label = None
        if base== 'X':
            label = "EGFP"
        if base.lower() in ['c','g','t','a']:
            label = base.upper()
        configs['slices'][i] = {'color':configs['base_color'][base], 'mag':mag,'label':label}

    return configs
##################################################################
def strand (configs, ax, start_angle, radius):

	slices = configs['slices']
	normalizer = 0 
	patch_labels = []

	sorted_keys   = [key for key in sorted([int(key) for key in slices.keys()],reverse=True)]

	sizes         = [slices[key]['mag']    for key in sorted_keys]
	colors        = [slices[key]['color']  for key in sorted_keys]
	explode       = [0]*len(sorted_keys)  # only "explode" the 2nd slice (i.e. 'Hogs')
	
	
	# autopct = '%.0f%%' '%1.1f%%'
	patches, patches_texts, on_slice_texts = ax.pie (sizes, explode=explode, colors=colors,
										 autopct='%1.1f%%', shadow=False, startangle=start_angle, frame=False,radius=radius,
										 wedgeprops = { 'linewidth': 0, 'fill':True },
										 textprops={'family':rcParams['font.family'],'color':'white', 'fontsize':15,'weight':'bold'} )

	for T in  on_slice_texts:# the text appearing on each slice (auto = % of that slice)
		T.set_text('')

	my_handles = []
	done       = []
	for key in slices.keys():
		if slices[key]['color'] not in done and slices[key]['label'] !=None: #no duplicate patches, I'm assuming the same color is not used for more than one thing (base)
			my_handles.append(mpatches.Patch(color=slices[key]['color'], label=slices[key]['label'].upper()))
			done.append(slices[key]['color'])
	
	ax.legend(handles=my_handles, loc=(0.9,0.1), frameon=False, fontsize=8)    
   
	ax.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
	ax.set_xticks([])
	ax.set_xlabel (configs['plotting_configs']['xlabel']) 
	ax.text(-.25, 0, "Plasmid", size=16, color='#660066')
##################################################################
def assign_colors(configs,index):
    slices = configs['slices']
    start       = 2
    skip        = 0
    distinction = len(slices.keys())#len([key for key in slices.keys() if slices[key]['color']==None]) # the higher the more distinct the colors will be            
    colors  = [         iter(cm.GnBu     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.YlOrBr   (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.YlGn     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Spectral (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Blues    (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Dark2    (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Paired   (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Set1     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.jet      (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.cool     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.BuGn     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.OrRd     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.OrRd     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.YlOrRd   (np.linspace(0,1,  (distinction*(skip+1))+start))),                       
                ] #http://matplotlib.org/users/colormaps.html    
    c = colors[index]
    for i in range(start):
        next(c)
          
    for key in sorted(slices.keys(), reverse=True):
        if key == configs['slices']['intervals']:
            slices[key]['color']='red'
        elif key == (configs['slices']['intervals']-1):
            slices[key]['color']='green'
        else:
            for i in range(skip):
                next(c)
            slices[key]['color'] = next(c)
##################################################################
def circle(color,linewidth,fill,radius):
    centre_circle = plt.Circle((0,0), radius, color=color, linewidth=linewidth, fill=fill)    
    ax.add_artist(centre_circle)  
##################################################################
if __name__ == "__main__":
    
    figure_size    = (6, 4) #(width, height)
    fig            = plt.figure(figsize=figure_size) 
    ax             = fig.add_subplot(1, 1, 1)
    
    bc1            = {'c':"#ffff33",'g':"#ff8000",'a':"#ff4dff",'t':"#0667f9", 'X':"white",'Y':"white"}    
    bc2            = {'c':"#ffff33",'g':"#ff8000",'a':"#ff4dff",'t':"#0667f9", 'X':"green",'Y':"#e6e6e6"}
    bc3            = {'c':"#ffff33",'g':"#ff8000",'a':"#ff4dff",'t':"#0667f9", 'X':"green",'Y':"#e6e6e6"}  
    
    sense          = "gtttagtgaaccgtcagatccgctagcgctaccggtcgccaXgtttagtgaaccgtcagatccgctagcgctaccggtcgccaY"
    asense         = "caaatcacttggcagtctaggcgatcgcgatggccagcggtXcaaatcacttggcagtctaggcgatcgcgatggccagcggtY"
    configs1       = setup(sense,  [0.3, 0.08, 0.62], bc1) # setup(plasmid, fractions, bases_colors)
    configs2       = setup(sense,  [0.1, 0.20, 0.70], bc2)
    configs3       = setup(asense,  [0.1, 0.20, 0.70], bc3)
    r              = 1.1
    #--------------------------------------------------------------
    strand      (configs1, ax, 107,   r-.1) # strand (configs, ax, start_angle, radius)
    circle      ('white', 10, False, r-0.2)
    
    strand      (configs2, ax, 80,   r-0.24)
    circle      ('white', 2, False,  r-0.30)
    
    strand      (configs3, ax, 80,   r-0.30) 
    circle      ('white', 0, True,   r-0.35)
    #--------------------------------------------------------------
    print ('saving: '+"plasmid."+configs1['plotting_configs']['file_extension'])
    plt.savefig("plasmid."+configs1['plotting_configs']['file_extension'], dpi=configs1['plotting_configs']['dpi'], bbox_inches="tight")
    
##################################################################