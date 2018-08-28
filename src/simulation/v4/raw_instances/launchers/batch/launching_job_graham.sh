#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1024M      # memory; default unit is megabytes
#SBATCH --time=0-00:10           # time (DD-HH:MM)

module load gcccore/.5.4.0 
module load openmpi/2.1.1 

cd $SIMULATION_DIRECTORYv4

python3 $LAUNCHING_SCRIPTv4batch $SIMULATION_CONFIGSv4
