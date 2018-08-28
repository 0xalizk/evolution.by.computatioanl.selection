#################### IMPORTANT ############## 
# $SCRATCH environment variable must be defined in .bash_profile
#############################################


import sys,os,random,itertools,socket
command_prefix ="python /home/mosha/EvoByCompSel/parallel/Release-03/src/simulation/efficiency/launchers/efficiency_launcher.py "
appendex = "\n# comments: \
\n# mode               = [serial | parallel] default: serial \
\n# output_directory     = desired path of directory where to store simulation results. results (along with a copy of this simulation file) will be stored in this dir \
\n# pressure           = [comma seperated percentages of nodes to be subjected to evolutionary pressure] \
\n# tolerance          = [comma seperated percentages of tolerated edges whose signs contradict the oracle advice] \
\n# sampling_threshold = simulations rounds will be the  minimum of sampling_threshold (above) and 2x(no. nodes + no. edges) \
\n# BD_criteria        = [source, target, both] corresponding to the three variations of NEP definition \
\n# KP_solver_source   = absolute path to the knapsack solver source [minknap.c, DP_solver.c] \
\n# KP_solver_binary   = absolute path to the knapsack solver binary [minknap.so, DP_solver.so], source will be compiled here \
\n#                                               Note: minknap()   returns [knapsack_value, knapsack_weight(WRONG),   coresize] \
\n#                                                     DP_solver() returns [knapsack_value, knapsack_weight(CORRECT), number_of_genes n] "

def slash(path):
    return path+(path[-1] != '/')*'/'
def multiply(L,m):
    return L*(int((m/len(L))))
#host =  os.getenv('HOSTNAME')
host = socket.gethostname()
#KP_solver_source    =slash(os.getenv('SOLVERS_DIRECTORY'))+'DP_solver.c'
#KP_solver_binary    =slash(os.getenv('SCRATCH'))+'DP_solver.so'
settings = {
           	'00version'              : ['v3'],
           	'01reduction_mode'       : ['reverse', 'scramble'],
           	'02sampling_rounds'      : ['2X'],
           	'03sampling_rounds_max'  : [30000],
           	'04pressure'             : [[0.1, 1, 5, 10, 15, 20, 25, 50, 75, 100]],
           	'05tolerance'            : [[0.1, 1, 5, 10, 15, 20, 25, 50, 75, 100]],
           	'06BD_criteria'          : ['both','source','target'],
           	'07KP_solver_source'     : [slash(os.getenv('SOLVERS_DIRECTORY'))+'minknap.c'],
           	'08KP_solver_binary'     : [slash(os.getenv('SCRATCH'))+'minknap.so'],
           	'09output_directory'     : [slash(os.getenv('SCRATCH'))]
	  }	
edge_files           = []
try:
    edge_files = open (sys.argv[1], 'r').readlines()
except:
    print ("Usage: python generator.py [absolute path to input file (containing paths to edge files)]")

for f in edge_files:
    tmp = settings['09output_directory']
    settings['10network_file']     = [f.split('\n')[0]]
    settings['11network_name']     = [f.split('/')[-1].split('.')[0]]
    settings['09output_directory'] = [slash(settings['09output_directory'][0])+settings['11network_name'][0]+'/'+settings['00version'][0]]
    
    combs = []
    for key in sorted(settings.keys()):
        combs.append(settings[key])
    
    #---------------------------------------
    configs = list(itertools.product(*combs)) # itertools.prodctu() expects lists as arguments
    #---------------------------------------
    params_dir = slash(str(os.getenv('HOME')))+'params/'+settings['11network_name'][0]+'/'
    os.makedirs(params_dir,exist_ok=True)
    for c in configs:
        out_file = c[11]+"_"+'_'.join((host, c[11],c[0], c[8].split('/')[-1].split('.')[0], c[2], c[6], c[1]))+'.params'
        out = open (params_dir+out_file,'w' )
        i=0
        clean_keys = []
        for key in sorted(settings.keys()):
            clean_keys.append (''.join([i for i in key if  i.isalpha() or i=='_']))     
        for p in clean_keys:
            if isinstance (c[i], list):
                out.write(p.ljust(25, ' ')+'= '+','.join([str(e) for e in c[i]])+'\n')
            else:
                out.write(p.ljust(25, ' ')+'= '+str(c[i])+'\n')
            i+=1
        out.write(appendex)
        print (command_prefix+params_dir+out_file)
    settings['09output_directory'] = tmp
    print (settings['11network_name'][0].ljust(20,'.')+str(len(configs))+' combinations')
