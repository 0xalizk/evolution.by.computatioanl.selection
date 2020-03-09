import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
#import seaborn as sns
import os,sys

params = (open (str(sys.argv[1]),'r')).readlines()

data_file = (str(params[0].split('=')[1])).strip()
zlim = int((params[1].split('=')[1]).strip())
        
rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 16
rcParams['xtick.labelsize'] = 8
rcParams['ytick.labelsize'] = 8
#rcParams['legend.fontsize'] = 14
#rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Utopia']
rcParams['grid.alpha'] = 0.1
rcParams['axes.grid']=False
rcParams['ytick.minor.pad']=0.1
rcParams['ytick.major.pad']=0.1
rcParams['savefig.pad_inches']=1
rcParams['grid.color']='white'
#rcParams['axes.labelpad ']=1


df = pd.read_csv(data_file,header=0,delimiter='\t', dtype='float32')

plots = {
         'Bin':           {'color':'green', 'measure_column':'Bin_avg',        'Z_label':'Benefits (knapsack value)'},
         'Din':           {'color':'red',   'measure_column':'Din_avg',        'Z_label':'Damages (knapsack weight)'},
         'Bout':          {'color':'red',   'measure_column':'Bout_avg',       'Z_label':'Bout'},
         'Dout':          {'color':'green', 'measure_column':'Dout_avg',       'Z_label':'Dout'},
         'Bin_over_Din':  {'color':'green', 'measure_column':'Bin_over_Din',   'Z_label':'Bin_over_Din'},
         'Bin_over_Bout': {'color':'green', 'measure_column':'Bin_over_Bout',  'Z_label':'Bin_over_Bout'},
         'Dout_over_Din': {'color':'green', 'measure_column':'Dout_over_Din',  'Z_label':'Dout_over_Din'},
         'Bout_over_Dout':{'color':'green', 'measure_column':'Bout_over_Dout', 'Z_label':'Bout_over_Dout'},
         'Bout_over_Bin': {'color':'red',   'measure_column':'Bout_over_Bin',  'Z_label':'Bout_over_Bin'}
        }

for measure in plots.keys():
    print (measure)
    zdata = (df[plots[measure]['measure_column']].tolist())
    zdata = (np.array(zdata)).reshape(10, 10)			#z
    Ts, Ps  = np.meshgrid( np.arange(zdata.shape[0]), np.arange(zdata.shape[1]))
    zdata, Ps, Ts = zdata.flatten(), Ps.flatten(), Ts.flatten()
    
    dx = [.5]*(len(Ps))
    dy = [.5]*(len(Ts))
    z = [0.0]*len(Ts)
    
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')

    ax.bar3d (Ts, Ps, z, dx, dy, zdata ,alpha=1,color=plots[measure]['color'])

    #ticks = np.arange(0.5, 10, 1)
    ticks = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
    ax.set_xticks(ticks)
    ticks.reverse()
    ax.set_yticks(ticks)

    xlabels = ['0.1','1','5','10','15','20','25','50','75','100']
    ylabels = ['100','75','50','25','20','15','10','5','1','0.1']
    ax.w_xaxis.set_ticklabels(xlabels)
    ax.w_yaxis.set_ticklabels(ylabels)
    ax.set_xlabel('Tolerance (% edges)')
    ax.set_ylabel('Pressure (% nodes)')
    ax.set_zlabel(plots[measure]['Z_label'])
    ax.set_zlim(top=zlim)
    ax.set_zlim(top=zlim)

    ax.view_init(elev=16,azim=305)
    plt.savefig(data_file[0:-4]+"-"+plots[measure]['measure_column']+".png", dpi=100)







#for key in  rcParams.keys():#sns.axes_style().keys():
    #print (key +"\t\t"+str(sns.axes_style()[key]))
    #print (key +"\t\t"+str(rcParams[key]))
    

#sns.set_style("ticks", {"xtick.major.size": 4, "ytick.major.size": 4})
#sns.set_style("white")
#sns.despine()
#bar3d(x, y, z, dx, dy, dz, color='b', zsort='average', *args, **kwargs)
#sns.set()


'''
for ii in range(305,321,5):
    for jj in range(10, 18, 2):
        ax.view_init(elev=jj, azim=ii)
        plt.savefig("img/movie"+str(ii)+"-"+str(jj)+".png")

for ii in range(1,20,1):
    ax.view_init(elev=ii, azim=320)
    plt.savefig("img/movie"+str(320)+"-"+str(ii)+".png")
'''
