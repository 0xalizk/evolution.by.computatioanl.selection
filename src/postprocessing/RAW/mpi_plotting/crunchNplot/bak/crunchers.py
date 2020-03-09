import sys,os,copy,math,numpy as np
from collections import Counter
sys.path.insert(0, os.getenv('lib'))
import time, util_plotting as util, master_cruncher as master
#######################################################################################
mywrite = util.mywrite
#######################################################################################
def ReAvg (previous_avg, previous_count, new_value):
    new_count = previous_count+1
    new_avg   = ((previous_avg*previous_count) + new_value)/float(new_count)
    return new_avg, new_count
#######################################################################################
def rescale(R, a,b):
    scaled = []
    minv = min(R)
    maxv = max(R)
    numerator = maxv-minv
    for r in R:
        scaled.append((((b-a)*(r-minv))/numerator) + a)
    return scaled
#######################################################################################    
def instanceBYdegree(Gs,Bs,Ds,Xs):
    ByDeg, BIN, DIN, BOU, DOU = {}, 0.0, 0.0, 0.0, 0.0
    for g,b,d,x in [(g,b,d,x) for g,b,d,x in zip(Gs,Bs,Ds,Xs)]:
        deg = sum([int(d) for d in g.split('$')[1:]])
        if x==1:
            BIN += b
            DIN += d
            if deg not in ByDeg.keys():
                ByDeg[deg] = {'bin':[],'din':[],'bou':[],'dou':[]}
            ByDeg[deg]['bin'].append(b)
            ByDeg[deg]['din'].append(d)
        elif x==0:
            BOU += b
            DOU += d
            if deg not in ByDeg.keys():
                ByDeg[deg] = {'bin':[],'din':[],'bou':[],'dou':[]}
            ByDeg[deg]['bou'].append(b)
            ByDeg[deg]['dou'].append(d)
        else:
            print("FATAL: bad solution vector\nExiting ..\n")
            sys.exit(1) 
    return ByDeg, BIN, DIN, BOU, DOU
#######################################################################################    
def updateSTATS(stats,STATS, metrics):
    for deg in stats.keys():
        if deg not in STATS.keys():
            STATS[deg]={}
            for m in metrics:
                STATS[deg][m]={'CsF':0.0,'AsF':0.0}
        for m in metrics:
            if stats[deg][m]>0: ###### ? ########
                STATS[deg][m]['AsF'], STATS[deg][m]['CsF'] = ReAvg (STATS[deg][m]['AsF'], STATS[deg][m]['CsF'], stats[deg][m])
#######################################################################################
def normalizeSTATS(STATS, metrics):
    for m in metrics:
        AVG = float(sum([STATS[deg][m]['AsF'] for deg in STATS.keys()]))
        CNT = float(sum([STATS[deg][m]['CsF'] for deg in STATS.keys()]))
        for deg in STATS.keys():
            STATS[deg][m]['AsF'] = (STATS[deg][m]['AsF']/AVG)*100
            STATS[deg][m]['CsF'] = (STATS[deg][m]['CsF']/CNT)*100
#######################################################################################  
def cruncher1 (Gs,Bs,Ds,Xs,slices): # relative COUNT of genes in each slice regardless if gene is IN or OUT knapsack
    for key in slices['segments'].keys():
        slices['segments'][key]['count']=0
    instance_size = 0
    for b,d in zip (Bs, Ds):
        instance_size += 1
        the_right_key = master.assign_range(slices, b, d)
        slices['segments'][the_right_key]['count'] += 1   # <<<<<<<<<<<<<<<
    counted=0
    for key in slices['segments'].keys():
        slices['segments'][key]['fractions'].append(float(slices['segments'][key]['count'])/instance_size)  # <<<<<<<<<<<<<<< #
        counted += slices['segments'][key]['count']
    assert instance_size == len(Bs) == len(Ds)  == counted
#######################################################################################
def cruncher2 (Gs,Bs,Ds,Xs,slices): # relative tot. benefit of genes in each slice regardless if gene is IN or OUT knapsack (obviously genes with b=0 are OUT)
    for key in slices['segments'].keys():
        slices['segments'][key]['count']=0
    instance_size = 0
    for b,d in zip (Bs, Ds):
        instance_size += 1
        the_right_key = master.assign_range(slices, b, d)
        slices['segments'][the_right_key]['count'] += b  
    for key in slices['segments'].keys():
        slices['segments'][key]['fractions'].append(float(slices['segments'][key]['count'])/sum(Bs))  
