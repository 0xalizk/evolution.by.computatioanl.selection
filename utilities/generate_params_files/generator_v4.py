#################### IMPORTANT ############## 
# $SCRATCH environment variable must be defined in .bash_profile
#############################################


import sys,os,random,itertools,socket,time
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util
timestamp=time.strftime("%B-%d-%Y-h%Hm%Ms%S")
command_prefix=None
try:
    command_prefix ="python "+os.getenv('LAUNCHING_SCRIPTv4batch')+' '
except:
    command_prefix ="python "+'lscript ??? '
appendex = "\n# comments: \
\n# output_directory   = desired path of directory where to store simulation results. results (along with a copy of this simulation file) will be stored in this dir \
\n# pressure           = [comma seperated percentages of nodes to be subjected to evolutionary pressure] \
\n# tolerance          = [comma seperated percentages of tolerated edges whose signs contradict the oracle advice] \
\n# sampling_threshold = simulations rounds will be the  minimum of sampling_threshold (above) and 2x(no. nodes + no. edges) \
\n# BD_criteria        = [source, target, both] corresponding to the three variations of NEP definition \
\n# KP_solver_source   = absolute path to the knapsack solver source [minknap.c, DP_solver.c] \
\n# KP_solver_binary   = absolute path to the knapsack solver binary [minknap.so, DP_solver.so], source will be compiled here \
\n#                     Note: minknap()   returns [knapsack_value, knapsack_weight(WRONG),   coresize] \
\n#                     DP_solver() returns [knapsack_value, knapsack_weight(CORRECT), number_of_genes n] "

def slash(path):
    return path+(path[-1] != '/')*'/'
def multiply(L,m):
    return L*(int((m/len(L))))

host = '' #socket.gethostname()

settings = {
           	'00version'              : ['v4'],
           	'01reduction_mode'       : ['reverse'],#, 'scramble'],
           	'02sampling_rounds'      : ['1X'],
           	'03sampling_rounds_max'  : [5000],
           	'04pressure'             : [100],#[[0.1, 1, 5, 10, 15, 20, 25, 50, 75, 100]],
           	'05tolerance'            : [[0.1, 1, 5, 10, 15, 25, 50]],#, 75, 100]],
           	'06BD_criteria'          : ['source'],#,'both','target'],
            '07KP_solver_source'     : ['$lib/kp_solvers/DPsolver.c'], #[slash(os.getenv('SOLVERS_DIRECTORY'))+'DPsolver.c'],
            #'07KP_solver_source'     : [slash(os.getenv('SOLVERS_DIRECTORY'))+'minknap.c'],
            '08KP_solver_binary'     : ['$SCRATCH/DPsolver.so'],#[slash(os.getenv('SCRATCH'))+'DPsolver.so'],
            #'08KP_solver_binary'     : [slash(os.getenv('SCRATCH'))+'minknap.so'],
            '09output_directory'     : ['$SCRATCH'],#[slash(os.getenv('SCRATCH'))],
           	'10advice_upon'          : ['nodes','edges'],#['nodes','edges'],
           	'11biased'               : [True,False],#[False,True],
            '12alpha'                :[0.2]
	  }	
edge_files           = []
try:
    edge_files = util.cleanPaths(sys.argv[1]) #open (sys.argv[1], 'r').readlines()
except:
    print ("Usage: python generator_v4.py [absolute path to input file (containing paths to edge files)]")

for f in edge_files:
    if f.strip()[0]=='#':
        continue
    tmp = settings['09output_directory']
    settings['13network_file']     = [f.split('\n')[0].replace( slash(os.getenv('data')), '$data/'  )]
    settings['14network_name']     = [f.split('/')[-1].split('.')[0]]
    settings['09output_directory'] = [slash(settings['09output_directory'][0])+settings['14network_name'][0]+'/'+settings['00version'][0]+'_alpha'+str(settings['12alpha'][0])]
    
    combs = []
    for key in sorted(settings.keys()):
        combs.append(settings[key])
    
    #---------------------------------------
    configs = list(itertools.product(*combs)) # itertools.prodctu() expects lists as arguments
    #---------------------------------------
    relpath = '$HOME/params/'+timestamp+'/'+settings['14network_name'][0]+'/'
    params_dir = slash(str(os.getenv('HOME')))+'params/'+timestamp+'/'+settings['14network_name'][0]+'/'
    os.makedirs(params_dir,exist_ok=True)
    for c in configs:
        #-----v4nb, v4nu, v4eb, v4eu
        v = c[0]+c[10][0]
        if c[11]:
            v = v+'b' 
        elif not c[11]:
            v = v+'u'
        else:
            print ("Fatal: unrecognized value for 'biased': "+c[11])
        #-----v4nb, v4nu, v4eb, v4eu
        out_file = c[14]+"_"+'_'.join((host, c[14],v,'alpha'+str(settings['12alpha'][0]), c[8].split('/')[-1].split('.')[0], c[2], c[6], c[1]))+'.params'
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
        print (relpath+out_file) #(command_prefix+params_dir+out_file)
    settings['09output_directory'] = tmp
    print ("")
    #print (settings['14network_name'][0].ljust(20,'.')+str(len(configs))+' combinations')
