#/home/mosha/EvoByCompSel/parallel/Release-03/src/simulation/output/01_resilience_simulation/data_points/Neural_BY_GENE_datapoints_February-26-2016-h03m21s14.csv
import matplotlib
matplotlib.use('Agg') # This must be done before importing matplotlib.pyplot
import matplotlib.pyplot as plt, matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
matplotlib.style.use('ggplot')
#input = open ("/home/mosha/EvoByCompSel/parallel/Release-03/src/simulation/output/01_resilience_simulation/data_points/Neural_BY_GENE_datapoints_February-26-2016-h03m21s14.csv", "r")
#df = pd.read_csv("/home/mosha/EvoByCompSel/parallel/Release-03/src/simulation/output/01_resilience_simulation/data_points/Neural_BY_GENE_datapoints_February-26-2016-h03m21s14.csv")

#df = pd.read_csv("output/01_resilience_simulation/data_points/Neural_BY_GENE_datapoints_February-26-2016-h03m21s14.csv")
df = pd.read_csv('output/01_resilience_simulation/data_points/Neural_AGGREGATE_datapoints_February-26-2016-h03m21s14.csv',header=0,delimiter='\t', dtype='float64')

fig = plt.figure(figsize=(10, 10), dpi=150)
ax1 = fig.add_subplot(111,projection='3d')

xpos = [1,2,3,4,5,6,7,8,9,10]
ypos = [1,2,3,4,5,6,7,8,9,10]
zpos = [0,0,0,0,0,0,0,0,0,0]

xposM, yposM = np.meshgrid(xpos, ypos, copy=False)

dx   = np.ones(10)
dy   = np.ones(10)
#dz   = [1,2,3,4,5,6,7,8,9,10]
dz    = df['Bin_avg'].tolist()

print (str(len(dz)))
dz1   = dz[0:10]
dz2   = dz[10:20]
dz3   = dz[20:30]
dz4   = dz[30:40]
dz5   = dz[40:50]
dz6   = dz[50:60]
dz7   = dz[60:70]
dz8   = dz[70:80]
dz9   = dz[80:90]
dz10  = dz[90:]

#Z=np.array(dz)
#Z.reshape((10,10))

#Z = np.array([dz1,dz2,dz3,dz4,dz5,dz6,dz7,dz8,dz9,dz10])
#Z.reshape((10,10))
#print (Z)
Z = [dz1,dz2,dz3,dz4,dz5,dz6,dz7,dz8,dz9,dz10]

ax1.bar3d (xposM.flatten(), yposM.flatten(), zpos, dx, dy, Z, color='red')
plt.savefig('fig.png')





#df.to_csv('foo.csv')
print ("here we go")


