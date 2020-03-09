import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
import numpy as np
import pandas as pd
from matplotlib import rcParams
#import seaborn as sns
import os,sys
import math

pd.set_option('display.precision', 3)

marker='.'
markersize=5
linestyle= '' #'dotted' # 'solid'   'dashed'   'None'
alpha=.7
markeredgecolor='none' 


rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 16
rcParams['xtick.labelsize'] = 8
rcParams['ytick.labelsize'] = 8
#rcParams['font.family'] = 'sans-serif'  
#rcParams['font.family'] = 'serif'  
rcParams['font.serif']= 'DejaVu Sans' #['Bitstream Vera Sans', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
rcParams['grid.alpha'] = 0.1
rcParams['axes.grid']=False
rcParams['ytick.minor.pad']=0.01
rcParams['ytick.major.pad']=0.01
rcParams['savefig.pad_inches']=.01
rcParams['grid.color']='white'
#rcParams['legend.facecolor']='#FFFFFF'
#rcParams['figure.frameon']=True
#rcParams['savefig.frameon']=True

#--------------------------------------------------------------------------------------
def getCommandLineArg():
    try:
        input_file  = str(sys.argv[1])
    except:
        print ('Usage: python3 plot_singles.py [input-file (line1: benefits, line2: damages) ] \nExiting...')
        sys.exit(1)
    return input_file
#--------------------------------------------------------------------------------------
def getPairs (BY_GENE_datafiles):
    PAIRS = []
    counter = 0
    for f in range(int(len(BY_GENE_datafiles)/2)):
        network1 = BY_GENE_datafiles[counter].strip()
        network2 = BY_GENE_datafiles[counter+1].strip()
        
        PAIRS.append([  network1, network2])
        counter +=2
    return PAIRS
#--------------------------------------------------------------------------------------  

if __name__ == "__main__": 

    input_file, plots_dir = getCommandLineArg(), os.path.join(os.getcwd(),'plots_singles')
    if not os.path.isdir(plots_dir):
        os.mkdir(plots_dir)    

    fig = plt.figure()
    fig.subplots_adjust(hspace = .2, wspace=.2)
        
    df                  = open (input_file, 'r').readlines()       
  
    Bs =  [int(b) for b in df[0].strip().split(' ')]
    Ds =  [int(d) for d in df[1].strip().split(' ')]
    x_max = max (max(Bs), max(Bs))
    y_max = max (max(Ds), max(Ds))
                    
    ax = fig.add_subplot(1, 1 ,1)
    #ax.set_xlabel ('Benefits')
    #ax.set_ylabel ('Damages')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks (  [x  for x in range(0, x_max+1, 10)]  )
    ax.set_yticks (  [y  for y in range(0, y_max+1, 10)]   )
    ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
    ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks
                           
    ax.scatter (Ds, Bs, color ='black', alpha=alpha, marker=marker)
   
    #plt.tight_layout(pad=0.1, h_pad=None, w_pad=None, rect=None)
    plt.savefig(plots_dir+"/"+str(input_file.split('/')[-1].split('.')[0])+".png")
    print ("\t\tplotted: "   +str(input_file.split('/')[-1].split('.')[0])+".png")
