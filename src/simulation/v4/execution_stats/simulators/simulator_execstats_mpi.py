from mpi4py import MPI
import sys,os
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util

comm         = MPI.COMM_WORLD
rank         = comm.Get_rank()
num_workers  = comm.Get_size()-1 #dont counter master
arguments    = util.getCommandLineArgs ()

if rank == 0:   
    import master_mpi as master   
    master.supervise (arguments, num_workers)
    
else:
    import worker 
    worker.work (arguments, rank)
#--------------------------------------------------------------------------------------------------
