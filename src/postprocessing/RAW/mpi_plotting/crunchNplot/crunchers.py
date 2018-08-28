import sys,os,copy,math,numpy as np
from collections import Counter
sys.path.insert(0, os.getenv('lib'))
import time, util_plotting as util, utilv4 as superutil, master_cruncher as master
#######################################################################################
mywrite = util.mywrite
avg     = np.average
std     = np.std
sdiv    = superutil.savedivision
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
            #if stats[deg][m]>0: ###### ? ########
            STATS[deg][m]['AsF'], STATS[deg][m]['CsF'] = ReAvg (STATS[deg][m]['AsF'], STATS[deg][m]['CsF'], stats[deg][m])
#######################################################################################
def normalizeSTATS(STATS, metrics):
    for m in metrics:
        AVG = float(sum([STATS[deg][m]['AsF'] for deg in STATS.keys()]))
        CNT = float(sum([STATS[deg][m]['CsF'] for deg in STATS.keys()]))
        for deg in STATS.keys():
            STATS[deg][m]['AsF'] = sdiv(STATS[deg][m]['AsF'], AVG)*100
            STATS[deg][m]['CsF'] = sdiv(STATS[deg][m]['CsF'], CNT)*100
#######################################################################################
def CSVsByPTs(csv_dir,spoint='_RAW_INSTANCES_'):
    all_files={}
    assert os.path.isdir(csv_dir)
    for root, dirs, files in os.walk(csv_dir): #'file_path' is a actually a dir path
        for f in files:
            if f.split('.')[-1] == 'csv':
                # extract p,t; Vinayagam_RAW_INSTANCES_p100.0_t001.0_V4NU_MINKNAP_4X_BOTH_REVERSE_alpha0.2.October-06-2016-h07m49s02.csv
                PT =[float(x.replace('p','').replace('t','')) for x in f.split('/')[-1].split(spoint)[-1].split('_')[0:2]]
                p,t = PT[0], PT[1]
                all_files[(p,t)] = os.path.join(root,f)
    return all_files
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
        slices['segments'][key]['fractions'].append(sdiv(float(slices['segments'][key]['count']),instance_size))  # <<<<<<<<<<<<<<< #
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
        slices['segments'][key]['fractions'].append(sdiv(float(slices['segments'][key]['count']),sum(Bs)))
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
        slices['segments'][key]['fractions'].append(sdiv(float(slices['segments'][key]['count']),sum(Bs)))
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
            tmp_freq[slice_id][degree] =  sdiv(tmp_freq[slice_id][degree] , normalizer)
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
    log, num_instances = configs['worker_log'], 0
    if sum(plot['processing_bit'] for plot in pair) >= 1:
        num_instances = master.max_instances(pair, configs, 5)
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

            plot['title'] = plot['title']+", "+util.pf(float(num_instances))+" instances]"
            #file_no, coords, pos, prefix, file_path, title, processing_bit = plot['file_no'], ['coords'], plot['pos'], plot['prefix'], plot['file_path'], plot['title'], plot['processing_bit']

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
            instances_so_far = 0
            while instances_so_far < num_instances:
                Gs     = [g for g in next(df).strip().split()]
                Bs     = [int(s) for s in next(df).strip().split()]
                Ds     = [int(s) for s in next(df).strip().split()]
                Xs     = [int(x) for x in next(df).strip().split()]  #skip over Xs (solution vector)
                next(df)                                     #skip over coresize/exec_time
                instances_so_far += 1
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
    log, xlim, ylim, num_instances = configs['worker_log'], 0, 0, 0
    if sum([plot['processing_bit'] for plot in pair]) >= 1:
        xlim, ylim, num_instances = master.calculate_Axis_limits (pair, configs)

    for plot in pair:
        if plot['processing_bit'] == 1:
            mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": applying scatter on "+plot['file_path'].split('/')[-1])

            plot['title'] = plot['title']+", "+util.pf(float(num_instances))+" instances]"

            mode, cbar_label = 'percentage' ,  "Frequency  (%)" # defaults
            if configs['mode'].strip() == 'count':
                cbar_label = "Frequency (log_2)"
                mode = 'count'
            #-------------------------------------
            df = open (plot['file_path'], 'r')
            #-------------------------------------
            instances_so_far, fraction_freq  = 0, {}
            while instances_so_far < num_instances:
                Bs_Ds         = {}
                next(df)      # skip over objects
                Bs        = [int(s) for s in next(df).split()]
                Ds        = [int(s) for s in next(df).split()]
                next(df)      #skip over Xs (solution vector)
                next(df)      #skip over coresize/exec_time
                instances_so_far += 1
                assert len(Bs) == len(Ds)

                if len(Bs)>0:
                    Bs_Ds  = Counter ([bd for bd in zip(Bs, Ds)])
                    for obj in Bs_Ds.keys():
                        if obj not in fraction_freq.keys():
                            fraction_freq[obj] = {'avg_frac_sofar':0.0,'count_sofar':0.0}
                        fraction  =  sdiv(float(Bs_Ds[obj]), len(Bs))
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

    ###############################################################
    all_files = CSVsByPTs(plot['file_path'])
    ###############################################################

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
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = sdiv(sum(by_degree[deg]['bin']), BIN)*100
            by_degree[deg]['din'] = sdiv(sum(by_degree[deg]['din']), DIN)*100
            by_degree[deg]['bou'] = sdiv(sum(by_degree[deg]['bou']), BOU)*100
            by_degree[deg]['dou'] = sdiv(sum(by_degree[deg]['dou']), DOU)*100
        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])
    else:  # will never execute of configs['normalize2unity'] == false
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou'])
#######################################################################################
def ETXcruncher1b(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # % contribution of nodes of deg x to total BIN/DIN/BOU/DOU
    if not final:
        by_degree, BIN, DIN, BOU, DOU = instanceBYdegree(Gs,Bs,Ds,Xs)
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = sdiv(sum(by_degree[deg]['bin']), BIN+BOU)*100
            by_degree[deg]['din'] = sdiv(sum(by_degree[deg]['din']), DIN+DOU)*100
            by_degree[deg]['bou'] = sdiv(sum(by_degree[deg]['bou']), BOU+BIN)*100
            by_degree[deg]['dou'] = sdiv(sum(by_degree[deg]['dou']), DOU+DIN)*100
        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])
    else:  # will never execute of configs['normalize2unity'] == false
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou'])
#######################################################################################
def ETXcruncher2a(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # ETB, normalizing by Ds
    if not final:
        by_degree, BIN, DIN, BOU, DOU = instanceBYdegree(Gs,Bs,Ds,Xs)
        for deg in by_degree.keys():
            by_degree[deg]['bin2din'] = sdiv(sdiv(sum(by_degree[deg]['bin']), sum(by_degree[deg]['din']))  , sdiv(BIN,DIN))*100
            by_degree[deg]['bou2dou'] = sdiv(sdiv(sum(by_degree[deg]['bou']), sum(by_degree[deg]['dou']))  , sdiv(BOU,DOU))*100

        updateSTATS(by_degree, BY_DEGREE, ['bin2din','bou2dou'])
    else:  # will never execute of configs['normalize2unity'] == false
        normalizeSTATS(BY_DEGREE, ['bin2din','bou2dou'])
#######################################################################################
def ETXcruncher2b(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # ETB, normalizing by Ds
    if not final:
        by_degree, BIN, DIN, BOU, DOU = instanceBYdegree(Gs,Bs,Ds,Xs)
        for deg in by_degree.keys():
            by_degree[deg]['bin2din'] = sdiv(sdiv(sum(by_degree[deg]['bin']), sum(by_degree[deg]['din']))  , BIN)*100
            by_degree[deg]['bou2dou'] = sdiv(sdiv(sum(by_degree[deg]['bou']), sum(by_degree[deg]['dou']))  , BOU)*100

        updateSTATS(by_degree, BY_DEGREE, ['bin2din','bou2dou'])
    else:  # will never execute of configs['normalize2unity'] == false
        normalizeSTATS(BY_DEGREE, ['bin2din','bou2dou'])
#######################################################################################
def ETXcruncher3(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # ETB, normalizing by (number of nodes of degree x in the instance)/(instance size)
    if not final:
        by_degree, BIN, DIN, BOU, DOU  = instanceBYdegree(Gs,Bs,Ds,Xs)
        size_in, size_ou           = len([x for x in Xs if x ==1]), len([x for x in Xs if x ==0])
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = sdiv(sum(by_degree[deg]['bin']) * (1 - sdiv(len(by_degree[deg]['bin']), size_in)) , 1) *100
            by_degree[deg]['din'] = sdiv(sum(by_degree[deg]['din']) * (1 - sdiv(len(by_degree[deg]['din']), size_in)) , 1) *100
            by_degree[deg]['bou'] = sdiv(sum(by_degree[deg]['bou']) * (1 - sdiv(len(by_degree[deg]['bou']), size_ou)) , 1) *100
            by_degree[deg]['dou'] = sdiv(sum(by_degree[deg]['dou']) * (1 - sdiv(len(by_degree[deg]['dou']), size_ou)) , 1) *100
        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])
    else:  # will never execute of configs['normalize2unity'] == false
        # we're done crunching, normalize all stats to add up to unity (100%),
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou'])
#######################################################################################
def ETXcruncher4(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # ETB, normalizing by (number of nodes of degree x in the instance)/(instance size)
    if not final:
        by_degree, BIN, DIN, BOU, DOU  = instanceBYdegree(Gs,Bs,Ds,Xs)
        size_in, size_ou           = len([x for x in Xs if x ==1]), len([x for x in Xs if x ==0])
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = sdiv(sdiv(sum(by_degree[deg]['bin']), len(by_degree[deg]['bin'])), BIN)*100
            by_degree[deg]['din'] = sdiv(sdiv(sum(by_degree[deg]['din']), len(by_degree[deg]['din'])), DIN)*100
            by_degree[deg]['bou'] = sdiv(sdiv(sum(by_degree[deg]['bou']), len(by_degree[deg]['bou'])), BOU)*100
            by_degree[deg]['dou'] = sdiv(sdiv(sum(by_degree[deg]['dou']), len(by_degree[deg]['dou'])), DOU)*100

        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])
    else:  # will never execute of configs['normalize2unity'] == false
        # we're done crunching, normalize all stats to add up to unity (100%),
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou'])
#######################################################################################
def ETXcruncher5(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # same as 4, but % of ETB instead of BIN
    if not final:
        by_degree, BIN, DIN, BOU, DOU  = instanceBYdegree(Gs,Bs,Ds,Xs)
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = sdiv(sum(by_degree[deg]['bin']), len(by_degree[deg]['bin']))
            by_degree[deg]['din'] = sdiv(sum(by_degree[deg]['din']), len(by_degree[deg]['din']))
            by_degree[deg]['bou'] = sdiv(sum(by_degree[deg]['bou']), len(by_degree[deg]['bou']))
            by_degree[deg]['dou'] = sdiv(sum(by_degree[deg]['dou']), len(by_degree[deg]['dou']))
        ###############################################################
        ETBin = sum(by_degree[deg]['bin'] for deg in by_degree.keys())
        ETDin = sum(by_degree[deg]['din'] for deg in by_degree.keys())
        ETBou = sum(by_degree[deg]['bou'] for deg in by_degree.keys())
        ETDou = sum(by_degree[deg]['dou'] for deg in by_degree.keys())
        ###############################################################
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = sdiv(by_degree[deg]['bin'], ETBin)*100
            by_degree[deg]['din'] = sdiv(by_degree[deg]['din'], ETDin)*100
            by_degree[deg]['bou'] = sdiv(by_degree[deg]['bou'], ETBou)*100
            by_degree[deg]['dou'] = sdiv(by_degree[deg]['dou'], ETDou)*100

        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])
    else: # will never execute of configs['normalize2unity'] == false
        # we're done crunching, normalize all stats to add up to unity (100%),
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou'])
#######################################################################################
def ETXcruncher_aggr(Gs,Bs,Ds,Xs,STATS,final=False): # BIN / (BIN+BOU)
    if not final:
        if len(STATS.keys())==0: # this is the first call
            STATS['bin2binPLUSbou'] = {'AsF':0.0,'CsF':0}
            STATS['bin2binPLUSdin'] = {'AsF':0.0,'CsF':0}
            STATS['bin2din']        = {'AsF':0.0,'CsF':0}
            STATS['Sbin2bin']       = {'AsF':0.0,'CsF':0}

        else:
            BIN  = sum([e[0] for e in zip(Bs,Xs) if e[1]==1])
            BOU  = sum([e[0] for e in zip(Bs,Xs) if e[1]==0])
            DIN  = sum([e[0] for e in zip(Ds,Xs) if e[1]==1])
            DOU  = sum([e[0] for e in zip(Ds,Xs) if e[1]==0])
            Sbin = sum(set([e[0] for e in zip(Bs,Xs) if e[1]==1]))
            assert BIN+BOU == sum(Bs) and DIN+DOU == sum(Ds)

            STATS['bin2binPLUSbou']['AsF'], STATS['bin2binPLUSbou']['CsF']  = ReAvg (STATS['bin2binPLUSbou']['AsF'], STATS['bin2binPLUSbou']['CsF'], sdiv(BIN,BIN+BOU)*100)
            STATS['bin2binPLUSdin']['AsF'], STATS['bin2binPLUSdin']['CsF']  = ReAvg (STATS['bin2binPLUSdin']['AsF'], STATS['bin2binPLUSdin']['CsF'], sdiv(BIN,BIN+DIN)*100)
            STATS['bin2din']['AsF'], STATS['bin2din']['CsF']                = ReAvg (STATS['bin2din']['AsF'], STATS['bin2din']['CsF'], sdiv(BIN,DIN))
            STATS['Sbin2bin']['AsF'], STATS['Sbin2bin']['CsF']              = ReAvg (STATS['Sbin2bin']['AsF'], STATS['Sbin2bin']['CsF'], sdiv(Sbin,BIN)*100)
