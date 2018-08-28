import matplotlib as mpl
import matplotlib.pyplot as plt, math
import numpy as np
import matplotlib.ticker as ticker

def z_tick_formatter (z, pos):
    # The two args are the value and tick position
    print ("z "+str(z)+"\tpos "+str(pos))
    return (str(int(z)))

     
zoffset        = 0
bounds        = []
magnitudes    = []
MEASURE_TOTAL = 0.0
width         = 0.1
fig           = plt.figure(figsize=(10,10))
ax            = fig.add_subplot (1, 1, 1)
yticks        = []
ylabels       = []

Sbin          = {1: 3895, 2: 3895, 3: 3895, 4: 3895, 5: 3895, 6: 3895, 7: 3895, 8: 3895, 9: 3895, 10: 3895, 11: 3895, 17: 3895, 83: 3895, 21: 3895, 22: 3895, 25: 3895, 26: 3895, 27: 3895, 86: 3895, 35: 3895, 47: 3895, 50: 3895, 53: 3895, 54: 3895, 57: 3895, 58: 3895}
num_instances = 3895.0
cmap          = plt.get_cmap("YlGn") # YlOrRd (Din)
cmaplist      = [cmap(i) for i in range(cmap.N)] # extract all colors from the  cmap
interval      = math.ceil(float(len(cmaplist))/(len(Sbin.keys())))
colors_steps  = [i for i in range(len(cmaplist)) if i%interval==0]
assert len(colors_steps) == len(Sbin.keys())

for key in sorted(Sbin.keys()):
    current_contribution = (float(Sbin[key])/num_instances)*key
    magnitudes.append(current_contribution)
for i in range(len(magnitudes)):
    ax.bar(1, magnitudes[i], width,color=cmaplist[colors_steps[i]],bottom=zoffset,edgecolor='black',linewidth=.2)
    zoffset+=magnitudes[i]
    bounds.append(zoffset)
    print (str(magnitudes[i])+'\t'+str(colors_steps[i])+'\t'+str(zoffset)+"")

ax.set_yscale('log',basey=2)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(z_tick_formatter))

print ("len(Sbin) "      +str(len(Sbin.keys())))
print ("colors_steps ("+str(len(colors_steps))+"): " +str(colors_steps))
print ("sorted "+str(sorted(Sbin.keys())))
print ("magnit "+str([int(i) for i in magnitudes]))
print ("sum magnit "+str(sum(magnitudes)))
print ("yticks "+str(ax.get_yticks()))

plt.show()

'''
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,  ticks=magnitudes, boundaries=bounds)
'''

#ax.set_yticks(yticks)
#ax.yaxis.set_ticklabels(ylabels)

#ax.set_ylabels(ylabels)
#ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

#reversed (useful with 'summer' cmap):
#colors_steps          = [i for i in range(len(cmaplist)-1,-1,-1) if i%math.ceil(float(len(cmaplist))/(len(Sbin.keys())))==0]
'''    
p1 = plt.bar(ind, menMeans, width, color='r', yerr=menStd)
p2 = plt.bar(ind, womenMeans, width, color='y',
             zoffset=menMeans, yerr=womenStd)
'''

'''
100/0.1
{
	'Bin': {'EFF': 727.0, 'TOT': 1379.8795892169449}
	'Bou': {'EFF': 9.627471116816432, 'TOT': 12.136842105263158}, 
	'Din': {'EFF': 0.98485237483953791, 'TOT': 0.98485237483953791}, 
	'Dou': {'EFF': 3.3268292682926828, 'TOT': 4.998716302952503}, 
	
	'Sdou': {1: 3836, 2: 1263, 3: 1191, 4: 617, 5: 111}, 
	'Sbin': {1: 3895, 2: 3895, 3: 3895, 4: 3895, 5: 3895, 6: 3895, 7: 3895, 8: 3895, 9: 3895, 10: 3895, 11: 3895, 17: 3895, 83: 3895, 21: 3895, 22: 3895, 25: 3895, 26: 3895, 27: 3895, 86: 3895, 35: 3895, 47: 3895, 50: 3895, 53: 3895, 54: 3895, 57: 3895, 58: 3895}, 
	'Sbou': {0: 2000, 1: 617, 2: 1191, 3: 1263, 4: 2426, 5: 3047, 6: 962}, 
	'Sdin': {0: 3895, 1: 3836}, 
	
	'num_instances': 3895.0, 
}
'''