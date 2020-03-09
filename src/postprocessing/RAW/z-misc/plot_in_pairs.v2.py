from scipy import stats as scipy_stats
import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as plticker
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from matplotlib import rcParams
#import seaborn as sns
import os,sys, socket
import math, time
from multiprocessing import Process

pd.set_option('display.precision', 3)

linestyle= '' #'dotted' # 'solid'   'dashed'   'None'
alpha=.5
markeredgecolor='none' 

rcParams['axes.labelsize'] = 8
rcParams['axes.titlesize'] = 8
rcParams['xtick.labelsize'] = 6
rcParams['ytick.labelsize'] = 6
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
def pf(num): # credit: http://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.0f%s' % (num, ['', 'K', 'M', 'B', 'T'][magnitude])
#--------------------------------------------------------------------------------------
def slash(path):
    return path+(path[-1] != '/')*'/'
#--------------------------------------------------------------------------------------
def getCommandLineArg():
    try:
        input_file , stamp = str(sys.argv[1]), str(sys.argv[2])
    except:
        print ('Usage: python3 plot_in_pairs.py [input-file (containing paths to RAW...csv files, see classify.py) ] [stamp: will be appended to output plots names] \nExiting...')
        sys.exit(1)
    return [input_file, stamp]
#--------------------------------------------------------------------------------------
def getPairs (datafiles, files_per_pair):
    PAIRS = []
    counter = 0
    if len(datafiles)%files_per_pair != 0:
        sys.stdout.write  ("\n<<<<<<<<<<<<<<<<<<<<<< WARNING: number of files % files_per_pair isn't even! (last file will be ignored)>>>>>>>>>>>>>>>>>>>>>>")
        datafiles = datafiles[0:int(len(datafiles)/files_per_pair)*files_per_pair]
    while counter < len(datafiles):
        tmp = [] 
        for i in range(counter, counter+files_per_pair, 1):
            tmp.append(datafiles[i])      
        PAIRS.append(tmp)   
        counter += files_per_pair
    SUBPLOTS = []     
    for pair in PAIRS:
        DATA_FILES=[]
        data_files = [p.strip() for p in pair]
        for df in data_files:
            spoint = '_RAW_INSTANCES_'
            if 'raw' in df.split('/')[-1].split('_') and 'instances' in df.split('/')[-1].split('_'):
                spoint = '_raw_instances_'
            DATA_FILES.append((df,spoint))
        #print (str(DATA_FILES))
        tmp        = [e[0].split('/')[-1].split(e[1]) for e in DATA_FILES]
        net_name   = [n[0] for n in tmp]
        suffix     = [n[1].split('_') for n in tmp] 
        titles     = [n+"\n[$"+s[0].replace('p','p=')+", "+s[1].replace('t','t=')+"$, "+s[2]+", "+s[3]+", "+s[4]+", "+s[5]+", "+s[6]  for n,s in zip(net_name, suffix)] # title will be later appended with num_instances +']' in PLOTTER
        SUBPLOTS.append ([e for e   in   zip(net_name, data_files, titles)])      
    return SUBPLOTS
