import matplotlib as mpl
mpl.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm 
import matplotlib.colors as mcolors
import  socket, math, time, numpy as np
from matplotlib import rcParams
import matplotlib.font_manager as font_manager

from collections import Counter
from worker_wheel import assign_range


slices =                       {    'interval':10,
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
                                }

#######################################################################################                            
def cruncher4 (Gs,Bs,Ds,Xs,slices): # relative COUNT of genes in each slice regardless if gene is IN or OUT knapsack
    instance_size = len(Gs)
    tmp_count     = {}
    for slice_id in slices['segments'].keys():
        tmp_count[slice_id]=[]
    
    for g,b,d in zip (Gs, Bs, Ds):
        the_right_slice_id = assign_range(slices, b, d)
        degree          = sum([int(deg) for deg in g.split('$')[1:]])
        tmp_count[the_right_slice_id].append(degree)       # <<<<<<<<<<<<<<<
    #print (str(tmp_count))    
    tmp_freq = {}
    for slice_id in tmp_count.keys(): # 1, 2, ... 
        freq = Counter (tmp_count[slice_id]) # freq is a dictionary
        tmp_freq[slice_id]={}
        for degree in freq.keys():
            tmp_freq[slice_id][degree]=freq[degree]

    #print ('\n\n'+str(tmp_freq))    
    check = 0
    for slice_id in tmp_freq.keys():
        #--------------------------------------------------
        normalizer = float(sum(tmp_freq[slice_id].values())) # normalizer = the total number of genes in a given b:d slice
        check +=normalizer
        #--------------------------------------------------
        for degree in tmp_freq[slice_id].keys():
            tmp_freq[slice_id][degree] =  tmp_freq[slice_id][degree] / normalizer
    assert check == instance_size
    #print ('\n\n'+str(tmp_freq))
    for slice_id in tmp_freq.keys():
        for degree in tmp_freq[slice_id].keys():
            if degree not in slices['segments'][slice_id]['degree_freq'].keys():
                slices['segments'][slice_id]['degree_freq'][degree] = {'avg_so_far':tmp_freq[slice_id][degree],'count_so_far':1}
            else:
                count_so_far = slices['segments'][slice_id]['degree_freq'][degree]['count_so_far']
                avg_so_far   = slices['segments'][slice_id]['degree_freq'][degree]['avg_so_far']
                new_count    = count_so_far + 1
                new_avg      = ((avg_so_far*count_so_far) + tmp_freq[slice_id][degree]) / new_count
                slices['segments'][slice_id]['degree_freq'][degree]['avg_so_far']   = new_avg
                slices['segments'][slice_id]['degree_freq'][degree]['count_so_far'] = new_count 
    #for key in slices['segments'].keys():
    #    print (str(slices['segments'][key]['label']).ljust(8,' ')+str(slices['segments'][key]['degree_freq']))
    #print("========"*20)
#######################################################################################
def plot_next_bar2d(slices, ax, title, configs):
    normalizer = 0 
    patch_labels = []
    
    #-------JSON serialization/deserialization results in all 'int' keys becoming 'str' -------------
    sorted_keys   = [str(key) for key in sorted([int(key) for key in slices['segments'].keys()])]
    #------------------------------------------------------------------------------------------------
    explode_index = 0
    for key in sorted_keys:
        slices['segments'][key]['avg'] = np.average (slices['segments'][key]['fractions'])
        slices['segments'][key]['std'] = np.std     (slices['segments'][key]['fractions'])
        normalizer          += slices['segments'][key]['avg']
        patch_labels.append(str(slices['segments'][key]['label']))
      
    sizes         = [slices['segments'][key]['avg']/normalizer for key in sorted_keys]
    colors        = [slices['segments'][key]['color']          for key in sorted_keys]
    

    font_path = util.slash(os.getenv('HOME'))+'.fonts/merriweather/Merriweather-Bold.ttf'
    prop = font_manager.FontProperties(fname=font_path)
    family = prop.get_name() 
    
    patches, texts, autotexts = ax.pie (sizes, explode=explode, colors=colors,
                                         autopct='%1.1f%%', shadow=False, startangle=0, frame=False,
                                         wedgeprops = { 'linewidth': 0 },
                                         textprops={'family':family,'color':'white', 'fontsize':8,'weight':'bold'} )
    updated_patch_labels = []
    i=0 
    #with standard dev.
    for p,t in zip(patch_labels,autotexts):
        updated_patch_labels.append( p.ljust(8,' ') + ' ('+t.get_text().ljust(8,' ')+'\u00B1'+str(round(slices['segments'][sorted_keys[i]]['std'],2))+')')
        i+=1

    
    ax.legend(patches, updated_patch_labels, loc=(1.02,0.1), frameon=False, fontsize=8)    
    ax.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
    
    ax.set_xticks([])
    ax.set_xlabel (title) 
    del slices
    return True
#######################################################################################
def process_instances (slices, file_path, num_lines, configs, cruncher):
    #-------------------------------------
    df = open (file_path, 'r')
    #-------------------------------------   
    lines_so_far = 0
    while lines_so_far < num_lines:                
        Gs     = [g for g in next(df).strip().split()]
        Bs     = [int(s) for s in next(df).strip().split()]
        Ds     = [int(s) for s in next(df).strip().split()]
        Xs     = [int(x) for x in next(df).strip().split()]  #skip over Xs (solution vector)
        next(df)                                     #skip over coresize/exec_time
        lines_so_far += 5         
        assert len(Bs) == len(Ds)

        if len(Bs)>0:
            cruncher4(Gs,Bs,Ds,Xs,slices)    
    return slices
#######################################################################################
slices = process_instances(slices, 'p100.csv',1000,None,None)

fig = plt.figure()
fig.suptitle('\ntitle', y=1)  
ax = fig.add_subplot(1, 1, 1) 
#plot_next_bar2d(slices, ax, 'title', {})
'''
for index in slices['segments'].keys():
    for degree in slices['segments'][index]['degree_freq'].keys():
        count=slices['segments'][index]['degree_freq'][degree]['count_so_far']
        avg =slices['segments'][index]['degree_freq'][degree]['avg_so_far']
        print ('('+str(degree)+','+ str(count)+','+str(avg)+') ', end='')
'''
print ("slices = "+str(slices))
print("")