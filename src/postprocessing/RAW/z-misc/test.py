import socket, math
if __name__ == "__main__":
    num_pairs = 49 
    submission_script = open ("test.sh", 'w')
    host              = ''.join([i for i in socket.gethostname() if not i.isdigit()])
    if "ip" in host or "cp" in host: #mammoth
        print ("We are on Mammoth, eh!")

        nodes      = max(1, math.ceil(float(num_pairs)/24))
        submission_script.write("#!/bin/bash")
        submission_script.write("\n#PBS -l nodes="+str(nodes)+":ppn=1")
        submission_script.write("\n#PBS -l walltime=00:45:00")
        submission_script.write("\n#PBS -A ymj-002-aa")
        submission_script.write("\nmodule unload intel64/12.0.5.220\nmodule unload pgi64/11.10\nmodule unload pathscale/4.0.12.1\nmodule load intel64/13.1.3.192\nmodule load pathscale/5.0.5\nmodule load pgi64/12.5\nmodule load openmpi_intel64/1.6.5\n")
        submission_script.write("mpirun --mca mpi_warn_on_fork 0 -n"+str(nodes*24)+" python3 master.py configs_file.txt")

