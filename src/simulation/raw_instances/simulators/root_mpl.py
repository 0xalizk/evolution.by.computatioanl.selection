import multiprocessing
from multiprocessing import Process
import sys,os
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util


num_workers  = multiprocessing.cpu_count() #dont counter master
arguments    = util.getCommandLineArgs ()


if __name__ == "__main__":  
    import master_serial  
    root   = Process(target=master_serial.supervise, args=(arguments, num_workers,))
    root.start()
    root.join()
    print ("root process done")