#######################################################################################
def ETXcruncher_aggr2(Gs,Bs,Ds,Xs,STATS,final=False): # BIN / (BIN+BOU)
    if not final:
        if len(STATS.keys())==0: # this is the first call
            STATS['bin2binPLUSbou'] = {'AsF':0.0,'CsF':0}
            STATS['bin2din']        = {'AsF':0.0,'CsF':0}

        else:
            BIN  = [e[0] for e in zip(Bs,Xs) if e[1]==1]
            BOU  = [e[0] for e in zip(Bs,Xs) if e[1]==0]
            DIN  = [e[0] for e in zip(Ds,Xs) if e[1]==1]
            DOU  = [e[0] for e in zip(Ds,Xs) if e[1]==0]

            bin2din        = sdiv (sum([sdiv(b,d)         for b,d     in zip(BIN,DIN)]), sum(BIN)         )*100
            bin2binPLUSbou = sdiv (sum(BIN)                                            , sum(BIN)+sum(BOU))*100


            STATS['bin2din']['AsF'], STATS['bin2din']['CsF']                = ReAvg (STATS['bin2din']['AsF'], STATS['bin2din']['CsF'], bin2din)
            STATS['bin2binPLUSbou']['AsF'], STATS['bin2binPLUSbou']['CsF']  = ReAvg (STATS['bin2binPLUSbou']['AsF'], STATS['bin2binPLUSbou']['CsF'], bin2binPLUSbou)
