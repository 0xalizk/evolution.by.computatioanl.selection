#!/bin/bash
#PBS -l nodes=4:ppn=8 
#PBS -l walltime=000:10:00
#PBS -A ymj-002-aa
#PBS -q short
#  PBS -M mosha5581@gmail.com
#  PBS -m abe

module load compilers/intel/14.0
module load mpi/openmpi/1.6.5
module load libs/mkl/11.1

cd $SIMULATION_DIRECTORY_exec_stats

mpirun --mca mpi_warn_on_fork 0 -n 32 python3 $SIMULATION_SCRIPT_exec_stats $SIMULATION_CONFIGS_exec_stats 
