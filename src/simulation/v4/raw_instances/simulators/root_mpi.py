from mpi4py import MPI
import sys,os
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util

comm         = MPI.COMM_WORLD
rank         = comm.Get_rank()
num_workers  = comm.Get_size()-1 #dont counter master
arguments    = util.getCommandLineArgs ()

if rank == 0:   
    with open ('root_mpi.log','w') as f:
        f.write('Im in dir '+str(os.getcwd())+', arguments = '+str(arguments)+ ', num_workers = '+str(num_workers))
        f.flush()
        f.close()
    import master    
    master.supervise (arguments, num_workers)
    
else:
    import worker 
    worker.work (arguments, rank)
#--------------------------------------------------------------------------------------------------