#######################################################################################
def ETXcruncher_gTB(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # greedy IN/OUT
    if not final:
        DEGs = []
        for g in Gs:
            DEGs.append (sum([int(deg) for deg in g.split('$')[1:]]))

        BIN  = sum([e[0] for e in zip(Bs,Xs) if e[1]==1])
        BOU  = sum([e[0] for e in zip(Bs,Xs) if e[1]==0])
        DIN  = sum([e[0] for e in zip(Ds,Xs) if e[1]==1])
        DOU  = sum([e[0] for e in zip(Ds,Xs) if e[1]==0])
        by_degree = {}
        for deg in set(DEGs):
            by_degree[deg] = {'bin':0,'din':0,'bou':0,'dou':0}

        Bs2Ds    = [sdiv(b,b+d) for b,d in zip(Bs,Ds)]
        greedyIN = sorted(zip(DEGs, Bs, Ds, Xs), key=lambda x: x[0], reverse=True) # sort ascendingly by degree
        greedyOU = sorted(zip(DEGs, Bs, Ds, Xs), key=lambda x: x[0], reverse=True) # sort ascendingly by degree

        gDIN, i, T = 0, 0, 0.20*len(Gs)
        while (gDIN < DIN or gDIN == 0) and i<= T: # greedy conserve (gain)
            if greedyIN[i][3] == 1:
                by_degree[greedyIN[i][0]]['bin'] += greedyIN[i][1]
                by_degree[greedyIN[i][0]]['din'] += greedyIN[i][2]
                gDIN                             += greedyIN[i][2]
            i                                += 1
        gBOU, i = 0, 0
        while (gBOU < BOU or gBOU == 0):# and i<=T: # greedy delete (cleanse)
            by_degree[greedyOU[i][0]]['bou'] += greedyOU[i][1]
            by_degree[greedyOU[i][0]]['dou'] += greedyOU[i][2]
            gBOU                             += greedyOU[i][1]
            i                                += 1
        for deg in by_degree.keys():
            by_degree[deg]['bin'] = sdiv(by_degree[deg]['bin'], BIN)*100 # greedy vs optimal BIN
            by_degree[deg]['din'] = sdiv(by_degree[deg]['din'], DIN)*100
            by_degree[deg]['bou'] = sdiv(by_degree[deg]['bou'], BOU)*100
            by_degree[deg]['dou'] = sdiv(by_degree[deg]['dou'], DOU)*100
        updateSTATS(by_degree, BY_DEGREE, ['bin','din','bou','dou'])
    else:# we don't wanna normalize to unity in this measure
        normalizeSTATS(BY_DEGREE, ['bin','din','bou','dou'])
#######################################################################################
def ETXcruncher_sBIN2totB(Gs,Bs,Ds,Xs,BY_DEGREE,final=False): # sBIN and totBIN as was defined in ACM-BCB paper
    if not final:
        by_degree , BIN, DIN, BOU, DOU = instanceBYdegree(Gs,Bs,Ds,Xs)
        for deg in by_degree.keys():
            by_degree[deg]['sBIN2totB'] = sdiv(sum(set(by_degree[deg]['bin'])), BIN)*100
            by_degree[deg]['sDIN2totD'] = sdiv(sum(set(by_degree[deg]['din'])), DIN)*100
        updateSTATS(by_degree, BY_DEGREE, ['sBIN2totB','sDIN2totD'])
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
                num_instances = min(int(sum([1 for line in df])/5),  configs['max_instances'])
                df.close()
                df = open (data[PT]['csv'], 'r')
                instances_so_far = 0
                while instances_so_far < num_instances:
                    Gs     = [g for g in next(df).strip().split()]
                    Bs     = [int(s) for s in next(df).strip().split()]
                    Ds     = [int(s) for s in next(df).strip().split()]
                    Xs     = [int(x) for x in next(df).strip().split()]  #skip over Xs (solution vector)
                    next(df)                                     #skip over coresize/exec_time
                    instances_so_far += 1
                    assert len(Bs) == len(Ds)
                    if len(Bs)>0:
                        cruncher(Gs,Bs,Ds,Xs,data[PT]['STATS'])
                norm = False
                try:
                    if str(configs['normalize2unity']).strip().lower() == 'true':
                        norm = True
                except:
                    pass # 'normalize2unity' was not provided
                if norm: # default = True
                    cruncher(None,None,None,None,data[PT]['STATS'],final=True) # normalize collected stats to add up to unity (100$)
                data[PT]['num_instances']=int(instances_so_far)
            plot['title'] = plot['title']+", "+util.pf(float(data[PT]['num_instances']))+" instances]"
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
def ExecStats_init(plot, configs):
    cruncher = None
    if 'cruncher' in configs.keys():
        if configs['cruncher'] in globals().keys():
            cruncher = globals()[configs['cruncher']]
        else:
            cruncher = runtime_cruncher # default
    else:
        cruncher = runtime_cruncher # default

    num_instances = sys.maxsize
    if 'max_instances' in configs.keys():
        try:
            if int(configs['max_instances'])>0:
                num_instances = int(configs['max_instances'])
        except:
            pass

    ###############################################################
    all_files = CSVsByPTs(plot['file_path'],spoint='_EXEC_STATS_')
    ###############################################################

    # Ps and Ts are mandatory in params file
    Ps = configs['Ps']#[float(p.strip()) for p in configs['Ps'].split(',')]
    Ts = configs['Ts']#[float(t.strip()) for t in configs['Ts'].split(',')]

    data = {}
    for p in Ps:
        for t in Ts:
            data[(p,t)]={}
            data[(p,t)]['csv']               = all_files[(p,t)]
            data[(p,t)]['num_instances']     = 0
            data[(p,t)]['bar_text']          = ''
            data[(p,t)]['STATS']             = {}
            data[(p,t)]['STATS']['coresize'] = []#{'AsF':0,'CsF':0}
            data[(p,t)]['STATS']['Ctime_s']  = []#{'AsF':0,'CsF':0}
            data[(p,t)]['STATS']['Pytime_s'] = []#{'AsF':0,'CsF':0}
    return cruncher, data, num_instances
#######################################################################################
def runtime_cruncher(stats, STATS, final=False):
    if not final:
        STATS['Ctime_s'].append  (stats[8] )
        STATS['Pytime_s'].append (stats[10])
    else:
        #STATS['Ctime_s']['AsF'], STATS['Pytime_s']['avg'] =  avg(stats['Ctime_s']), avg(stats['Pytime_s'])
        #STATS['Ctime_s']['AsF'], STATS['Pytime_s']['std'] =  std(stats['Ctime_s']), std(stats['Pytime_s'])
        A, S = 0, 0
        if len(STATS['Ctime_s'])>0:
            A = avg(STATS['Ctime_s']) #harvest['data'][(p,t)]['STATS'][bar_key]['avg']
            S = std(STATS['Ctime_s'])
        STATS['Ctime_s']={}
        STATS['Ctime_s']['avg'] = A
        STATS['Ctime_s']['std'] = S
        A, S = 0, 0
        if len(STATS['Pytime_s'])>0:
            A = avg(STATS['Pytime_s']) #harvest['data'][(p,t)]['STATS'][bar_key]['avg']
            S = std(STATS['Pytime_s'])
        STATS['Pytime_s']={}
        STATS['Pytime_s']['avg'] = A
        STATS['Pytime_s']['std'] = S
#######################################################################################
def coresize_cruncher(stats, STATS, final=False):
    # calculate coresize as a % of instance size
    # each line in csv (=stats) is: num_white_genes, num_black_genes, num_grey_genes, TOTAL_Bin, TOTAL_Din, TOTAL_Bou, TOTAL_Dou, core_size,          Ctime_s, Ctime_ms, PythonTime
    if not final:
        num_grey_genes = stats[2]
        coresize = stats[7]
        if num_grey_genes > 0:
            assert coresize <= num_grey_genes
            STATS['coresize'].append  ((coresize/num_grey_genes)*100 )

    else:
        #STATS['coresize']['avg'], STATS['coresize']['std'] =  avg(stats['coresize']), std(stats['coresize'])
        A, S = 0, 0
        if len(STATS['coresize'])>0:
            A = avg(STATS['coresize'])
            S = std(STATS['coresize'])
        #print('\nA= '+str(A))
        #print('\nS= '+str(S))
        STATS['coresize']={}
        STATS['coresize']['avg']=A
        STATS['coresize']['std']=S
#######################################################################################
def ExecStats_processor(configs, pair, rank):
    log           = configs['worker_log']
    for plot in pair:
        if plot['processing_bit'] == 1:
            ##############################################################
            cruncher, data, num_instances = ExecStats_init(plot, configs)
            ##############################################################
            mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": applying "+cruncher.__name__+" on "+plot['file_path'][0:90]+"...")

            for PT in data.keys():
                ####################################################################################
                num_instances = min(sum([1 for line in open (data[PT]['csv'], 'r')]), num_instances)
                ####################################################################################
                df = open (data[PT]['csv'], 'r')
                instances_so_far = 0
                optimized_over_instances = 0
                while instances_so_far < num_instances:
                    stats     = [float(s) for s in next(df).strip().split()]
                    # each line in csv (=stats) is: 0-num_white_genes, 1-num_black_genes, 2-num_grey_genes, 3-TOTAL_Bin, 4-TOTAL_Din, 5-TOTAL_Bou, 6-TOTAL_Dou, 7-core_size, 8-Ctime_s, 9-Ctime_ms, 10-PythonTime
                    # we only consider instances that were optimized over, i.e. grey genes>0, coresize & exec_time > 0 (see minknap_execstats.c)
                    if stats[8]>=0:#stats[7]>0 and stats[8] >0:
                        cruncher(stats, data[PT]['STATS'])
                        optimized_over_instances += 1
                    instances_so_far += 1
                cruncher(None, data[PT]['STATS'], True)
                data[PT]['num_instances']=int(instances_so_far)
                print('\n'+data[PT]['csv'].split('/')[-1]+': optimized_over_instances = '+str(optimized_over_instances))
                data[PT]['bar_text'] = '$'+util.pf(optimized_over_instances)+'/'+util.pf(float(instances_so_far))+'$'
            plot['title'] = plot['title']+", ACTUAL: "+util.pf(float(instances_so_far))+" instances]"
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
def iSize_cruncher(Gs,Bs,Ds,Xs,slices):
    return cruncher1 (Gs,Bs,Ds,Xs,slices)
