import random,util, math

#--------------------------------------------------------------------------------------------------  
def reverse_reduction(M, P_nodes, T_percentage, advice_sampling_threshold, BD_criteria):    
    if  advice_sampling_threshold <=0:
        yield [{},{},0]
    elif BD_criteria == 'source':
        for i in range(advice_sampling_threshold):
            yield [
                    BDT_calculator_source (M, util.advice(util.sample_p_genes(M.nodes(),P_nodes)), T_percentage)
                  ]
    elif BD_criteria == 'target':
        for i in range(advice_sampling_threshold):
            yield [
                    BDT_calculator_target (M, util.advice(util.sample_p_genes(M.nodes(),P_nodes)), T_percentage)
                  ]
    else:
        for i in range(advice_sampling_threshold):
            yield [
                    BDT_calculator_both (M, util.advice(util.sample_p_genes(M.nodes(),P_nodes)), T_percentage)
                  ]      
#--------------------------------------------------------------------------------------------------  
def scramble_reduction(M, P_nodes, T_percentage, advice_sampling_threshold, BD_criteria):    
    if  advice_sampling_threshold <=0:
        yield [{},{},0]    
    if BD_criteria == 'source':
        for i in range(advice_sampling_threshold):
            yield [
                    scramble (BDT_calculator_source (M, util.advice(util.sample_p_genes(M.nodes(),P_nodes)), T_percentage))
                  ]
    elif BD_criteria == 'target':
        for i in range(advice_sampling_threshold):
            yield [
                    scramble (BDT_calculator_target (M, util.advice(util.sample_p_genes(M.nodes(),P_nodes)), T_percentage))
                  ]
    else:
        for i in range(advice_sampling_threshold):
            yield [
                    scramble (BDT_calculator_both (M, util.advice(util.sample_p_genes(M.nodes(),P_nodes)), T_percentage))
                  ]      
#--------------------------------------------------------------------------------------------------            
def BDT_calculator_source (M, Advice, T_percentage):
    BENEFITS, DAMAGES, relevant_edges = {}, {}, 0
    for target in Advice.keys():
        for source in M.predecessors (target):
            relevant_edges +=1
            if M[source][target]['sign']==Advice[target]:      #in agreement with the Oracle
                ######### REWARDING the source node ###########
                if source in BENEFITS.keys():
                    BENEFITS[source]+=1
                else:
                    BENEFITS[source]=1
                    if source not in DAMAGES.keys():
                        DAMAGES[source]=0    
            else:                                              #in disagreement with the Oracle
                ######### PENALIZING the source node ##########
                if source in DAMAGES.keys():
                    DAMAGES[source]+=1
                else:
                    DAMAGES[source]=1
                    if source not in BENEFITS.keys():
                        BENEFITS[source]=0
    
    T_edges = max (1, math.ceil (relevant_edges*(T_percentage/100)))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------                
def BDT_calculator_target (M, Advice, T_percentage):
    BENEFITS, DAMAGES, relevant_edges = {}, {}, 0
    for target in Advice.keys():
        for source in M.predecessors (target):
            relevant_edges +=1
            if M[source][target]['sign']==Advice[target]:      #in agreement with the Oracle  
                ######### REWARDING the target node ###########
                if target in BENEFITS.keys():
                    BENEFITS[target]+=1
                else:
                    BENEFITS[target]=1
                    if target not in DAMAGES.keys():
                        DAMAGES[target]=0   
            else:                                              #in disagreement with the Oracle
                ######### PENALIZING the target node ##########
                if target in DAMAGES.keys():
                    DAMAGES[target]+=1
                else:
                    DAMAGES[target]=1
                    if target not in BENEFITS.keys():
                        BENEFITS[target]=0
                ###############################################
    
    T_edges = max (1, math.ceil (relevant_edges*(T_percentage/100)))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------                
def BDT_calculator_both (M, Advice, T_percentage):
    BENEFITS, DAMAGES, relevant_edges = {}, {}, 0
    for target in Advice.keys():
        for source in M.predecessors (target):
            relevant_edges +=1
            if M[source][target]['sign']==Advice[target]:      #in agreement with the Oracle
                ######### REWARDING the source node ###########
                if source in BENEFITS.keys():
                    BENEFITS[source]+=1
                else:
                    BENEFITS[source]=1
                    if source not in DAMAGES.keys():
                        DAMAGES[source]=0    
                ######### REWARDING the target node ###########
                if target in BENEFITS.keys():
                    BENEFITS[target]+=1
                else:
                    BENEFITS[target]=1
                    if target not in DAMAGES.keys():
                        DAMAGES[target]=0   
                ###############################################
                ###############################################
            else:                                              #in disagreement with the Oracle
                ######### PENALIZING the source node ##########
                if source in DAMAGES.keys():
                    DAMAGES[source]+=1
                else:
                    DAMAGES[source]=1
                    if source not in BENEFITS.keys():
                        BENEFITS[source]=0
                ######### PENALIZING the target node ##########
                if target in DAMAGES.keys():
                    DAMAGES[target]+=1
                else:
                    DAMAGES[target]=1
                    if target not in BENEFITS.keys():
                        BENEFITS[target]=0
                ###############################################
    
    T_edges = max (1, math.ceil (relevant_edges*(T_percentage/100)))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------