#######################################################################################
def cruncher3 (Gs,Bs,Ds,Xs,slices): # only genes IN knapsack 
    for key in slices['segments'].keys():
        slices['segments'][key]['count']=0
    instance_size = 0
    for b,d,x in zip (Bs, Ds, Xs):
        if x==1:                                           # <<<<<<<<<<<<<<<
            instance_size += 1        
            the_right_key = master.assign_range(slices, b, d)
            slices['segments'][the_right_key]['count'] += b # <<<<<<<<<<<<<<<
    for key in slices['segments'].keys():
        slices['segments'][key]['fractions'].append(float(slices['segments'][key]['count'])/sum(Bs)) 
#######################################################################################
def cruncher4 (Gs,Bs,Ds,Xs,slices): # stacked bar2d of relative COUNT of genes in each slice regardless if gene is IN or OUT knapsack
    instance_size = len(Gs)
    tmp_count     = {}
    for slice_id in slices['segments'].keys():
        tmp_count[slice_id]=[]
    
    for g,b,d in zip (Gs, Bs, Ds):
        the_right_slice_id = master.assign_range(slices, b, d)
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
#######################################################################################
def wheel_processor   (configs, pair, rank):
    log, num_lines = configs['worker_log'], 0
    if sum(plot['processing_bit'] for plot in pair) >= 1:
        num_lines = master.max_lines(pair, configs)
    for plot in pair: 
        if plot['processing_bit'] == 1:     
            cruncher = None
            if 'cruncher' in configs.keys():
                if configs['cruncher'] in globals().keys():
                    cruncher = globals()[configs['cruncher']]
                else:
                    cruncher = cruncher1 # default    
            else:
                cruncher = cruncher1 # default
            mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": applying "+cruncher.__name__+" on "+plot['file_path'].split('/')[-1])

            plot['title'] = plot['title']+", "+util.pf(float(num_lines)/5.0)+" instances]"
            file_no, coords, pos, prefix, file_path, title, processing_bit = plot['file_no'], ['coords'], plot['pos'], plot['prefix'], plot['file_path'], plot['title'], plot['processing_bit']

            assert processing_bit == 1
            slices      = copy.deepcopy(configs['slices']) 
            for key in slices['segments'].keys(): #assert slices 
                if cruncher==cruncher4:
                    assert slices['segments'][key]['degree_freq'] == {}
                else:
                    assert slices['segments'][key]['count']     == 0
                    assert slices['segments'][key]['fractions'] == []
            #-------------------------------------
            df = open (plot['file_path'], 'r')
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
                    cruncher(Gs,Bs,Ds,Xs,slices)    
            plot['data'], plot['worker_configs'], plot['rank'] = slices, configs, rank
            ##########################
            master.dump(plot)
            ##########################
        else:
            mywrite(log,"\n\t\t\t\tworker #"+str(rank)+": skipping: "+plot['file_path'].split('/')[-1])              
