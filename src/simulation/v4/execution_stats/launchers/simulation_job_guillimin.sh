#!/bin/bash
#PBS -l procs=32
#PBS -l walltime=00:90:00
#PBS -A ymj-002-aa

module load gcc/4.9.1
module load MKL/11.2
module load openmpi/1.8.3-gcc

cd $SIMULATION_DIRECTORY_exec_stats

mpirun --mca mpi_warn_on_fork 0 -n 32 python3 $SIMULATION_SCRIPT_exec_stats $SIMULATION_CONFIGS_exec_stats