#--------------------------------------------------------------------------------------
def calculate_Axis_limits (pair, configs):
    
    if configs['plot'] == "scatter_BD":
        max_B, max_D = 0, 0        
        num_lines =[]
        for prefix, file_path, title in pair:
            df = open (file_path, 'r').readlines()
            num_lines.append(len(df))
            assert len(df)%5 == 0
            for i in range(0,len(df),5):
                max_B    = max (max_B, max([int(b) for b in df[i+1].split() if b!='nil']))
                max_D    = max (max_D, max([int(d) for d in df[i+2].split() if d!='nil']))       
        if len(num_lines)==0:
            num_lines=[0]
        return [max_D, max_B, min(num_lines)]
    
    
    elif configs['plot']=='green_grey_red':
        max_y = 0
        num_lines=[]
        for prefix, file_path, title in pair:
            df = open (file_path, 'r').readlines()
            num_lines.append(len(df))
            assert len(df)%5 == 0
            for i in range(0,len(df),5):
                Bs     = [int(s) for s in df[i+1].split() if s!='nil']
                Ds     = [int(s) for s in df[i+2].split() if s!='nil']
                w, g, r, instance_size = 0, 0, 0, 0.0
                assert len(Bs) == len(Ds)
                if len(Bs)>0:
                    for b,d in zip (Bs, Ds):
                        instance_size += 1
                        if (b>0 and d==0):
                            w  += 1
                        elif (b>0 and d>0):
                            g   += 1
                        elif (b==0 and d>0):
                            r  += 1
                        else:
                            pass
                max_y = max (max_y, float(w)/instance_size, float(g)/instance_size, float(r)/instance_size)        
        if len(num_lines)==0:
            num_lines=[0]
        return [max_y, min(num_lines)]

    else: #percentiles
        max_y = 0
        num_lines =[] #in case both files don't have the same no. of instances, choose the minimum ==> fair comparison
        for prefix, file_path, title in pair:
            df = open (file_path, 'r').readlines()
            num_lines.append(len(df))
            assert len(df)%5 == 0
            perc_tuple = []
            for i in range(0,len(df),5):
                Bs     = [int(b) for b in df[i+1].split() if b!='nil']
                Xs     = [int(x) for x in df[i+3].split() if x!='nil']
                if len(Bs)>0:
                    max_y  = max (max_y, len([b for b in [b*x for b,x in zip(Bs, Xs)] if b !=0]))                

        return [max_y, min(num_lines)]
    
    '''
    elif configs['plot'] == "coresize":
        max_core = 0  
        for prefix, file_path, title in pair:
            cores =  []
            df = open (file_path, 'r').readlines()
            for i in range(0,len(df),5):
                stats = [int(s) for s in df[i+4].split() if s!='nil']
                assert len(stats)==2 or len(stats)==0
                if len(stats)>0:
                    cores = cores + [stats[0]] # stats[1] = execution_time
            relfreq = scipy_stats.relfreq(cores, numbins=10)
            x = relfreq.lowerlimit + np.linspace(0, relfreq.binsize*relfreq.frequency.size, relfreq.frequency.size)
            print (str(x))
            max_core = max(max_core, max(x))
        return max_core
    '''   
#--------------------------------------------------------------------------------------
def scatter_BD(df, fig, ax, configs):
    Bs_Ds = {}
    for i in range(0,configs['num_lines'],5):
        tmp_Bs    = [int(b) for b in df[i+1].split() if b!='nil']
        tmp_Ds    = [int(d) for d in df[i+2].split() if d!='nil']
        assert len(tmp_Bs) == len(tmp_Ds)
        if len(tmp_Bs)>0:
            for obj in zip(tmp_Bs, tmp_Ds):
                if obj in Bs_Ds.keys():
                    Bs_Ds[obj] +=1
                else:
                    Bs_Ds[obj] = 1
    Bs,Ds,frequency,colors = [],[],[],[]
    for obj in Bs_Ds.keys():
        Bs.append(obj[0])
        Ds.append(obj[1])
        frequency.append(Bs_Ds[obj])        
    #-------------------------------------------------------     
    frequency = ([math.log(f,2) for f in frequency])
    #-------------------------------------------------------    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    sc = ax.scatter (Ds, Bs, alpha=alpha, marker=configs['marker'], edgecolors='none',  c=frequency, cmap=configs['cmap'])                      
    cbar = fig.colorbar(sc, shrink=0.4, pad=0.01, aspect=20, fraction=.2) # 'aspect' ratio of long to short dimensions, # 'fraction' of original axes to use for colorbar
    cbar.outline.set_visible(False)
    cbar.set_label(configs['cbar_label'] )
    cbar_ax = cbar.ax
    cbar_ax.tick_params(axis='y', which='minor', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='off') 
    cbar_ax.tick_params(axis='y', which='major', bottom='off', top='off', left='off', right='off',  labelleft='off', labelright='on')
    cbar_ax.tick_params(axis='both', which='major', labelsize=configs['cbar_labelsize'])
        
    return sc
#--------------------------------------------------------------------------------------  
def coresize (df, ax, configs): 
    cores =  []  
    for i in range(0,configs['num_lines'],5):
        stats = [int(s) for s in df[i+4].split() if s!='nil']
        assert len(stats)==2 or len(stats)==0
        if len(stats)>0:
            cores = cores + [stats[0]] # stats[1] = execution_time
    relfreq = scipy_stats.relfreq(cores, numbins=10)
    #Calculate space of values for x
    x = relfreq.lowerlimit + np.linspace(0, relfreq.binsize*relfreq.frequency.size, relfreq.frequency.size)
    #ax.set_xlim([x.min(), x.max()])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    sc = ax.bar(x, relfreq.frequency, width=relfreq.binsize, color='forestgreen', edgecolor='none')
            
    return sc 
#--------------------------------------------------------------------------------------  
def polar (df, ax, configs): 
    Bs, Ds = [], []
    for i in range(0,configs['num_lines'],5):
        Bs    = [int(b) for b in df[i+1].split() if b!='nil']
        Ds    = [int(d) for d in df[i+2].split() if d!='nil']       
        assert len(Bs)==len(Ds)
        if len(Bs)>0:
            ax.scatter(Bs,Ds,marker=configs['marker'], cmap=configs['cmap'])
    return ax
