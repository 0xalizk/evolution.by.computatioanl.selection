result = open('root.txt').readlines()[5:-3]
for line in result:
    n = [float(n) for n in line.strip().split()]
    diff = abs(n[0]-n[-1])
    if diff > 2:
        print ('oh oh\t'+str(diff).ljust(25,' ')+str(n[0]))
