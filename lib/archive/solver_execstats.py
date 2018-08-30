from ctypes import c_int, c_double
from time import process_time as ptime
#--------------------------------------------------------------------------------------------------
def solve_knapsack (kp_instance, knapsack_solver):    
    #kp_instance is a tuple: (  {"gene":benefit},  {"gene":damage},  knapsack_size(=tolerance)   )
    B_dict, D_dict, T_edges, N  = kp_instance[0][0], kp_instance[0][1], kp_instance[0][2], len(kp_instance[0][0].keys())
    
    assert (N==len(B_dict)==len(D_dict))
    if N == 0:
        return []
    else:        
        grey_genes       = [key for key in B_dict.keys() if (B_dict[key]>0 and D_dict[key] > 0) ]
        num_white_genes  = len([key for key in B_dict.keys() if (B_dict[key]>0 and D_dict[key]==0) ])
        num_black_genes  = len([key for key in B_dict.keys() if B_dict[key]==0])
        num_grey_genes   = len(grey_genes) 
        assert (len(grey_genes) + num_white_genes + num_black_genes) == len (B_dict.keys())
        N = len (grey_genes)      
        
        B, D, F, solver_returns1, solver_returns2, i =  (c_int*N)(),  (c_int*N)(), (c_int*N)(),  (c_int*3)(), (c_double*2)(), 0
        for key in grey_genes:            
            B[i], D[i], i = B_dict[key], D_dict[key], i+1
        #---------------------------------------------------------------------    
        t0 = ptime()
        knapsack_solver.solve (B, D, T_edges, N, F, solver_returns1, solver_returns2)   # WARNING: minknap.so does not return the correct knapsack weight (solver_returns[1])                          
        t1 = ptime() - t0
        #---------------------------------------------------------------------
        TOTAL_Bin, TOTAL_Din, TOTAL_Bou, TOTAL_Dou = 0, 0, 0, 0
        for g in range (0, N):
            assert (F[g] == 0) or (F[g] == 1) #TODO: remove assert
            if F[g] == 1:
                TOTAL_Bin += B[g]
                TOTAL_Din += D[g]
            else:
                TOTAL_Bou += B[g]
                TOTAL_Dou += D[g]
        assert TOTAL_Bin == solver_returns1[0]
        
        return [num_white_genes, num_black_genes, num_grey_genes, TOTAL_Bin, TOTAL_Din, TOTAL_Bou, TOTAL_Dou, solver_returns1[2], solver_returns2[0], solver_returns2[1], t1]
        #       num_white_genes, num_black_genes, num_grey_genes, TOTAL_Bin, TOTAL_Din, TOTAL_Bou, TOTAL_Dou, core_size,          Ctime_s, Ctime_ms, PythonTime
        '''
        
        solver_returns1[0] => knapsack_total_value
        solver_returns1[1] => knapsack_total_weight = # WARNING: minknap.so does not return the correct knapsack weight (maybe it's return the original capacity; if you need it re-calculate based on solution vector F)  
        solver_returns1[2] => coresize # if DP_solver.so is used,  coresize = len (grey_genes)      
        solver_returns2[3] => execution_time_s
        solver_returns2[3] => execution_time_ms
        t1                 => python's time calculation (try t0.resolution to see precision, it's nanoseconds i think (10E-9), see: https://docs.python.org/3.5/library/time.html#time.get_clock_info
        
        '''