#--------------------------------------------------------------------------------------  
def green_grey_red_bar (PAIRS, configs):

    fig = plt.figure(figsize=configs['fig_size'])
    y = 1.2 # y=1.08 determines space between fig title and subplots
    if len(PAIRS)>2:
        y=1
    fig.suptitle('\n'+configs['fig_suptitle'], fontsize=configs['fig_suptitle_fontsize'], y=y       )  
    savename = []
    pos=1   
    bar_width=0.15
    bar_spacing=0.01
    
    for  pair in PAIRS:  #rows
        title=[]
        ax = None
        axis_limits              = calculate_Axis_limits (pair, configs)
        configs['num_lines']     = axis_limits[-1]

        if configs['projection'] != None:
            ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos, projection=configs['projection'])
        else:                
            ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos)
        #----------------------------------------------------------------------------------------
        fig.subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['wspace'], hspace=configs['hspace'] )
        # the values of left, right, bottom and top are to be provided as fractions of the figure width and height. In additions, all values 
        # are measured from the left and bottom edges of the figure. This is why right and top can't be lower than left and right.
        #----------------------------------------------------------------------------------------
        ax.set_ylim([0,axis_limits[0]])        
        ax.grid(True)
        y_pos            = np.arange(3)      
        for tuple in pair: #columns        
            prefix, file_path = tuple[0], tuple[1]
            title.append(tuple[2])
            savename.append (prefix[0:6])

            title[-1] = title[-1]+", "+pf(configs['num_lines']/5)+" instances]"
            
            sys.stdout.write ("\n"+configs['plot'].ljust(13,' ')+"\t"+title[-1].replace('$','').ljust(65,' ')+"\t"+str(int(float(pos)*100/(len(PAIRS)*len(PAIRS[0]))))+" %")
            sys.stdout.flush()
            #-------------------------------------
            df = open (file_path, 'r').readlines()     
            #-------------------------------------       
            try:
                assert len(df) % 5 == 0 
            except:
                sys.stdout.write ("\n==================================================================================================================")
                sys.stdout.write ("\nWarning, no. lines not multiple of 5: "+str(file_path))
                sys.stdout.write ("\nI will chop off bad trailing lines")       
                sys.stdout.write ("\n==================================================================================================================")
                #----------------------------------------------------------------------------------------
                df = df[0:int(len(df)/5)*5]
                #----------------------------------------------------------------------------------------
                pass
            
            greens, greys, reds, warn,  = [], [], [], True
              
            for i in range(0,configs['num_lines'],5):
                Bs     = [int(s) for s in df[i+1].split() if s!='nil']
                Ds     = [int(s) for s in df[i+2].split() if s!='nil']
                w, g, r, duds, instance_size = 0, 0, 0, 0, 0.0
                assert len(Bs) == len(Ds)
                if len(Bs)>0:
                    for b,d in zip (Bs, Ds):
                        instance_size += 1
                        if (b>0 and d==0):
                            w  += 1
                        elif (b>0 and d>0):
                            g   += 1
                        elif (b==0 and d>0):
                            r  += 1              
                        else:
                            duds+=1
                            if warn:
                                sys.stdout.write ("\n\nWarning: in green_grey_red(): both b and d == 0, if this is a 'scramble' mode data this is ok, otherwise, this is FATAL. I won't warn about this again for this file ...\n\n")
                                warn = False

                    assert instance_size == len(Bs) == len(Ds) == (w+g+r+duds)
        
                    greens.append(float(w)/instance_size)
                    greys.append (float(g)/instance_size)
                    reds.append(float(r)/instance_size)
                  
            width            = bar_width      
        
            categories       = [np.average(greens), np.average(greys), np.average(reds)]
            yerr             = [np.std(greens), np.std(greys), np.std(reds)]
            colors           = ['forestgreen','grey','red']
            
            
            
            ax.bar(y_pos, categories, width,  color=colors, align='center', edgecolor='none', yerr=yerr, ecolor='black') #ecolor = error bar color
            #bar.set_hatch(pattern[i])
            
            y_pos = [y+width+bar_spacing for y in y_pos]
                #ax.xticks = ['green','grey','red']
            
        pos +=1 
        
        ca               = plt.gca()
        y_pos            = np.arange(3) +(bar_width/2.)*(len(pair)-1) 
        plt.xticks(y_pos, ('$b>0, d=0$', '$b>0, d>0$', '$b=0, d>0$'))
        ca.spines['top'].set_visible(False)
        ca.spines['right'].set_visible(False)
        ca.set_title('\n'.join(title))
        ca.set_xlabel (configs['xlabel'] )
        ca.set_ylabel (configs['ylabel'])
        ca.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
        ca.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks          
        
    if not os.path.isdir(configs['plot_dir']):
        os.makedirs(configs['plot_dir'])
    savename = "-vs-".join(sorted(list(set(savename)),reverse=True)) +'_'   
    sys.stdout.write ('\n'+"\t"*3+configs['plot']+ " >>> saving plot .. "+slash(configs['plot_dir'])+savename+configs['plot']+configs['file_extension']+" .. <<<")
    sys.stdout.flush()
    plt.savefig(slash(configs['plot_dir'])+savename.replace('__','_')+configs['plot']+configs['file_extension'], dpi=configs['dpi'], bbox_inches="tight")      
    sys.stdout.write ('\n'+"\t"*10+configs['plot']+ " >>> plotted: "+savename.replace('__','_')+"_"+configs['plot']+configs['file_extension']+"\n")  
    sys.stdout.flush()
    sys.stdout.write("Success .. returning")
    return       
