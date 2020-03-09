import sys,os, subprocess, random
#queue = sys.argv[1]
queue_pop  = os.getenv('HOME')+'/queue.pop'
queue_push = os.getenv('HOME')+'/queue.push'
if not os.path.isfile(queue_pop):
    print ("Couldn't find ~/queue.pop")
else:
    jobs = open (queue_pop,'r').readlines()
    if len(jobs)==0:
        print('There are not jobs to submit (empty qpop?)')
        sys.exit(0)
    #ignore empty lines and lines starting with '#'
    i=0
    while len(jobs[i].strip().replace('\n','')) == 0 or jobs[i][0]=='#':
        jobs=jobs[1:]
        i+=1
    #pop the first line and run it, the rest: re-write them into queue
    if len(jobs)>0:
        print ("subprocess: "+' '.join([arg for arg in jobs[0].split()])) 
        top_job = [arg for arg in jobs[0].split()] + ['>'] + [os.getenv('HOME')+'/job'+str(random.random())]
        result = (subprocess.Popen (top_job, stdout=subprocess.PIPE, universal_newlines=True)).stdout.read()
        print (result)
        rewrite=None
        if not os.path.isfile(queue_push):
            rewrite=open(queue_push,'w')
        else:
            rewrite = open(queue_push,'a')
        rewrite.write(jobs[0])
        remaining= open(queue_pop,'w')
        for line in jobs[1:]:
            remaining.write(line)
    else:
        print ("no more jobs in queue: "+queue_pop)
