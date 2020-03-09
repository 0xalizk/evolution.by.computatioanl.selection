#############################################
How to create a parallel job to plot bar3d:
#############################################

(1) collect all the data_points dir they want to plot and put this in a file called INPUT.txt; example:

        /rap/ymj-002-aa/mosha/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/
        /rap/ymj-002-aa/mosha/Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/
        /rap/ymj-002-aa/mosha/ER_Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_reverse/02_raw_instances_simulation/data_points/
        /rap/ymj-002-aa/mosha/ER_Vinayagam/v4_alpha0.2/v4nu_minknap_4X_both_scramble/02_raw_instances_simulation/data_points/

(2) create a params file called INPUT.params and put the following in it:

        # this line is a comment, comments must be on separate lines
        # a.k.a number of files per pair
        columns            = 4
        file_extension     = svg

        # path to the file in step (1) above
        input_files = /path/to/INPUT.txt 

        stamps = V4XX_BOTH

        output_dir         = /rap/ymj-002-aa/mosha/plotting/bar3d/V4XX
        PLOTTING_ROOT_SCRIPT = /home/mosha/EvoByCompSel/parallel/Release-03/src/postprocessing/RAW/mpi_plotting/src/bar3d/root_bar3d_MPI.py

        # used by launcher.py to determine how many workers needed, in bar3d plots, these four inputs will have the same zlim
        files_per_worker     = 4

        #default = max (30, min(90, num_workers * 3)) 
        walltime=700

(3) submit the job (it takes about ~5 hours per 2-dir pair): 
        MPI:
                python3  /path/to/launcher_plotting.py  /path/to/INPUT.params
        multiprocessing:
                python3 root_bar3d_multiprocessing.py /path/to/INPUT.params
