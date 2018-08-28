#!/bin/bash
#SBATCH --ntasks=32               # number of MPI processes
#SBATCH --mem-per-cpu=4096M      # memory; default unit is megabytes
#SBATCH --time=0-01:00           # time (DD-HH:MM)


module load gcccore/.5.4.0 
module load openmpi/2.1.1

echo 'simulating: python '$SIMULATION_BATCH_ROOT' 32 '$SIMULATION_CONFIGSv4
cd $SIMULATION_DIRECTORYv4

python $SIMULATION_BATCH_ROOT 32 $SIMULATION_CONFIGSv4
