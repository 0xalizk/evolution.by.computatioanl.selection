#!/bin/bash
#PBS -l procs=1
#PBS -l walltime=00:10:00
#PBS -A ymj-002-aa

module load gcc/4.9.1
module load MKL/11.2
module load openmpi/1.8.3-gcc

echo 'launching python3 '$LAUNCHING_SCRIPTv4batch' '$SIMULATION_CONFIGSv4

cd $LAUNCHING_DIRECTORYv4batch

python3 $LAUNCHING_SCRIPTv4batch $SIMULATION_CONFIGSv4

