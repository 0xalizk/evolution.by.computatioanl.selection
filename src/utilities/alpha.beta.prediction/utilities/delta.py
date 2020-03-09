import sys,os,time, subprocess as sp,numpy as np
from multiprocessing import Process

sys.path.insert(0, os.getenv('lib'))
import fitting_lib
unambiguity_score = fitting_lib.unambiguity_score
######################################################################
def absolute_delta(NETS): # difference area under the curve

    for key in list(NETS.keys()):
        DELTA = None

        for n2e in [x/100 for x in range(1,101,1)]:
            for e2n in [x/10 for x in range(1,101,1)]:
                delta = 0
                for d,f in zip(NETS[key]['deg'], NETS[key]['freq']) :
                    ##################################
                    delta += abs(f - unambiguity_score(d,n2e,e2n))
                    ##################################
                if DELTA != None:
                    if delta < DELTA[2]:
                        DELTA = (n2e,e2n,delta)
                else:
                    DELTA = (n2e,e2n,delta)

        print (('\''+key+'\':').ljust(20,' ')+ str([DELTA[0],DELTA[1], (1-DELTA[2])*100]).ljust(15,' ') + '\t#accuracy = '+str((1-DELTA[2])*100))
######################################################################
def relative_delta(NETS): # find the fit that generates most accurate node prediction (as a % nodes)

    for key in list(NETS.keys()):

        DELTA = None

        for n2e in [x/100 for x in range(1,101,1)]:
            for e2n in [x/10 for x in range(1,101,1)]:
                delta = 0
                for d,f in zip(NETS[key]['deg'], NETS[key]['freq']) :
                    #######################################
                    predict = unambiguity_score(d,n2e,e2n)
                    delta  += (abs(f - predict)/f)*NETS[key]['nodes']
                    #######################################
                if DELTA != None:
                    #################################
                    delta = delta/NETS[key]['nodes']
                    if delta < DELTA[2]:
                    #################################
                        DELTA = (n2e,e2n,delta)
                else:
                    DELTA = (n2e,e2n,delta)

        print (('\''+key+'\':').ljust(20,' ')+ str([DELTA[0],DELTA[1]]).ljust(15,' ') + 'accuracy = '+str((1-DELTA[2])*100))
######################################################################
######################################################################
if __name__ == '__main__':

    NETS = fitting_lib.networks

    eval = absolute_delta
    print('='*20+' absolute '+'='*20)
    #eval  = relative_delta
    #print('='*20+' relative '+'='*20)

    # a single network; default all networks
    if len(sys.argv) > 1:
        if sys.argv[1].strip() in NETS.keys():
            NETS = {sys.argv[1].strip():NETS[sys.argv[1].strip()]}


    PROCESSES = []
    KEYS = list([key for key in NETS.keys()]) #if key!='Human_orig' and key!='Human'])
    for rank in range (0, len(KEYS),1):
        PROCESSES.append(Process(target=eval, args= ({KEYS[rank]:NETS[KEYS[rank]]}, )))

    # spawn them
    for p in PROCESSES:
        p.start()
    running = len(PROCESSES)
    #print ("root says: watching processes\n\n")
    sleep = True
    while len(PROCESSES)>0:
        if sleep:
            time.sleep(10)
        else:
            sleep = True
        for i in range(len(PROCESSES)):
            if not PROCESSES[i].is_alive():
                PROCESSES[i].terminate()
                del PROCESSES[i]
                #print('root says: terminated a process; remaining processes =  '+str(len(PROCESSES)))
                sleep = False
                break
    print ("root says: done, all processes have terminated. Goodbye!\n\n")
