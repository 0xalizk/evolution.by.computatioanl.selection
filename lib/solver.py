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
        grey_genes   = [key for key in B_dict.keys() if (B_dict[key]>0 and D_dict[key] > 0) ]
        white_genes  = [key for key in B_dict.keys() if (B_dict[key]>0 and D_dict[key]==0) ]
        black_genes  = [key for key in B_dict.keys() if B_dict[key]==0]
        assert (len(grey_genes)+len(white_genes)+len(black_genes)) == len (B_dict.keys())
        N = len (grey_genes)      
        
        G, B, D, F, solver_returns1, solver_returns2, i = ['' for x in range(0,N)], (c_int*N)(),  (c_int*N)(), (c_int*N)(),  (c_int*3)(), (c_double*2)(), 0
        for key in grey_genes:            
            G[i], B[i], D[i], i = key, B_dict[key], D_dict[key], i+1
        #---------------------------------------------------------------------    
        t0 = ptime()
        knapsack_solver.solve (B, D, T_edges, N, F, solver_returns1, solver_returns2)   # WARNING: minknap.so does not return the correct knapsack weight (solver_returns[1])                          
        t1 = ptime() - t0
        #---------------------------------------------------------------------
        TOTAL_Bin, TOTAL_Din, TOTAL_Bout, TOTAL_Dout, GENES_in, GENES_out = 0, 0, 0, 0, [], []
        for g in range (0, N):
            assert (F[g] == 0) or (F[g] == 1) #TODO: remove assert
            if F[g] == 1:                               
                TOTAL_Bin += B[g]
                TOTAL_Din += D[g]
                GENES_in.append ((G[g], B[g], D[g]))  
            else:
                TOTAL_Bout += B[g]
                TOTAL_Dout += D[g]
                GENES_out.append ((G[g], B[g], D[g]))

        #assert (TOTAL_Bin == solver_returns [0]) and (TOTAL_Din == solver_returns [1]) and ((len(GENES_out)+len(GENES_in)) == len(G) == len (F) == N) #TODO: remove assert
        assert (TOTAL_Bin == solver_returns1 [0]) and ((len(GENES_out)+len(GENES_in)) == len(G) == len (F) == N)

        for key in white_genes: # white_genes are automatically in knapsack
            TOTAL_Bin += B_dict[key]
            GENES_in.append((key, B_dict[key], D_dict[key]))
        for key in black_genes: # black_genes are automatically outside knapsack
            TOTAL_Dout += D_dict[key]
            GENES_out.append((key, B_dict[key], D_dict[key]))
      
        return {
                    'TOTAL_Bin':TOTAL_Bin, 
                    'TOTAL_Din':TOTAL_Din, 
                    'TOTAL_Bout':TOTAL_Bout, 
                    'TOTAL_Dout':TOTAL_Dout, 
                    'GENES_in':GENES_in, 
                    'GENES_out':GENES_out, 
                    'white_genes':white_genes, 
                    'black_genes':black_genes, 
                    'grey_genes':grey_genes, 
                    'execution_stats': {'coresize':solver_returns1[2], 'Ctime_s':solver_returns2[0], 'Ctime_ms':solver_returns2[1], 'PythonTime_s':t1}
               }
