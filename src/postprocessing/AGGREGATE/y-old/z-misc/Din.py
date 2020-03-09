import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
#import seaborn as sns
import os,sys

zlim = 5000
Z_label = 'Incurred Damages'
input =str(sys.argv[1])
measure = 'Din_avg'
color = 'red'

rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 16
rcParams['xtick.labelsize'] = 8
rcParams['ytick.labelsize'] = 8
#rcParams['legend.fontsize'] = 14
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Utopia']
rcParams['grid.alpha'] = 0.1

rcParams['axes.grid']=False
rcParams['ytick.minor.pad']=0.1
rcParams['ytick.major.pad']=0.1
rcParams['savefig.pad_inches']=1
rcParams['grid.color']='white'
#rcParams['axes.labelpad ']=1


#sns.set_style("ticks", {"xtick.major.size": 4, "ytick.major.size": 4})
#sns.set_style("white")
#sns.despine()
#bar3d(x, y, z, dx, dy, dz, color='b', zsort='average', *args, **kwargs)
#sns.set()



df = pd.read_csv(input,header=0,delimiter='\t', dtype='float32')


Bin = (df[measure].tolist())


Bin = (np.array(Bin)).reshape(10, 10)			#z
#Bin.transpose()
Ts, Ps  = np.meshgrid( np.arange(Bin.shape[0]), np.arange(Bin.shape[1]))

Bin, Ps, Ts = Bin.flatten(), Ps.flatten(), Ts.flatten()

#print (Bin)
#print (Ps)
#print (Ts)
dx = [.5]*(len(Ps))
dy = [.5]*(len(Ts))
z = [0.0]*len(Ts)

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
#ax= Axes3D(fig)
for key in  rcParams.keys():#sns.axes_style().keys():
    #print (key +"\t\t"+str(sns.axes_style()[key]))
    print (key +"\t\t"+str(rcParams[key]))
ax.bar3d (Ts, Ps, z, dx, dy, Bin ,alpha=1,color=color)



#ticks = np.arange(0.5, 10, 1)
ticks = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
ax.set_xticks(ticks)
#ticks = np.arange (0.5,10, 1)
ticks.reverse()
ax.set_yticks(ticks)

xlabels = ['0.1','1','5','10','15','20','25','50','75','100']
ylabels = ['100','75','50','25','20','15','10','5','1','0.1']
ax.w_xaxis.set_ticklabels(xlabels)
ax.w_yaxis.set_ticklabels(ylabels)
ax.set_xlabel('Tolerance (% edges)')
ax.set_ylabel('Pressure (% nodes)')
ax.set_zlabel(Z_label)
ax.set_zlim(top=zlim)
'''
for ii in range(305,321,5):
    for jj in range(10, 18, 2):
        ax.view_init(elev=jj, azim=ii)
        plt.savefig("img/movie"+str(ii)+"-"+str(jj)+".png")

for ii in range(1,20,1):
    ax.view_init(elev=ii, azim=320)
    plt.savefig("img/movie"+str(320)+"-"+str(ii)+".png")
'''
ax.view_init(elev=16,azim=305)
plt.savefig(input[0:-4]+"-"+measure+".png", dpi=300)

#ax.bar3d(np.array(Ts), np.array(Ps), 0, np.array(dx), np.array(dy), np.array(Bin))
#ax.bar3d((np.array(Ts)).flatten(), (np.array(Ps)).flatten(), 0, (np.array(dx)).flatten(), (np.array(dy)).flatten(), (np.array(Bin)).flatten())

'''
print (Ps)
print ("\n")
print ((Ts))
print ("\n")
print ((Bin))
print ("\n")

print (len(dx))
print ("\n")
print (len(dy))
print ("\n")
print (len(z))
print ("\n")
'''