#######################################################################################
def iSize_init(plot, configs):
    _ , data = ETX_init(plot, configs)
    cruncher = iSize_cruncher
    return cruncher, data
#######################################################################################
def iSize_processor(configs, pair, rank):
    log           = configs['worker_log']
    # you can't do this cos max_instances() expects files not dirs
    #if sum(plot['processing_bit'] for plot in pair) >= 1:
    #    num_instances = master.max_instances(pair, configs, 5)
    for plot in pair:
        if plot['processing_bit'] == 1:
            ############################################
            cruncher, data = iSize_init(plot, configs)
            ############################################
            mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": applying "+cruncher.__name__+" on "+plot['file_path'][0:90]+"...")
            for PT in data.keys():
                df = open (data[PT]['csv'], 'r')
                num_instances = min(int(sum([1 for line in df])/5),  configs['max_instances'])
                df.close()
                df = open (data[PT]['csv'], 'r')
                instances_so_far = 0
                slices      = copy.deepcopy(configs['slices'])
                while instances_so_far < num_instances:
                    try:
                        Gs     = [g for g in next(df).strip().split()]
                        Bs     = [int(s) for s in next(df).strip().split()]
                        Ds     = [int(s) for s in next(df).strip().split()]
                        Xs     = [int(x) for x in next(df).strip().split()]  #skip over Xs (solution vector)
                        next(df)                                     #skip over coresize/exec_time
                        instances_so_far += 1
                        assert len(Bs) == len(Ds)
                        if len(Bs)>0:
                            cruncher(Gs,Bs,Ds,Xs,slices)
                    except:
                        print ("\nError ("+str(instances_so_far)+"): "+str(data[PT]['csv']))
                data[PT]['num_instances']=int(instances_so_far)
                data[PT]['STATS'] = slices
                del slices
            plot['title'] = plot['title']+", "+util.pf(float(instances_so_far))+" instances]"
            plot['data'], plot['worker_configs'], plot['rank'] = data , configs, rank
            ##########################
            master.dump(plot)
            ##########################
        else:
            mywrite(log,"\n\t\t\t\tworker #"+str(rank)+": skipping "+plot['file_path'][0:90])
