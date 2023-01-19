# A workflow for kymograph processing

### Problems with KymoClear and KymoButler
Typically, .IMS or .TIF files are opened in ImageJ and tracks are marked by the user with the KymoClear plugin. This produces a `/kymograph` directory that contains subdirectories and files that can be a headache when working with lots of samples. Moreover, things get weird if one doesn't segregate their input files into separate directories to start with. Moreover, the resulting kymographs need to be repackaged for quick upload to KymoButler for processing. Finally, the output from KymoButler can be cumbersome to sort through to generate desired graphs of velocity, flux, and so forth. 

### Solutions provided by kbresults
This `kbresults` repo contains three quick functions to address these problems. `filetiffs(path)` simply takes every TIF in `(experiment_directory)` and moves it into its own directory with the same name. Then once the images have been marked with KymoClear, `sortkymos(experiment_directory)` finds all the kymographs in all the subdirectories of the experiment and wraps them into a folder named `/4KymoButler`; this folder can then be compressed into a ZIP file for upload to KymoButler. The kymographs will be named according to the original movie title, plus the numerical suffix applied to the kymograph by KymoClear. 

KymoButler produces an archive of directories and CSV files, organized primarily by sample with no numbering other than the order in which they were processed, and then secondarily by type of data. The `sortkbcsv(experiment_directory, kboutput_directory)` function will take the (unzipped) archive `kboutput_directory` and repackage all the files into `experiment_directory/Results/` subdirectories by data type (velocity, pause times, etc.) with the original names of the kymographs applied to each CSV. **This only works if the 4KymoButler directory is present in the experiment directory and contains all the kymographs in the experiment and no other files.** 

For Python users who like to work with downstream data as a Pandas dataframe (or take one to export to a CSV file), the `summaryframe(experiment_dir, dict_a, dict_b, culture='000000')` function extracts two dataframes from the experiment directory: one with the velocities/intensities/etc. for each individual vesicle and a second that lists the positive and negative flux for each axon. This also numbers the axons from 1 to N per experimental condition, rather than starting over with "axon 1" each time the data come from a new field of view. The `dict_a` and `dict_b` are user-supplied dictionaries currently allowing mapping of the initial character in the filenames to two different experimental variables (for example, treatment with different concentrations of drug A and different concentrations of drug B). The values in those directories become entries in two separate columns in the dataframes that can be indexed in downstreeam analyses. The `culture` variable allows the user to specify an identifier for an experiment such that the dataframe can be concatenated with dataframes from other experiments. 

### Dependencies and conventions
This has been tested with Python 3.6, and requires `pandas`, `os`, `sys`, and `numpy` libraries. Currently there are no error handling measures. The workflow has been tested with a filenaming convention where each starting TIF has at least three characters: the first being a letter denoting the experimental conditions, the second being an integer indicating the field of view (this value is incorporated into a field in the dataframe generated by the `summaryframe` function). The third character of each TIF is copied to a column in the dataframes generated by the `summaryframe` function. **Dictionaries `dict_a` and `dict_b` must be specified to execute the `summaryframe` function.** See the `Examples` folder for a notebook demonstrating all the functions in detail. 
