#!/bin/bash
#PBS -l procs=32
#PBS -l walltime=01:00:00
#PBS -A ymj-002-aa

module load gcc/4.9.1
module load MKL/11.2
module load openmpi/1.8.3-gcc

echo 'simulating: python '$SIMULATION_BATCH_ROOT' 32 '$SIMULATION_CONFIGSv4

cd $SIMULATION_DIRECTORYv4

python $SIMULATION_BATCH_ROOT 32 $SIMULATION_CONFIGSv4