#######################################################################################
def sSpace_cruncher(Gs,Bs,Ds,sSpace):
    '''
    total_genes     = len( [g for g in zip(Bs,Ds) if g[0]!=0 or  g[1]!=0] ) # total number of genes: ambig + unambig
    ambig_genes     = len( [g for g in zip(Bs,Ds) if g[0]!=0 and g[1]!=0] ) # number of ambigeous genes
    total_space     = 2 ** total_genes
    search_space    = 2 ** ambig_genes
    sSpace['fractions'].append([ambig_genes, total_genes])
    '''
    # 2
    '''
    total_search_space, effective_search_space = 0,0
    for b,d in zip(Bs,Ds):
        #if b>0 or d>0:
        total_search_space     += (b+d)
        #if b>0 and d>0:
        effective_search_space += abs(b-d)
    sSpace['fractions'].append((total_search_space,effective_search_space))
    '''
    # 3
    '''
    if x out y edges are damaging, the prob that a series of mutation transform/disables all x edges is approximated by:
        1/degree * 1/degree * .... x times
        = 1/(degree^x) = 1/(degree^damages)
        => degree^damages = search space size for that gene = Sx

        for all genes, we multiply thru, S1*S2*..Sx...Sn,  this is a large number so we take the log and simplify as follows:

    = log [ degree(n1)^(damage(n1))  * degree(n2)^(damage(n2))* ... degree(nn)^(damage(nn)) ]
    = log [ degree(n1)^(damage(n1))] + log [ degree(n2)^(damage(n2))] + .... + log [ degree(nn)^(damage(nn))]
    = damage(n1)*log[degree(n1)]     + damage(n2)*log[degree(n2)]     + .... + damage(nn)*log[degree(nn)]

    total_search_space, effective_search_space = 0,0
    for g,b,d in zip(Gs,Bs,Ds):
        #if d>0:
        deg = sum([int(x) for x in g.split('$')[1:] ]) # degree = in_degree + out_degree
        total_search_space     += deg*math.log(deg,2)
        effective_search_space += d*math.log(deg,2)
    sSpace['fractions'].append((total_search_space,effective_search_space))
    '''
    # 4
    '''
    total_search_space, effective_search_space = 0,0
    for g,b,d in zip(Gs,Bs,Ds):

        #deg = sum([int(x) for x in g.split('$')[1:] ]) # degree = in_degree + out_degree
        #total_search_space     += deg
        if b>0 and d>0:
            effective_search_space += deg - max(b,d)
    sSpace['fractions'].append((total_search_space,effective_search_space))
    '''
    # 5, good except NL
    '''
    total_search_space, effective_search_space = 0,0
    for b,d in zip(Bs,Ds):
        if b>0 and d>0: # only relevant genes
            total_search_space     += 1
            effective_search_space += 1-(max(b,d)/(b+d))
    sSpace['fractions'].append((total_search_space,effective_search_space))
    '''
    #6
    '''
    total_search_space, effective_search_space = 0,0
    for b,d in zip(Bs,Ds):
        if b>0 and d>0: # only relevant genes
            total_search_space     += 1
            effective_search_space += 1-(abs(b-d)/(b+d))
    sSpace['fractions'].append((total_search_space,effective_search_space))
    '''

    # 7
    
    total_search_space, effective_search_space = 0,0
    for b,d in zip(Bs,Ds):
        if b>0 or d>0: # only relevant genes
            total_search_space     += 1
            effective_search_space += 1-(abs(b-d)/(b+d))
    sSpace['fractions'].append((total_search_space,effective_search_space))
    '''
    #8
    total_search_space, effective_search_space = 0,0
    for b,d in zip(Bs,Ds):
        total_search_space     += 1
        effective_search_space += 1-(abs(b-d)/(b+d))
    sSpace['fractions'].append((total_search_space,effective_search_space))
    '''

