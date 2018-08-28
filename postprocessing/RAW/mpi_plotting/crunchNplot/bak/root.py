import sys,os,time, subprocess as sp
from multiprocessing import Process 
sys.path.insert(0, os.getenv('lib')) 
import util_plotting as util
import master_plotter
import master_cruncher

################################################
myprint      = util.myprint
configs_file = util.getCommandLineArg ()
num_workers = 4 # don't count master
################################################
def this_is_an_MPI_environment():
	try:
		from mpi4py import MPI
		comm         = MPI.COMM_WORLD
		rank         = comm.Get_rank()    
		if comm.Get_size() <=1: # switch to mpl, either we're not in MPI environment or we are running on only one cpu
			return False
		else:
		    return True
	except:
		return False
	return True
################################################
if this_is_an_MPI_environment():
	if rank == 0:
		master_plotter.supervise (configs_file, num_workers)
	else:
		master_cruncher.crunch (configs_file, rank)
else:	
	PROCESSES = []

	# master process
	PROCESSES.append(Process(target=master_plotter.supervise, args=(configs_file, num_workers,)))

	#workers
	for rank in range (1, num_workers+1,1):
		PROCESSES.append(Process(target=master_cruncher.crunch, args= (configs_file, rank, )))

	# spawn them
	for p in PROCESSES:
		p.start()
		time.sleep(1)
	running = len(PROCESSES)
	myprint ("\n\nroot says: watching processes\n\n")
	sleep = True
	while len(PROCESSES)>0:
		if sleep:
			time.sleep(30)
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