#--------------------------------------------------------------------------------------
def green_grey_red_pie (PAIRS, configs):

    fig = plt.figure(figsize=configs['fig_size'])
    y = 1.2 # y=1.08 determines space between fig title and subplots
    if len(PAIRS)>2:
        y=1
    fig.suptitle('\n'+configs['fig_suptitle'], fontsize=configs['fig_suptitle_fontsize'], y=y       )  
    savename = []
    pos=1   
    bar_width=0.15
    bar_spacing=0.01
    
    for  pair in PAIRS:  #rows

        axis_limits              = calculate_Axis_limits (pair, configs)
        configs['num_lines']     = axis_limits[-1]
        for tuple in pair: #columns            
                                 
            ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos)
            #----------------------------------------------------------------------------------------
            fig.subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['wspace'], hspace=configs['hspace'] )
            # the values of left, right, bottom and top are to be provided as fractions of the figure width and height. In additions, all values 
            # are measured from the left and bottom edges of the figure. This is why right and top can't be lower than left and right.
            #----------------------------------------------------------------------------------------

            prefix, file_path, title = tuple[0], tuple[1], tuple[2]+", "+pf(configs['num_lines']/5)+" instances]"

            savename.append (prefix[0:6])

            
            sys.stdout.write ("\n"+configs['plot'].ljust(13,' ')+"\t"+title[-1].replace('$','').ljust(65,' ')+"\t"+str(int(float(pos)*100/(len(PAIRS)*len(PAIRS[0]))))+" %")
            sys.stdout.flush()
            #-------------------------------------
            df = open (file_path, 'r').readlines()     
            #-------------------------------------       
            try:
                assert len(df) % 5 == 0 
            except:
                sys.stdout.write ("\n==================================================================================================================")
                sys.stdout.write ("\nWarning, no. lines not multiple of 5: "+str(file_path))
                sys.stdout.write ("\nI will chop off bad trailing lines")       
                sys.stdout.write ("\n==================================================================================================================")
                #----------------------------------------------------------------------------------------
                df = df[0:int(len(df)/5)*5]
                #----------------------------------------------------------------------------------------
                pass
            
            greens, greys, reds, warn,  = [], [], [], True
              
            for i in range(0,configs['num_lines'],5):
                Bs     = [int(s) for s in df[i+1].split() if s!='nil']
                Ds     = [int(s) for s in df[i+2].split() if s!='nil']
                w, g, r, duds, instance_size = 0, 0, 0, 0, 0.0
                assert len(Bs) == len(Ds)
                if len(Bs)>0:
                    for b,d in zip (Bs, Ds):
                        instance_size += 1
                        if (b>0 and d==0):
                            w  += 1
                        elif (b>0 and d>0):
                            g   += 1
                        elif (b==0 and d>0):
                            r  += 1              
                        else:
                            duds+=1
                            if warn:
                                sys.stdout.write ("\n\nWarning: in green_grey_red(): both b and d == 0, if this is a 'scramble' mode data this is ok, otherwise, this is FATAL. I won't warn about this again for this file ...\n\n")
                                warn = False

                    assert instance_size == len(Bs) == len(Ds) == (w+g+r+duds)
        
                    greens.append(float(w)/instance_size)
                    greys.append (float(g)/instance_size)
                    reds.append(float(r)/instance_size)
                  
        
            
            grand_total = float(sum(greens)+sum(greys)+sum(reds))
            
            
            yerr             = [np.std(greens), np.std(greys), np.std(reds)]
            colors           = ['forestgreen','grey','red']       
            patch_labels  = ['$b>0, d=0$', '$b>0, d>0$', '$b=0, d>0$']
            sizes   = [sum(greens)/grand_total, sum(greys)/grand_total, sum(reds)/grand_total]
            colors  = ['#0cc406','#929999','#e72929']
            explode = (0, 0.0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

            # 
            #-------------------------------------------------------------------------------------- 
            # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie
            patches, texts, autotexts = plt.pie(sizes, explode=explode, colors=colors,
                                                autopct='%1.1f%%', shadow=False, startangle=90, frame=False,
                                                wedgeprops = { 'linewidth': 0 },
                                                textprops={'color':'white', 'fontsize':8,'weight':'bold'} )
            for T in  autotexts:
                T.set_text (str(T.get_text())+'\n\u00B1'+str(round(yerr[0],2))+'%')
            
            ax.legend(patches, patch_labels, loc=(.8,.8), frameon=False, fontsize=8)    
            #--------------------------------------------------------------------------------------        
            ax.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
            plt.tight_layout()
            

            ax.set_xticks([])

            #ax.set_xticklabels([title])
            ax.set_xlabel (title)

            
            
            pos +=1 
        
       
    if not os.path.isdir(configs['plot_dir']):
        os.makedirs(configs['plot_dir'])
    savename = "-vs-".join(sorted(list(set(savename)),reverse=True)) +'_'   
    sys.stdout.write ('\n'+"\t"*3+configs['plot']+ " >>> saving plot .. "+slash(configs['plot_dir'])+savename+configs['plot']+configs['file_extension']+" .. <<<")
    sys.stdout.flush()
    plt.savefig(slash(configs['plot_dir'])+savename.replace('__','_')+configs['plot']+configs['file_extension'], dpi=configs['dpi'], bbox_inches="tight")      
    sys.stdout.write ('\n'+"\t"*10+configs['plot']+ " >>> plotted: "+savename.replace('__','_')+"_"+configs['plot']+configs['file_extension']+"\n")  
    sys.stdout.flush()
    sys.stdout.write("Success .. returning")
    return       
#--------------------------------------------------------------------------------------  
def pearsonr_BD (df, ax, configs): 
    r, pvalue = [], []
    for i in range(0,configs['num_lines'],5):
        Bs    = [int(b) for b in df[i+1].split() if b!='nil']
        Ds    = [int(d) for d in df[i+2].split() if d!='nil']
        assert len(Bs) == len(Ds)
        if len(Bs)>0:
            pearsonr = scipy_stats.pearsonr(Bs,Ds)
            r      = r      + [pearsonr[0]]
            pvalue = pvalue + [pearsonr[1]]
                    
    relfreq = scipy_stats.relfreq(r, numbins=10)        
    #Calculate space of values for x
    x = relfreq.lowerlimit + np.linspace(0, relfreq.binsize*relfreq.frequency.size, relfreq.frequency.size)          
    #ax.set_xlim([x.min(), x.max()])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.bar(x, relfreq.frequency, width=relfreq.binsize, color='dodgerblue', edgecolor='none')
           
    return ax, ', $avg \quad p-value='+ str((np.average(pvalue)))+'$' 
#--------------------------------------------------------------------------------------  
def percentiles (df, ax, configs):
    perc_tuple = []
    for i in range(0,len(df),5):
        Bs     = [int(b) for b in df[i+1].split() if b!='nil']
        Ds     = [int(d) for d in df[i+2].split() if d!='nil']
        Xs     = [int(x) for x in df[i+3].split() if x!='nil']
        assert len(Bs) == len(Ds) == len(Xs) 
        
        
        if len(Bs)>0:
            Bs_in = sorted ([b for b in [b*x for b,x in zip(Bs, Xs)] if b !=0], reverse=True)
            knapsack_value  = sum (Bs_in)
            #Ds_in = sorted ([d for d in [d*x for d,x in zip(Ds, Xs)] if d !=0], reverse=True)
            #knapsack_weight = sum (Ds_in)
            NUM_GENES = len(Bs_in)
            i=0           
            sum_so_far = 0
            
            perc_25 =0 
            while  sum_so_far < 0.25*float(knapsack_value):
                sum_so_far += Bs_in[i]
                perc_25 +=1
                i+=1
            
            perc_50 = perc_25         
            while  sum_so_far < 0.50*float(knapsack_value):
                sum_so_far += Bs_in[i]
                perc_50 +=1
                i+=1
            
            perc_75 = perc_50           
            while  sum_so_far < 0.75*float(knapsack_value):
                sum_so_far += Bs_in[i]
                perc_75 +=1
                i+=1
            
            perc_90 = perc_75          
            while  sum_so_far < 0.90*float(knapsack_value):
                sum_so_far += Bs_in[i]
                perc_90 +=1
                i+=1
            
            perc_tuple.append((perc_25, perc_50, perc_75, perc_90, NUM_GENES))   

        
    AVG_25  = np.average([p[0] for p in perc_tuple])
    AVG_50  = np.average([p[1] for p in perc_tuple])
    AVG_75  = np.average([p[2] for p in perc_tuple])
    AVG_90  = np.average([p[3] for p in perc_tuple])
    AVG_100 = np.average([p[4] for p in perc_tuple])
    STD_25  = np.std    ([p[0] for p in perc_tuple])
    STD_50  = np.std    ([p[1] for p in perc_tuple])
    STD_75  = np.std    ([p[2] for p in perc_tuple])
    STD_90  = np.std    ([p[3] for p in perc_tuple])    
    STD_100 = np.std    ([p[4] for p in perc_tuple])
                  
    width            = 0.15       # the width of the bars
    y_pos            = np.arange(5)
    heights          = [AVG_25, AVG_50, AVG_75, AVG_90, AVG_100]
    yerr             = [STD_25, STD_50, STD_75, STD_90, STD_100]
    colors           = ['green','green','green', 'green', 'grey']
    
    ax.bar(y_pos, heights, width,  color=colors, align='center', yerr=yerr, edgecolor='none')
    ax.xticks = ['25%','50%','75%','90%','100%']
    plt.xticks(y_pos + width/2., ('25%','50%','75%','90%','100%'))
        
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
       
    return ax 
#-------------------------------------------------------------------------------------- 
def PLOTTER (PAIRS, configs): 
    fig = plt.figure(figsize=configs['fig_size'])
    y = 1.2 # y=1.08 determines space between fig title and subplots
    if len(PAIRS)>2:
        y=1
    fig.suptitle('\n'+configs['fig_suptitle'], fontsize=configs['fig_suptitle_fontsize'], y=y       )  
    savename = []
    pos=1
    
    for  pair in PAIRS:
        
        #------------------------------------
        axis_limits              = calculate_Axis_limits (pair, configs)
        configs['num_lines']     = axis_limits[-1]
        #------------------------------------
        for tuple in pair:
            prefix, file_path, title = tuple[0], tuple[1], tuple[2]
            #print ('\nprefix\t'+prefix+'\nfile_path\t'+file_path+'\ntitle\t'+title+'\n')
            savename.append (prefix[0:6])
            ax = None
            if configs['projection'] != None:
                ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos, projection=configs['projection'])
            else:
                
                ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos)
            #----------------------------------------------------------------------------------------
            fig.subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['wspace'], hspace=configs['hspace'] )
            # the values of left, right, bottom and top are to be provided as fractions of the figure width and height. In additions, all values 
            # are measured from the left and bottom edges of the figure. This is why right and top can't be lower than left and right.
            #----------------------------------------------------------------------------------------
            ax.grid(True)
            title = title+", "+pf(configs['num_lines']/5)+" instances]"
            ax.set_title(title)
            sys.stdout.write ("\n"+configs['plot'].ljust(13,' ')+"\t"+title.replace('$','').ljust(65,' ')+"\t"+str(int(float(pos)*100/(len(PAIRS)*len(PAIRS[0]))))+" %")
            sys.stdout.flush()
            df = open (file_path, 'r').readlines()            
            try:
                assert len(df) % 5 == 0 
            except:
                sys.stdout.write ("\n==================================================================================================================")
                sys.stdout.write ("\nWarning, no. lines not multiple of 5: "+str(file_path))
                sys.stdout.write ("\nI will chop off bad trailing lines")       
                sys.stdout.write ("\n==================================================================================================================")
                #----------------------------------------------------------------------------------------
                df = df[0:int(len(df)/5)*5]
                #----------------------------------------------------------------------------------------
                pass
            
            x_suff=""
            if configs['plot'] == "scatter_BD":
                ax.set_xlim([-1,axis_limits[0]])
                ax.set_ylim([-1,axis_limits[1]])
                sc = scatter_BD(df, fig, ax, configs)
                
            elif configs['plot']=='polar':
                sc = polar(df, ax, configs)   
                
            else:# configs['plot']=='pearsonr_BD':
                sc, x_suff = pearsonr_BD (df, ax, configs)                            

            
            ax.set_xlabel (configs['xlabel']+x_suff )
            ax.set_ylabel (configs['ylabel'])
            ax.tick_params(axis='x', which='both', left='off', right='off', bottom='on', top='off',  labelbottom='on', labeltop='off') # both major and minor ticks
            ax.tick_params(axis='y', which='both', bottom='off', top='off', left='on', right='off',  labelleft='on', labelright='off') # both major and minor ticks          
            
            pos +=1  
    
    if not os.path.isdir(configs['plot_dir']):
        os.makedirs(configs['plot_dir'])
    savename = "-vs-".join(sorted(list(set(savename)),reverse=True)) +'_'   
    sys.stdout.write ('\n'+"\t"*3+configs['plot']+ " >>> saving plot .. "+slash(configs['plot_dir'])+savename+configs['plot']+configs['file_extension']+" .. <<<")
    sys.stdout.flush()
    plt.savefig(slash(configs['plot_dir'])+savename.replace('__','_')+configs['plot']+configs['file_extension'], dpi=configs['dpi'], bbox_inches="tight")      
    sys.stdout.write ('\n'+"\t"*10+configs['plot']+ " >>> plotted: "+savename.replace('__','_')+"_"+configs['plot']+configs['file_extension']+"\n")  
    sys.stdout.flush()
    sys.stdout.write("Success .. returning")
    return              