#######################################################################################
def sSpace_init(plot, configs):
    _ , data = ETX_init(plot, configs)
    cruncher = sSpace_cruncher
    return cruncher, data
#######################################################################################
def sSpace_processor(configs, pair, rank):
    log           = configs['worker_log']
    # you can't do this cos max_instances() expects files not dirs
    #if sum(plot['processing_bit'] for plot in pair) >= 1:
    #    num_instances = master.max_instances(pair, configs, 5)
    for plot in pair:
        if plot['processing_bit'] == 1:
            ############################################
            cruncher, data = sSpace_init(plot, configs)
            ############################################
            mywrite(log, "\n\t\t\t\tworker #"+str(rank)+": applying "+cruncher.__name__+" on "+plot['file_path'][0:90]+"...")
            for PT in data.keys():
                df = open (data[PT]['csv'], 'r')
                num_instances = min(int(sum([1 for line in df])/5),  configs['max_instances'])
                df.close()
                df = open (data[PT]['csv'], 'r')
                instances_so_far = 0
                sSpace      = copy.deepcopy(configs['slices'])
                while instances_so_far < num_instances:
                    try:
                        #next(df)  #skip over Gs
                        Gs     = [str(g).strip() for g in next(df).strip().split()]
                        Bs     = [int(s) for s in next(df).strip().split()]
                        Ds     = [int(s) for s in next(df).strip().split()]
                        next(df) #skip over Xs
                        next(df) #skip over coresize/exec_time
                        instances_so_far += 1
                        assert len(Bs) == len(Ds)
                        if len(Bs)>0:
                            cruncher(Gs,Bs,Ds,sSpace)
                    except:
                        print ("\nError in sSpace_processor() inside crunchers.py ("+str(instances_so_far)+"): "+str(data[PT]['csv']))
                data[PT]['num_instances']=int(instances_so_far)
                data[PT]['STATS'] = sSpace
                del sSpace
            plot['title'] = plot['title']+", "+util.pf(float(instances_so_far))+" instances]"
            plot['data'], plot['worker_configs'], plot['rank'] = data , configs, rank
            ##########################
            master.dump(plot)
            ##########################
        else:
            mywrite(log,"\n\t\t\t\tworker #"+str(rank)+": skipping "+plot['file_path'][0:90])
#######################################################################################
