#!/bin/bash
#PBS -l procs=32
#PBS -l walltime=01:00:00
#PBS -A ymj-002-aa

module load gcc/4.9.1
module load MKL/11.2
module load openmpi/1.8.3-gcc

cd $SIMULATION_DIRECTORYv4

mpirun --mca mpi_warn_on_fork 0 -n 32 python3 $SIMULATION_SCRIPTv4 $SIMULATION_CONFIGSv4
