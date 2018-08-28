import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
df = pd.read_csv('output/01_resilience_simulation/data_points/Neural_AGGREGATE_datapoints_February-26-2016-h03m21s14.csv',header=0,delimiter='\t', dtype='float64')
dz    = df['Bin_avg'].tolist()

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

data_2d = [dz1,dz2,dz3,dz4,dz5,dz6,dz7,dz8,dz9,dz10]


#
# Assuming you have "2D" dataset like the following that you need
# to plot.
#
'''data_2d = [ [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [11, 12, 13, 14, 15, 16, 17, 18 , 19, 20],
            [16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
            [21, 22, 23, 24, 25, 26, 27, 28, 29, 30] ]
'''#
# Convert it into an numpy array.
#
data_array = np.array(data_2d)
#
# Create a figure for plotting the data as a 3D histogram.
#
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sns.axes_style("whitegrid")
#
# Create an X-Y mesh of the same dimension as the 2D data. You can
# think of this as the floor of the plot.
#
x_data, y_data = np.meshgrid( np.arange(data_array.shape[1]),
                              np.arange(data_array.shape[0]) )
#
# Flatten out the arrays so that they may be passed to "ax.bar3d".
# Basically, ax.bar3d expects three one-dimensional arrays:
# x_data, y_data, z_data. The following call boils down to picking
# one entry from each array and plotting a bar to from
# (x_data[i], y_data[i], 0) to (x_data[i], y_data[i], z_data[i]).
#
x_data = x_data.flatten()
y_data = y_data.flatten()
z_data = data_array.flatten()
ax.bar3d( x_data, y_data, np.zeros(len(z_data)),
          0.5, 0.5, z_data )
print (x_data)
print ("\n")
print (y_data)
print ("\n")
print (z_data)
print ("\n")

#bar3d(x, y, z, dx, dy, dz, color='b', zsort='average', *args, **kwargs)
#
# Finally, display the plot.
plt.savefig('test.png')
