# Evolution by Computational Selection

This repository contains all the sources code and datasets for: 
1. Running the Network Evolution Problem (NEP) simulations
2. Processing visualizing the resulting simulation data
3. Running utility scripts such as network stats, generating random analog networks. 

Detailed instruction for 1/2/3 above are included under `src/simulation`, `src/postprocessing` and `src/utilities`.

-----

## Overview 

The principle of "Evolution by Computational Selection" relates to the idea that just as natural selection as optimized for better hardware (think: size of girraf's heart, insect skin colour (camouflage), allometry of a lion's jaw, etc), it has also optimized for better "software" in the the manner in which the connectivity of genes (which gene interacts with which). People with computer science background are familiar with the idea that if every object is interacting with every other an an OOP paradignm, the resulting software can't be maintained and is is destined for collapse under its own chaotic weight at some point. Similar organization manifest in biological networks: the topology of such networks is one rather guranatees high maintainability. Maintenance in the context of evolutionary biology is carried out through the process of random variation and non-random selection. The simulation here generate hypothetical evolutionary pressure scenario and assesses the difficulty of maintenance (computational cost, characterized by how many generation will it take before the network has been sufficiently wired away from a bad situation).

-----

## Requirements
1. Python 3.5+
2. gcc 5.4.0+ 
3. matplotlib, numpy, scipy, and pandas
4. Optional: mpi4py if parallelizing with MPI (cluster high-power computing environment). If running on a single multi-core machines use \*\_serial.py scripts instead, all cores will automatically be utilized.

## Quick start

1. simulation: `python3 src/simulation/raw_instances/ROOT.py [_path_to_configs.txt]`. Note: if running on a cluster refer to your scheduler's documentation for how to submit a job. ROOT.py will automatically detect the available cores from the environment variable (see `src/simulation/raw_instances/launchers/` for example launching scripts).

2. postprocessing: `python3 src/postprocessing/RAW/mpi_plotting/crunchNplot/root.py [_path_to_plotting_config.txt]`. See example config.txt files under `src/postprocessing/RAW/mpi_plotting/crunchNplot/`

3. utilities: most utility functions either take a config.txt file as argument or a direct link to a network dataset (e.g. network stats). Each utility contains example input files in the same directory.

## Advanced simulations:

For running the simulation against very large networks (e.g. ENCODE), the data is only meaningful if multiple rounds of sampling is conducted (we did 1K+ in our work, and found that increasing it further does not add much value, see the Central Limit Theorem as to why that is the case). To do that, parallelization is necessary, because each round of simulation (which involves the generation and solving an instance of the NP-Hard NEP problem) takes some time. The core algorithm running in the simulation is a knapsack dynamic-programming solver written in C, which must be compiled in advance (an included binary is under `lib/kp_solvers directory`). 

The quickest way to get started on running the simulation on the cluster is to edit the example qsub submission scripts found under `src/simulation/raw_instances/launchers` and adapt it to your environment. For help please email atiia [at] cs [dot] mcgill [dot] ca.

## References:

The literature references for this work are still being considered for publication but can be provided upon request, email: atiia [at] cs [dot] mcgill [dot] ca.Further documentation can also be found under /doc directory 
