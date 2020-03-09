from scipy import stats as scipy_stats
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm 
import matplotlib.colors as mcolors
import os,sys, socket, math, time, numpy as np
from multiprocessing import Process
from matplotlib import rcParams

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

        tmp        = [e[0].split('/')[-1].split(e[1]) for e in DATA_FILES]
        net_name   = [n[0] for n in tmp]
        suffix     = [n[1].split('_') for n in tmp] 
        titles     = [n+"\n[$"+s[0].replace('p','p=')+", "+s[1].replace('t','t=')+"$, "+s[2]+", "+s[3]+", "+s[4]+", "+s[5]+", "+s[6]  for n,s in zip(net_name, suffix)] # title will be later appended with num_instances +']' in PLOTTER
        SUBPLOTS.append ([e for e   in   zip(net_name, data_files, titles)])      
    return SUBPLOTS
#--------------------------------------------------------------------------------------
def max_lines (pair, configs):
    assert configs['plot']=='green_grey_red'
    num_lines=[]
    for prefix, file_path, title in pair:
        num_lines.append(0)
        df = open (file_path, 'r')
        while True:
            try: # insist on reading chunks of 5 lines 
                next(df)                
                next(df)
                next(df)
                next(df) 
                next(df) 
            except:
                break
            num_lines[-1] += 5       
    if len(num_lines)==0:
        num_lines=[0]
    return min(num_lines)