def scramble (NEP_instance):
    randomized_BENEFITS, randomized_DAMAGES, T_edges = NEP_instance[0], NEP_instance[1], NEP_instance[2]
    assert len(randomized_BENEFITS.keys())==len(randomized_DAMAGES.keys())
    if len(randomized_BENEFITS.keys()) == 0:
        return {},{},0
    original_Bsum, original_Dsum, random_Bsum, random_Dsum = sum(randomized_BENEFITS.values()), sum(randomized_DAMAGES.values()), 0, 0
    
    KEYS = list(randomized_BENEFITS.keys())
    
    for key in KEYS:
        randomized_BENEFITS[key], randomized_DAMAGES[key] = 0, 0
    # spread benefits/damages around randomly
    while random_Bsum < original_Bsum:
        random_key = random.SystemRandom().sample(KEYS,1)[0] 
        randomized_BENEFITS[random_key] += 1  
        random_Bsum +=1
    while random_Dsum < original_Dsum:
        random_key = random.SystemRandom().sample(KEYS,1)[0] 
        randomized_DAMAGES[random_key] += 1
        random_Dsum +=1

    assert random_Bsum == original_Bsum and random_Dsum == original_Dsum
    
    return randomized_BENEFITS, randomized_DAMAGES, T_edges
    
    #the code below is too slow
    '''
    let:
        bmax, bmin  = max(Bs), min(Bs)  where Bs/Ds are list of benefits/damages (values/weights in Knapsack jargon)
        dmax, dmin  = max(Ds), min(Ds) 
        MAX, MIN    = max(bmax,dmax), min(bmin,dmin) 
        n           = len(Bs) = len(Ds)
    define:
        random_Bs   = [rb_1, rb_2, .... rb_n]
        random_Ds   = [rd_1, rd_2, .... rd_n]
        where:
                  rb_x, rd_x is selected uniformly randomly from [MIN, MAX]
        and:
                  random_Bs, random_Ds are subsequently adjusted such that:
                  sum (sum(random_Bs) + sum(random_Ds)) == sum (sum(Bs) + sum(Ds))
                  (by randomly timming/topping off some rb_x or rd_x till the above equality holds

    return:
        [random_Bs, random_Ds, T_edges (=knapsack_size, as-received)
    
    t0=time.time()
    BENEFITS, DAMAGES, T_edges = NEP_instance[0], NEP_instance[1], NEP_instance[2]
    Bs, Ds = [],[]
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    for gene in BENEFITS.keys():
        Bs.append(BENEFITS[gene])
        Ds.append(DAMAGES[gene])    
    if len(Bs) == 0:
        return {},{},0
    num_edges  = sum(Bs)+sum(Ds)

    random_Bs, random_Ds  = [], []
    #--------------------------------------------------------------------
    random_max,random_min = max (max(Bs),max(Ds)),  min (min(Bs),min(Ds))
    #--------------------------------------------------------------------
    for i in range(len(Bs)):
        random_Bs.append(random.SystemRandom().sample (range(random_min, random_max+1),1)[0])
        random_Ds.append(random.SystemRandom().sample (range(random_min, random_max+1),1)[0])

    num_random_edges  = sum(random_Bs)+sum(random_Ds)
    # trim/top-off random Bs/Ds till num_random_edges == num_edges
    while num_random_edges != num_edges:
        if num_random_edges > num_edges: #trim
            if util.flip() == 1:
                random_index_b = random.SystemRandom().sample(range(len(random_Bs)),1)[0] 
                random_Bs[random_index_b] = max(0, random_Bs[random_index_b] - 1)
            else:
                random_index_d = random.SystemRandom().sample(range(len(random_Bs)),1)[0]
                random_Ds[random_index_d] = max(0, random_Ds[random_index_d] - 1)
            num_random_edges = sum(random_Bs)+sum(random_Ds)
        elif num_random_edges < num_edges: #top-off:
            if util.flip() == 1:
                random_index_b = random.SystemRandom().sample(range(len(random_Bs)),1)[0]
                random_Bs [random_index_b] = random_Bs [random_index_b] + 1
            else:
                random_index_d = random.SystemRandom().sample(range(len(random_Bs)),1)[0]
                random_Ds [random_index_d] = random_Ds [random_index_d] + 1
            num_random_edges = sum(random_Bs)+sum(random_Ds)

    #-----------------------------------------------------------------------------------------------
    assert num_random_edges == num_edges # the random instance is a true analog of the input instance
    #-----------------------------------------------------------------------------------------------
    # turn random_Bs, random_Ds into dictionaries (solver.solve_knapsack(..) expects dicts)
    size = len(random_Bs)
    BENEFITS_scrambled, DAMAGES_scrambled = {}, {}
    i=0
    for k in BENEFITS.keys():
        #next_key = str(k).rjust(int(math.log(max(1,size),10)+1),'0')
        BENEFITS_scrambled[k] = random_Bs[i]
        DAMAGES_scrambled [k] = random_Ds[i]
        i+=1
    assert (i) == len(random_Bs) == len(random_Ds)
    t1=time.time()
    print (str(t1-t0)+' s')
    return BENEFITS_scrambled, DAMAGES_scrambled, T_edges

    '''
#--------------------------------------------------------------------------------------------------