#--------------------------------------------------------------------------------------  
def PLOTTER_combined (PAIRS, configs): 
    '''     
        if configs['plot'] == "coresize":
            ax.set_ylim([0,1])
            sc, savename = coresize (df, ax, configs)  
                        
        else:
            ax.set_ylim([0,axis_limits[0]])
            sc, savename = percentiles (df, ax, configs)          
    ''' 
#--------------------------------------------------------------------------------------

if __name__ == "__main__": 
    args = getCommandLineArg()
    input_file, stamp = args[0], args[1]
    plots_root_dir  = os.getenv('post')
    if plots_root_dir == None or plots_root_dir == '':
        plots_root_dir = slash(os.getcwd())+ 'output/plots_'+str(socket.gethostname())+'_'+ time.strftime("%B-%d-%Y")
    else:
        plots_root_dir = slash(plots_root_dir)+'RAW/output/plots_'+str(socket.gethostname())+'_'+ time.strftime("%B-%d-%Y")
    if not os.path.isdir(plots_root_dir):
        try:
            os.makedirs(plots_root_dir)
        except:
            pass
    datapoints_files = open (input_file).readlines()
    
    #-------------------------------------------------------------
    columns = 2 # aka no. of files per pair
    PAIRS = getPairs (datapoints_files, columns)
    rows = len(PAIRS)
    #-------------------------------------------------------------
     
    
    
    #-------------------------------------------------------------
    # assuming the input_file is of the form /path/INPUT_BOTH_p0.1
    input_file = input_file.split('/')[-1]
    stamp = "_"+".".join((input_file.split('.')[:-1]))+'_'+stamp
    file_extension = ".svg"  
    figure_size = (5*columns, 3*(max(rows,2))) #(width, height)
    dpi = 500
    #--------------------------------------------------------------
    
    #wspace = horizental space between subplots
    #hspace = vertical 
    configs_polar = {
                'fig_size':              figure_size,
                'fig_suptitle':          "Benefit vs Damage plot", 
                'fig_suptitle_fontsize': 18,             
                'plot':                  "polar",
                'xlabel':                "Damage", 
                'ylabel':                "Benefit",
                'cbar_label':            "$Frequency \quad (log_2)$",
                'cmap':                  plt.cm.get_cmap('plasma'),
                'marker':                mpl.markers.MarkerStyle(marker='+', fillstyle=None),
                'alpha':                 1,
                'cbar_labelsize':        5,
                'wspace':                0.4,
                'hspace':                0.4,
                'file_extension':        '_'+stamp+file_extension,
                'projection':            'polar',
                'dpi':                   dpi,
                'plot_dir':              plots_root_dir+'/polar/'
    }   
    configs_scatter_BD = {
                'fig_size':              figure_size,
                'fig_suptitle':          "Benefit vs Damage plot", 
                'fig_suptitle_fontsize': 18,             
                'plot':                  "scatter_BD",
                'xlabel':                "Damage", 
                'ylabel':                "Benefit",
                'cbar_label':            "$Frequency \quad (log_2)$",
                'cmap':                  plt.cm.get_cmap('plasma'),
                'marker':                mpl.markers.MarkerStyle(marker='+', fillstyle=None),
                'alpha':                 1,
                'cbar_labelsize':        5,
                'wspace':                0.2,
                'hspace':                0.4,
                'file_extension':        '_'+stamp+file_extension,
                'projection':            None,
                'dpi':                   dpi,
                'plot_dir':              plots_root_dir+'/scatter/'
    }   
    configs_coresize = {
                'fig_size':              figure_size,
                'fig_suptitle':          "Instance coresize (Psinger minknap algorithm)", 
                'fig_suptitle_fontsize': 18,   
                'plot':                  "coresize",
                'xlabel':                "core size", 
                'ylabel':                "fraction",
                'cbar_label':            None,
                'cbar_labelsize':        None,
                'cmap':                  plt.cm.get_cmap('plasma'),
                'marker':                None,
                'alpha':                 1,
                'cbar_labelsize':        None,
                'wspace':                0.3,
                'hspace':                0.4,
                'file_extension':        '_'+stamp+file_extension,
                'projection':            None,
                'dpi':                   dpi,
                'plot_dir':              plots_root_dir+'/coresize/'
    }
    configs_green_grey_red_pie = {
                'fig_size':              figure_size,
                'fig_suptitle':          "Green, Grey, and Red Genes", 
                'fig_suptitle_fontsize': 18,   
                'plot':                  "green_grey_red",
                'xlabel':                "Gene B/D class", 
                'ylabel':                "fraction",
                'cbar_label':            None,
                'cbar_labelsize':        None,
                'cmap':                  plt.cm.get_cmap('plasma'),
                'marker':                None,
                'alpha':                 1,
                'cbar_labelsize':        None,
                'wspace':                0.4,
                'hspace':                0.4,
                'file_extension':        '_'+stamp+file_extension,
                'projection':            None,
                'dpi':                   dpi,
                'plot_dir':              plots_root_dir+'/green_grey_red/'
    }
    configs_pearsonr_BD = {
                'fig_size':              figure_size,
                'fig_suptitle':          "Pearson $r$ correlation coeff. ", 
                'fig_suptitle_fontsize': 18,   
                'plot':                  "pearsonr_BD",
                'xlabel':                "pearson $r$", 
                'ylabel':                "fraction",
                'cbar_label':            None,
                'cbar_labelsize':        None,
                'cmap':                  plt.cm.get_cmap('plasma'),
                'marker':                None,
                'alpha':                 1,
                'cbar_labelsize':        None,
                'wspace':                0.3,
                'hspace':                0.4,
                'file_extension':        '_'+stamp+file_extension,
                'projection':            None,
                'dpi':                   dpi,
                'plot_dir':              plots_root_dir+'/pearsonr/'
    }
    configs_percentile = {
                'fig_size':              figure_size,
                'fig_suptitle':          "How many genes does it take to fill x % of the knapsack", 
                'fig_suptitle_fontsize': 18,   
                'plot':                  "percentile",
                'xlabel':                "% of Knapsack total value", 
                'ylabel':                "number of genes to achieve that %",
                'cbar_label':            None,
                'cbar_labelsize':        None,
                'cmap':                  plt.cm.get_cmap('plasma'),
                'marker':                None,
                'alpha':                 1,
                'cbar_labelsize':        None,
                'wspace':                0.4,
                'hspace':                0.4,
                'file_extension':        '_'+stamp+file_extension,
                'projection':            None,
                'dpi':                   dpi,
                'plot_dir':              plots_root_dir+'/percentile/'
    }

    green_grey_red_pie(PAIRS, configs_green_grey_red_pie)
    #a   = Process(target=PLOTTER, args=(PAIRS, configs_polar,))   
    #b   = Process(target=PLOTTER, args=(PAIRS, configs_scatter_BD,))
    #c   = Process(target=PLOTTER, args=(PAIRS, configs_coresize,))
    #d   = Process(target=green_grey_red, args=(PAIRS, configs_green_grey_red,))
    #e   = Process(target=PLOTTER, args=(PAIRS, configs_pearsonr_BD,))
    #f   = Process(target=PLOTTER, args=(PAIRS, configs_percentile,))
    
    #Remember also that non-daemonic processes will be automatically be joined.
    #a.daemon = True
    
    #a.start()
    #time.sleep(1)
    
    #result_b = b.start()
    #time.sleep(1)
    #result_c = c.start()
    #=time.sleep(1)
    #result_d = d.start()
    #time.sleep(1)
    #result_e = e.start()
    #time.sleep(1)
    #result_f = f.start()
    #time.sleep(1)
    
    #Remember also that non-daemonic processes will be automatically be joined.
    #a.join()
    #b.join()
    #c.join()
    #d.join()
    #e.join()
    #f.join()
    '''
    sys.stdout.write ("\nscatter_BD: "+str(result_b))
    sys.stdout.write ("\ncoresize: "+str(result_c))
    sys.stdout.write ("\ngreen_grey_red: "+str(result_d))
    #sys.stdout.write ("\npearsonr_BD: "+str(result_e))
    sys.stdout.write ("\nPercentile: "+str(result_f))
    
    sys.stdout.flush()'''
    #sys.exit(0)
    
    
    
    
    
