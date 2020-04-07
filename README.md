# Orthology-Maps
All code relevant to Orthology Maps Thesis Project

1) h5_munging_pipeline
This script was written because the Seurat Read10X_h5 function in Vera was not working, and I needed to manipulate 4D raw matrices. 

-This script is located in /home/pprakriti/Git/Orthology-Maps

** Script Part 1 **
-It reads in h5 files containing raw 4D matrices in Mac using Seurat Read10X_h5.
-These input files are located in "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology Maps/h5_munging/4D_GSE131155_RAW" (this is Vera's path, Mac's path is in code)
-It exports the matrix and its dimnames.
-Chunks of this process are present for earN1 -> midG1.
-These output files are present in "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology Maps/h5_munging/h5_munging_output_files"

** Script 2 **
-Matrix and dimname output files are then read in by Vera and raw matrices are made manually: stage_name and final_matrix_name are manually updated for each stage.

** Notes ** 
-Output files in "manually_done" directory contain output files for iniG1 -> earN1
-Can refer to h5_output_log for order of processing.

2) orthology_maps_data_inputs.Rmd
This script reads in raw data from Schier, Klein, and 4D to create raw matrices (sc-RNA seq count data)

