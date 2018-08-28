import sys,os
from mpi4py import MPI
sys.path.insert(0, os.getenv('lib')) 
import util_plotting as util

comm         = MPI.COMM_WORLD
rank         = comm.Get_rank()
num_workers  = comm.Get_size()-1 #dont counter master
configs_file = util.getCommandLineArg ()


if rank == 0:
    import master_bar3d as master
    master.supervise (configs_file, num_workers)

else:
    import worker_bar3d as worker
    worker.work (configs_file, rank)
