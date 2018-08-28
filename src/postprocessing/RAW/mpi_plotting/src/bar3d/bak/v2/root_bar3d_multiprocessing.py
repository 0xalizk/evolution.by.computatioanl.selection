import sys,os,time
from multiprocessing import Process 
sys.path.insert(0, os.getenv('lib')) 
import util_plotting as util
import master_bar3d as master
import worker_bar3d as worker


num_workers  = 1 #dont counter master
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
    print ("\nRoot: finished spawining master and workers")
    
   
