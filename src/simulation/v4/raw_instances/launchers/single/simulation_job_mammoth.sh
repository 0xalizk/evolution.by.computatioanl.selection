#!/bin/bash
#PBS -l nodes=2:ppn=1 
#PBS -l walltime=08:00:00
#PBS -l pmem=4gb
#PBS -q qfbb
#PBS -A ymj-002-aa
#   PBS -M mosha5581@gmail.com
#   PBS -m e

module unload intel64/12.0.5.220
module unload pgi64/11.10
module unload pathscale/4.0.12.1
module load intel64/13.1.3.192
module load pathscale/5.0.5
module load pgi64/12.5
module load openmpi_intel64/1.6.5

cd $SIMULATION_DIRECTORYv4

mpirun --mca mpi_warn_on_fork 0 -n 48 python3 $SIMULATION_SCRIPTv4 $SIMULATION_CONFIGSv4
