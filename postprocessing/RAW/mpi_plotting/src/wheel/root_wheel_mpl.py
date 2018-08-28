
import sys,os,time, subprocess as sp
from multiprocessing import Process 
sys.path.insert(0, os.getenv('lib')) 
import util_plotting as util
import master_wheel as master
import worker_wheel as worker

myprint      = util.myprint
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
    running = len(PROCESSES)
    myprint ("\n\nroot says: watching processes\n\n")
    sleep = True
    while len(PROCESSES)>0:
        if sleep:
            time.sleep(60)
        else:
            sleep = True
        for i in range(len(PROCESSES)):
            if not PROCESSES[i].is_alive():
                PROCESSES[i].terminate()
                del PROCESSES[i]
                myprint('\nroot says: terminated a process; remaining processes =  '+str(len(PROCESSES)))
                sleep = False
                break
    myprint ("\n\nroot says: done, all processes have terminated. Goodbye!\n\n")
    