#######################################################################################        
def scatter_processor (configs, pair, rank):
    log, xlim, ylim, num_lines = configs['worker_log'], 0, 0, 0
    if sum([plot['processing_bit'] for plot in pair]) >= 1:
        xlim, ylim, num_lines = master.calculate_Axis_limits (pair, configs)
    
    for plot in pair: 
        if plot['processing_bit'] == 1:  
            mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": applying scatter on "+plot['file_path'].split('/')[-1])

            plot['title'] = plot['title']+", "+util.pf(float(num_lines)/5.0)+" instances]"
    
            mode, cbar_label = 'percentage' ,  "$Frequency \quad (\%)$" # defaults
            if configs['mode'].strip() == 'count':
                cbar_label = "$Frequency \quad (log_2)$"
                mode = 'count'            
            #-------------------------------------
            df = open (plot['file_path'], 'r')
            #-------------------------------------            
            lines_so_far, fraction_freq  = 0, {}
            while lines_so_far < num_lines:
                Bs_Ds         = {}
                next(df)      # skip over objects
                Bs        = [int(s) for s in next(df).split()]
                Ds        = [int(s) for s in next(df).split()]
                next(df)      #skip over Xs (solution vector)
                next(df)      #skip over coresize/exec_time
                lines_so_far += 5         
                assert len(Bs) == len(Ds)

                if len(Bs)>0:
                    Bs_Ds  = Counter ([bd for bd in zip(Bs, Ds)])                  
                    for obj in Bs_Ds.keys():
                        if obj not in fraction_freq.keys(): 
                            fraction_freq[obj] = {'avg_frac_sofar':0.0,'count_sofar':0.0}
                        fraction  =  float(Bs_Ds[obj])/len(Bs)
                        fraction_freq[obj]['avg_frac_sofar']   = ((fraction_freq[obj]['avg_frac_sofar']*fraction_freq[obj]['count_sofar']) + fraction ) /  (fraction_freq[obj]['count_sofar'] + 1)
                        fraction_freq[obj]['count_sofar']      = fraction_freq[obj]['count_sofar'] + 1             
                del Bs_Ds
            Bs, Ds, frequency = [],[],[]
            for obj in fraction_freq.keys():
                Bs.append(obj[0])
                Ds.append(obj[1])
                if mode == 'percentage':
                    frequency.append(fraction_freq[obj]['avg_frac_sofar']*100) # convert it to %
                else:
                    frequency.append(math.log (fraction_freq[obj]['count_sofar'], 2))

            if rank == 1 and mode == 'percentage':
                master.print_freqs(fraction_freq, plot['file_path'], configs['worker_log'])                 

            plot['data'], plot['worker_configs'], plot['rank'] = {'Bs':Bs, 'Ds':Ds, 'frequency':frequency, 'xlim':xlim, 'ylim':ylim, 'cbar_label':cbar_label}, configs, rank
            ##########################
            master.dump(plot)
            ##########################
        else:
            mywrite(log,"\n\t\t\t\tworker #"+str(rank)+": skipping: "+plot['file_path'].split('/')[-1])   
#######################################################################################
def ETX_init(plot, configs):
    cruncher = None
    if 'cruncher' in configs.keys():
        if configs['cruncher'] in globals().keys():
            cruncher = globals()[configs['cruncher']]
        else:
            cruncher = ETXcruncher1 # default    
    else:
        cruncher = ETXcruncher1 # default
    
    all_files = {}
    assert os.path.isdir(plot['file_path'])
    for root, dirs, files in os.walk(plot['file_path']): #'file_path' is a actually a dir path
        for f in files:
            if f.split('.')[-1] == 'csv':
                # extract p,t; Vinayagam_RAW_INSTANCES_p100.0_t001.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv
                PT =[float(x.replace('p','').replace('t','')) for x in f.split('/')[-1].split('_RAW_INSTANCES_')[-1].split('_')[0:2]]
                p,t = PT[0], PT[1]
                all_files[(p,t)] = os.path.join(root,f)
    
    # Ps and Ts are mandatory in params file
    Ps = configs['Ps']#[float(p.strip()) for p in configs['Ps'].split(',')]
    Ts = configs['Ts']#[float(t.strip()) for t in configs['Ts'].split(',')]
    
    data = {} 
    for p in Ps:
        for t in Ts:
            data[(p,t)]={}
            data[(p,t)]['csv']           = all_files[(p,t)]
            data[(p,t)]['num_instances'] = 0
            data[(p,t)]['STATS']         = {}
    
    return cruncher, data
