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
        print ('Usage: python3 [input-file (containing paths to BY_GENE.csv files) ] \nExiting...')
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

    input_file, plots_dir = getCommandLineArg(), os.path.join(os.getcwd(),'plots')
    if not os.path.isdir(plots_dir):
        os.mkdir(plots_dir)
    datapoints_files = open (input_file).readlines()
    
    verify = True
    

        
    #fig = plt.figure(figsize=(30, 70))
    fig = plt.figure()
    fig.subplots_adjust(hspace = .2, wspace=.2)

    pos=1
    PAIRS = getPairs (datapoints_files)
    for pair in PAIRS:
        data_file1, data_file2 = pair[0].strip() ,  pair[1].strip() 
        title1, title2 = data_file1.split('/')[-1].split('_BY_GENE_')[0], data_file2.split('/')[-1].split('_BY_GENE_')[0]
        print ("\t\tplotting "+str(data_file1.split('/')[-1])+"\n\t\tplotting "+str(data_file2.split('/')[-1]))
        df1                  = open (data_file1, 'r').readlines()
        df2                  = open (data_file2, 'r').readlines()
           
        Bs1 =  [int(b) for b in df1[0].strip().split(' ')]
        Bs2 =  [int(b) for b in df2[0].strip().split(' ')]
        Ds1 =  [int(d) for d in df1[1].strip().split(' ')]
        Ds2 =  [int(d) for d in df2[1].strip().split(' ')]
        
        x_max = max (max(Bs1), max(Bs2))
        y_max = max (max(Ds1), max(Ds2))
        print ("x_max "+str(x_max))
        print ("y_max "+str(y_max))
        for  df, col, title in [(df1,0, title1), (df2,1, title2)]:

            Bs =  [int(b) for b in df[0].strip().split(' ')]
            Ds =  [int(d) for d in df[1].strip().split(' ')]
                
                  
            ax = fig.add_subplot(len(PAIRS), 2 ,pos+col)
            #ax.set_xlabel ('Benefits')
            #ax.set_ylabel ('Damages')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_xticks (  [x  for x in range(0, x_max+1, 10)]  )
            ax.set_yticks (  [y  for y in range(0, y_max+1, 10)]   )
            ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
            ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks
            
                    
            ax.scatter (Ds, Bs, color ='black', alpha=alpha, marker=marker)
        
        pos +=2                          
    
    #plt.tight_layout(pad=0.1, h_pad=None, w_pad=None, rect=None)
    plt.savefig(plots_dir+"/BD_corr_plot.png")
