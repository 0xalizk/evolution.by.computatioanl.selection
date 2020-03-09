import random, utilv4 as util, math, time, numpy as np

#--------------------------------------------------------------------------------------------------  
def reverse_reduction(M, sample_size, T_percentage, advice_sampling_threshold, advice_upon, biased, BD_criteria):    
    if  advice_sampling_threshold <=0:
        yield [{},{},0]
    else:      
        if advice_upon == 'nodes':
            if BD_criteria == 'source':
                for i in range(advice_sampling_threshold):
                    yield [
                            BDT_calculator_node_source (M, util.advice_nodes (M, util.sample_p_elements(M.nodes(),sample_size), biased), T_percentage)
                          ]
            elif BD_criteria == 'target':
                for i in range(advice_sampling_threshold):
                    yield [
                            BDT_calculator_node_target (M, util.advice_nodes (M, util.sample_p_elements(M.nodes(),sample_size), biased), T_percentage)
                          ]
            else:
                for i in range(advice_sampling_threshold):
                    yield [
                            BDT_calculator_node_both   (M, util.advice_nodes (M, util.sample_p_elements(M.nodes(),sample_size), biased), T_percentage)
                          ]
        elif advice_upon == 'edges':
            if BD_criteria == 'source':
                for i in range(advice_sampling_threshold):
                    yield [
                            BDT_calculator_edge_source (M, util.advice_edges (M, util.sample_p_elements(M.edges(),sample_size), biased), T_percentage)
                          ]
            elif BD_criteria == 'target':
                for i in range(advice_sampling_threshold):
                    yield [
                            BDT_calculator_edge_target (M, util.advice_edges (M, util.sample_p_elements(M.edges(),sample_size), biased), T_percentage)
                          ]
            else:
                for i in range(advice_sampling_threshold):
                    yield [
                            BDT_calculator_edge_both   (M, util.advice_edges (M, util.sample_p_elements(M.edges(),sample_size), biased), T_percentage)
                          ]     
#--------------------------------------------------------------------------------------------------  
def scramble_reduction(M, sample_size, T_percentage, advice_sampling_threshold, advice_upon, biased, BD_criteria):    
    if  advice_sampling_threshold <=0:
        yield [{},{},0]
    else:      
        if advice_upon == 'nodes':
            if BD_criteria == 'source':
                for i in range(advice_sampling_threshold):
                    yield [
                            scramble (BDT_calculator_node_source (M, util.advice_nodes (M, util.sample_p_elements(M.nodes(),sample_size), biased), T_percentage))
                          ]
            elif BD_criteria == 'target':
                for i in range(advice_sampling_threshold):
                    yield [
                            scramble (BDT_calculator_node_target (M, util.advice_nodes (M, util.sample_p_elements(M.nodes(),sample_size), biased), T_percentage))
                          ]
            else:
                for i in range(advice_sampling_threshold):
                    yield [
                            scramble (BDT_calculator_node_both   (M, util.advice_nodes (M, util.sample_p_elements(M.nodes(),sample_size), biased), T_percentage))
                          ]
        elif advice_upon == 'edges':
            if BD_criteria == 'source':
                for i in range(advice_sampling_threshold):
                    yield [
                            scramble (BDT_calculator_edge_source (M, util.advice_edges (M, util.sample_p_elements(M.edges(),sample_size), biased), T_percentage))
                          ]
            elif BD_criteria == 'target':
                for i in range(advice_sampling_threshold):
                    yield [
                            scramble (BDT_calculator_edge_target (M, util.advice_edges (M, util.sample_p_elements(M.edges(),sample_size), biased), T_percentage))
                          ]
            else:
                for i in range(advice_sampling_threshold):
                    yield [
                            scramble (BDT_calculator_edge_both   (M, util.advice_edges (M, util.sample_p_elements(M.edges(),sample_size), biased), T_percentage))
                          ]
#--------------------------------------------------------------------------------------------------            
def BDT_calculator_edge_source (M, Advice, T_percentage):
    BENEFITS, DAMAGES = {}, {}
    for edge in Advice.keys():            
        source, target = edge[0], edge[1]
        if M[source][target]['sign']==Advice[(source, target)]:      #in agreement with the Oracle
            ######### REWARDING the source node ###########
            if source in BENEFITS.keys():
                BENEFITS[source]+=1
            else:
                BENEFITS[source]=1
                if source not in DAMAGES.keys():
                    DAMAGES[source]=0    
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

    
    T_edges = round (max (1, math.ceil (sum(DAMAGES.values())*(T_percentage/100))))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------                
def BDT_calculator_edge_target (M, Advice, T_percentage):
    BENEFITS, DAMAGES = {}, {}
    for edge in Advice.keys():            
        source, target = edge[0], edge[1]
        if M[source][target]['sign']==Advice[(source, target)]:      #in agreement with the Oracle  
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
            ######### PENALIZING the target node ##########
            if target in DAMAGES.keys():
                DAMAGES[target]+=1
            else:
                DAMAGES[target]=1
                if target not in BENEFITS.keys():
                    BENEFITS[target]=0
            ###############################################
    
    T_edges = round (max (1, math.ceil (sum(DAMAGES.values())*(T_percentage/100))))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------                
def BDT_calculator_edge_both (M, Advice, T_percentage):
    BENEFITS, DAMAGES = {}, {}
    for edge in Advice.keys():            
        source, target = edge[0], edge[1]
        if M[source][target]['sign']==Advice[(source, target)]:      #in agreement with the Oracle
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
            
    T_edges = round (max (1, math.ceil (sum(DAMAGES.values())*(T_percentage/100))))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------
def BDT_calculator_node_source (M, Advice, T_percentage):
    BENEFITS, DAMAGES = {}, {}
    for target in Advice.keys():
        for source in M.predecessors (target):
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
    
    T_edges = round (max (1, math.ceil (sum(DAMAGES.values())*(T_percentage/100))))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------                
def BDT_calculator_node_target (M, Advice, T_percentage):
    BENEFITS, DAMAGES = {}, {}
    for target in Advice.keys():
        for source in M.predecessors (target):
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
    
    T_edges = round (max (1, math.ceil (sum(DAMAGES.values())*(T_percentage/100))))
    
    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
#--------------------------------------------------------------------------------------------------                
def BDT_calculator_node_both (M, Advice, T_percentage):
    BENEFITS, DAMAGES = {}, {}
    for target in Advice.keys():
        for source in M.predecessors (target):
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
    
    T_edges = round (max (1, math.ceil (sum(DAMAGES.values())*(T_percentage/100))))
    
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
#--------------------------------------------------------------------------------------------------
