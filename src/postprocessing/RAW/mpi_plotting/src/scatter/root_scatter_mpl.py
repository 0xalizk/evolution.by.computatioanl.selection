
import sys,os,time, subprocess as sp
from multiprocessing import Process 
sys.path.insert(0, os.getenv('lib')) 
import util_plotting as util
import master_scatter as master
import worker_scatter as worker


num_workers  = 2 # don't count master
configs_file = util.getCommandLineArg ()


if __name__ == "__main__":

    PROCESSES = []
    
    # master process
    PROCESSES.append(Process(target=master.supervise, args=(configs_file, num_workers,)))
    
    #workers
    for rank in range (1, num_workers+1,1):
        PROCESSES.append(Process(target=worker.work, args= (configs_file, rank, )))


    # spawn them
    for p in PROCESSES:
        p.start()
        time.sleep(1)
    util.myprint ("\n\nroot says: finished spawining master and workers\n")
    
   