#######################################################################################
def ETXcruncher1(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # % contribution of nodes of deg x to total BIN/DIN/BOU/DOU
    if not final: 
        by_degree, BIN, DIN, BOU, DOU = instanceBYdegree(Gs,Bs,Ds,Xs)        
        BIN, DIN, BOU, DOU        = max(BIN,1), max(DIN,1), max(BOU,1), max(DOU,1) # avoid division by zero
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = (sum(by_degree[deg]['bin'])/BIN)*100
            by_degree[deg]['din'] = (sum(by_degree[deg]['din'])/DIN)*100
            by_degree[deg]['bou'] = (sum(by_degree[deg]['bou'])/BOU)*100
            by_degree[deg]['dou'] = (sum(by_degree[deg]['dou'])/DOU)*100
        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])
    else: 
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou'])
#######################################################################################
def ETXcruncher2(Gs,Bs,Ds,Xs,BY_DEGREE): # ETB, normalizing by Ds
    by_degree, BIN, DIN, BOU, DOU = instanceBYdegree(Gs,Bs,Ds,Xs)        
    BIN, DIN, BOU, DOU        = max(BIN,1), max(DIN,1), max(BOU,1), max(DOU,1) # avoid division by zero       
    for deg in by_degree.keys():
        by_degree[deg]['bin2din'] = (sum([b/max(1,d) for b,d in zip (by_degree[deg]['bin'], by_degree[deg]['din'])])      /BIN)*100
        by_degree[deg]['bou2dou'] = (sum([b/max(1,d) for b,d in zip (by_degree[deg]['bou'], by_degree[deg]['dou'])])      /BOU)*100
    updateSTATS(by_degree, BY_DEGREE, ['bin2din','bou2dou'])
#######################################################################################     
def ETXcruncher3(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # ETB, normalizing by (number of nodes of degree x in the instance)/(instance size)
    if not final:
        by_degree, BIN, DIN, BOU, DOU  = instanceBYdegree(Gs,Bs,Ds,Xs)        
        BIN, DIN, BOU, DOU         = max(BIN,1), max(DIN,1), max(BOU,1), max(DOU,1) # avoid division by zero   
        size_in, size_ou           = len([x for x in Xs if x ==1]), len([x for x in Xs if x ==0])
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = (sum(by_degree[deg]['bin']) * (1 - (len(by_degree[deg]['bin'])/size_in)) / BIN) *100
            #by_degree[deg]['bin']  = (np.average(by_degree[deg]['bin'])/BIN)*100 # this is Sbin (taking a set)
            by_degree[deg]['din'] = (sum(by_degree[deg]['din']) * (1 - (len(by_degree[deg]['din'])/size_in)) / DIN) *100
            by_degree[deg]['bou'] = (sum(by_degree[deg]['bou']) * (1 - (len(by_degree[deg]['bou'])/size_ou)) / BOU) *100
            by_degree[deg]['dou'] = (sum(by_degree[deg]['dou']) * (1 - (len(by_degree[deg]['dou'])/size_ou)) / DOU) *100

        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])  
    else: 
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou']) # we're done crunching, normalize all stats to add up to unity (100%)
#######################################################################################
#######################################################################################     
def ETX_processor (configs, pair, rank): 
    log           = configs['worker_log']
    for plot in pair: 
        if plot['processing_bit'] == 1:  
            ############################################
            cruncher, data = ETX_init(plot, configs) 
            ############################################
            mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": applying "+cruncher.__name__+" on "+plot['file_path'][0:90]+"...")
            for PT in data.keys():                
                df = open (data[PT]['csv'], 'r')
                lines_so_far = 0
                while lines_so_far+5 <= configs['max_lines']:                
                    Gs     = [g for g in next(df).strip().split()]
                    Bs     = [int(s) for s in next(df).strip().split()]
                    Ds     = [int(s) for s in next(df).strip().split()]
                    Xs     = [int(x) for x in next(df).strip().split()]  #skip over Xs (solution vector)
                    next(df)                                     #skip over coresize/exec_time
                    lines_so_far += 5         
                    assert len(Bs) == len(Ds)
                    if len(Bs)>0:
                        cruncher(Gs,Bs,Ds,Xs,data[PT]['STATS'])    
                if cruncher in [ETXcruncher1,ETXcruncher3]:
                    cruncher(None,None,None,None,data[PT]['STATS'],final=True) # normalize collected stats to add up to unity (100$)
                data[PT]['num_instances']=int(lines_so_far/5)
            plot['title'] = plot['title']+", "+util.pf(float(configs['max_lines']))+" instances]"
            plot['data'], plot['worker_configs'], plot['rank'] = data , configs, rank
            #with open('dump'+str(rank)+'-'+str(plot['pos']),'wb') as f:
            #    import pickle
            #    pickle.dump(plot,f)
            #    f.close()
            ##########################
            master.dump(plot)
            ##########################
        else:
            mywrite(log,"\n\t\t\t\tworker #"+str(rank)+": skipping "+plot['file_path'][0:90])     
#######################################################################################