#--------------------------------------------------------------------------------------
def assign_colors(slices):
    start       = 0
    skip        = 0
    distinction = 13 # the higher the more distinct the colors will be            
    colors  = [         iter(cm.GnBu     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.YlOrBr   (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.YlGn     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Spectral (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Blues    (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Dark2    (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Paired   (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.Set1     (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.jet      (np.linspace(0,1,  (distinction*(skip+1))+start))),\
                        iter(cm.cool     (np.linspace(0,1,  (distinction*(skip+1))+start))),    
                ] #http://matplotlib.org/users/colormaps.html    
    c = colors[-3]
    for i in range(start):
        next(c)
        
    for key in sorted(slices.keys(), reverse=True):
        if slices[key]['color'] == None:
            for i in range(skip):
                next(c)
            slices[key]['color'] = next(c)
    return slices
#--------------------------------------------------------------------------------------
def assign_range(slices, b, d):
    b2d_ratio, d2b_ratio = 0, 0 
    the_right_key=None                 
    if b>0 or d>0:
        b2d_ratio, d2b_ratio = (float(b)/float(b+d))*100,  (float(d)/float(b+d))*100
        the_right_key_for_b = [key for key in sorted(slices.keys()) if b2d_ratio >= slices[key]['range'][0]]
        the_right_key_for_d = [key for key in sorted(slices.keys()) if d2b_ratio <= slices[key]['range'][1]]
        the_right_key = [key for key in the_right_key_for_b if key in the_right_key_for_d][0]
       
    else:
        the_right_key =  [key for key in slices.keys() if slices[key]['range'][0]==0 and  slices[key]['range'][1]==0     ][0]
        
    slices[the_right_key]['count'] += 1

    return slices
#--------------------------------------------------------------------------------------
def plot_next_pie(slices,ax, title):
    normalizer = 0 
    patch_labels = []
    for key in sorted(slices.keys()):
        slices[key]['avg'] = np.average (slices[key]['fractions'])
        slices[key]['std'] = np.std     (slices[key]['fractions'])
        normalizer          += slices[key]['avg']
        patch_labels.append(str(slices[key]['range']))
    
    #print ("\n\nnormalizer: "+str(normalizer))
    #patch_labels  = ['$b>0, d=0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b>0, d>0$', '$b=0, d>0$']
    
    sorted_keys = sorted(slices.keys())
    sizes         = [slices[key]['avg']/normalizer for key in sorted_keys]
    colors        = [slices[key]['color']          for key in sorted_keys]
    explode       = [0]*len(sorted_keys)  # only "explode" the 2nd slice (i.e. 'Hogs')

    #-------------------------------------------------------------------------------------- 
    # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie
    patches, texts, autotexts = plt.pie (sizes, explode=explode, colors=colors,
                                         autopct='%1.1f%%', shadow=False, startangle=0, frame=False,
                                         wedgeprops = { 'linewidth': 0 },
                                         textprops={'color':'black', 'fontsize':8,'weight':'bold'} )
            
    centre_circle = plt.Circle((0,0),0.3,color=None, fc='white',linewidth=0)    
    plt.gca().add_artist(centre_circle)    
    
    i=0
    updated_patch_labes=[]
    for p,t in zip(patch_labels,autotexts):
        updated_patch_labes.append( p.ljust(8,' ') + '('+t.get_text().ljust(8,' ')+'\u00B1'+str(round(slices[sorted_keys[i]]['std'],2))+')')
        i+=1
    for T in  autotexts:
        #T.set_text (str(T.get_text())+'\n\u00B1'+str(round(slices[sorted_keys[i]]['std'],2))+'%')
        T.set_text('')
    
    ax.legend(patches, updated_patch_labes, loc=(.9,.25), frameon=False, fontsize=8)    
    #--------------------------------------------------------------------------------------        
    ax.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.tight_layout()
    ax.set_xticks([])
    #ax.set_xticklabels([title])
    ax.set_xlabel (title) 
    #ax.text(.1, .5, "setosa", size=16, color='red')
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
        configs['num_lines']   = max_lines (pair, configs)
        axis_limits            = 1

        if configs['projection'] != None:
            ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos, projection=configs['projection'])
        else:                
            ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos)
        #----------------------------------------------------------------------------------------
        fig.subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['wspace'], hspace=configs['hspace'] )
        # the values of left, right, bottom and top are to be provided as fractions of the figure width and height. In additions, all values 
        # are measured from the left and bottom edges of the figure. This is why right and top can't be lower than left and right.
        #----------------------------------------------------------------------------------------
        ax.set_ylim([0,axis_limits])        
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
    
    for  pair in PAIRS:  #rows

        configs['num_lines']              = max_lines (pair, configs)

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
            
            greens, greys, reds, duds, warn,  = [], [], [], [], True              
            for i in range(0,configs['num_lines'],5):
                Bs     = [int(s) for s in df[i+1].split() if s!='nil']
                Ds     = [int(s) for s in df[i+2].split() if s!='nil']
                w, g, r, dd, instance_size = 0, 0, 0, 0, 0.0
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
                            dd+=1
                            if warn:
                                sys.stdout.write ("\n\nWarning: in green_grey_red(): both b and d == 0, if this is a 'scramble' mode data this is ok, otherwise, this is FATAL. I won't warn about this again for this file ...\n\n")
                                warn = False

                    print("\ninstance_size "+str(instance_size)+" duds "+str(dd))
                    assert instance_size == len(Bs) == len(Ds) == (w+g+r+dd)
                    divider = instance_size-dd
                    greens.append(float(w)/divider)
                    greys.append (float(g)/divider)
                    reds.append(float(r)/divider)
                    
                  
        
            
            grand_total = float(sum(greens)+sum(greys)+sum(reds))
            
            
            yerr             = [np.std(greens), np.std(greys), np.std(reds), np.std(duds)]
            
            patch_labels  = ['$b>0, d=0$', '$b>0, d>0$', '$b=0, d>0$']
            sizes   = [sum(greens)/grand_total, sum(greys)/grand_total, sum(reds)/grand_total]
            colors  = ['#0cc406','#929999', '#e72929']
            #colors   = ['#008837','#2c7bb6','#d7191c']
            #colors   = ['#3182bd','#9ecae1','#deebf7']
            #colors   = ['#2c7fb8','#7fcdbb','#edf8b1']
            #colors = ['#31a354','#addd8e','#f7fcb9']
            #colors   = ['#31a354','#addd8e','#f7fcb9']
            explode = (0.0,0.0,0.0)  # only "explode" the 2nd slice (i.e. 'Hogs')

            # 100:0, 90:10, 75:25, 50:50, 25:75, 10:90, 0:100 
            #-------------------------------------------------------------------------------------- 
            # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie
            patches, texts, autotexts = plt.pie(sizes, explode=explode, colors=colors,
                                                autopct='%1.1f%%', shadow=False, startangle=90, frame=False,
                                                wedgeprops = { 'linewidth': 0 },
                                                textprops={'color':'black', 'fontsize':8,'weight':'bold'} )
            centre_circle = plt.Circle((0,0),0.3,color=None, fc='white',linewidth=0)            
            plt.gca().add_artist(centre_circle)                                     
            
            
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
def green_grey_red_pie_detailed (PAIRS, configs):
    slices      = configs['slices']
    fig = plt.figure(figsize=configs['fig_size'])
    y = 1.2 
    if len(PAIRS)>2:
        y=1
    fig.suptitle('\n'+configs['fig_suptitle'], fontsize=configs['fig_suptitle_fontsize'], y=y       )  
    savename = []
    pos=1   

    for  pair in PAIRS:  #rows

        configs['num_lines']   = max_lines (pair, configs)

        for tuple in pair: #columns            
                
            ax = fig.add_subplot(len(PAIRS), len(PAIRS[0]), pos)
            #----------------------------------------------------------------------------------------
            fig.subplots_adjust(left=0.1 , bottom=0.1, right=.9, top=.9, wspace=configs['wspace'], hspace=configs['hspace'] )
            # the values of left, right, bottom and top are to be provided as fractions of the figure width and height. In additions, all values 
            # are measured from the left and bottom edges of the figure. This is why right and top can't be lower than left and right.
            #----------------------------------------------------------------------------------------
            prefix, file_path, title = tuple[0], tuple[1], tuple[2]+", "+pf(configs['num_lines']/5)+" instances]"
            savename.append (prefix[0:6])       
            sys.stdout.write (configs['plot'].strip().ljust(13,' ')+"\t"+title.strip().replace('$','').ljust(65,' ')+"\t"+str(int(float(pos)*100/(len(PAIRS)*len(PAIRS[0]))))+" %")
            sys.stdout.flush()
            #------------------------------------
            slices = assign_colors(slices)            
            #-------------------------------------
            df = open (file_path, 'r')
            #-------------------------------------               
            
            #multiprocessing.cpu_count()
            
            lines_so_far, warn = 0, True
            
            while lines_so_far < configs['num_lines']:                
                next(df)                                     # skip over objects
                Bs     = [int(s) for s in next(df).split()]
                Ds     = [int(s) for s in next(df).split()]
                next(df)                                     #skip over Xs (solution vector)
                next(df)                                     #skip over coresize/exec_time
                lines_so_far += 5         
                assert len(Bs) == len(Ds)
                
                instance_size = 0
                for key in slices:
                    slices[key]['count']=0
                if len(Bs)>0:
                    for b,d in zip (Bs, Ds):
                        instance_size += 1
                        #-------------------------------------
                        slices = assign_range(slices, b, d)
                        #-------------------------------------
                    counted=0
                for key in slices.keys():
                    slices[key]['fractions'].append(float(slices[key]['count'])/instance_size)
                    counted += slices[key]['count']
                    
                assert instance_size == len(Bs) == len(Ds)  == counted      
            
            plot_next_pie (slices, ax, title)
                                
            pos +=1 
       
    if not os.path.isdir(configs['plot_dir']):
        os.makedirs(configs['plot_dir'])
    savename = "-vs-".join(sorted(list(set(savename)),reverse=True)) +'_'   
    sys.stdout.write ('\n'+"\t"*3+configs['plot']+ " >>> saving plot .. "+slash(configs['plot_dir'])+savename+configs['plot']+configs['file_extension']+" .. <<<")
    sys.stdout.flush()
    plt.savefig(slash(configs['plot_dir'])+savename.replace('__','_')+configs['plot']+configs['file_extension'], dpi=configs['dpi'], bbox_inches="tight")      
    sys.stdout.write ('\n'+"\t"*10+configs['plot']+ " >>> plotted: "+savename.replace('__','_')+"_"+configs['plot']+configs['file_extension']+"\n")  
    sys.stdout.flush()
    sys.stdout.write("\nSuccess .. returning\n\n")
    
    return       
#--------------------------------------------------------------------------------------
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

    slices = {
                               1  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},
                               2  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(90,10)},
                               3  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'80:20', 'range':(80,20)},
                               4  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'70:30', 'range':(70,30)},
                               5  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'60:40', 'range':(60,40)},
                               6  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'50:50', 'range':(50,50)},
                               7  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'40:60', 'range':(40,60)},
                               8  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'30:70', 'range':(30,70)},
                               9  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'20:80', 'range':(20,80)},
                               10 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(10,90)},
                               11 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},
                               
                               12 :{'fractions':[], 'count':0, 'color':'black', 'avg':0, 'std':0, 'label':'0:0', 'range':(0,0)},
                }
    slices_short = { 
                               1  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'100:0', 'range':(100,0)},                               
                               2  :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'90:10', 'range':(75,25)},
                               3 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'10:90', 'range':(50,50)},
                               4 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(25,75)},
                               5 :{'fractions':[], 'count':0, 'color':None, 'avg':0, 'std':0, 'label':'0:100', 'range':(0,100)},
                               
                               6 :{'fractions':[], 'count':0, 'color':'black', 'avg':0, 'std':0, 'label':'0:0', 'range':(0,0)},
                }
    configs_green_grey_red_pie = {
                'fig_size':              figure_size,
                'fig_suptitle':          "The Good, The Bad, and The Ugly", 
                'fig_suptitle_fontsize': 18,   
                'plot':                  "green_grey_red",
                'xlabel':                "B:D distribution", 
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
                'plot_dir':              plots_root_dir+'/green_grey_red/',
                'slices':                slices_short
    }
    
    #-----------------------------------------------------------------
    green_grey_red_pie_detailed([PAIRS[0]], configs_green_grey_red_pie)
    #-----------------------------------------------------------------





