#!/bin/bash
#PBS -l nodes=1:ppn=8 
#PBS -l walltime=00:10:00
#PBS -A ymj-002-aa
#PBS -M mosha5581@gmail.com
#PBS -q short

module load compilers/intel/14.0
module load mpi/openmpi/1.6.5
module load libs/mkl/11.1

cd $LAUNCHING_DIRECTORYv4

python3 $LAUNCHING_SCRIPTv4 $SIMULATION_CONFIGSv4


