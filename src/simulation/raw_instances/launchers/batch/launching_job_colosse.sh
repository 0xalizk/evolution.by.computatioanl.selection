#!/bin/bash
#PBS -l nodes=1:ppn=8 
#PBS -l walltime=00:10:00
#PBS -A ymj-002-aa
#PBS -M mosha5581@gmail.com
# PBS -m abe
#PBS -q test

module load compilers/intel/14.0
module load mpi/openmpi/1.6.5
module load libs/mkl/11.1

echo 'launching python3 '$LAUNCHING_SCRIPTv4batch' '$SIMULATION_CONFIGSv4

cd $LAUNCHING_DIRECTORYv4batch

python3 $LAUNCHING_SCRIPTv4batch $SIMULATION_CONFIGSv4

