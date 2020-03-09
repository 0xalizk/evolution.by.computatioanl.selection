from multiprocessing import Process
import sys,os
sys.path.insert(0, os.getenv('lib'))
import utilv4 as util


num_workers  = 20 #dont counter master
arguments    = util.getCommandLineArgs ()


if __name__ == "__main__":  
    import master_mpl as master 
    root   = Process(target=master.supervise, args=(arguments, num_workers,))
    root.start()
    root.join()
    print ("\n\nroot process done")

