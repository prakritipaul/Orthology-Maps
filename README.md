# Orthology-Maps
All code relevant to Orthology Maps Thesis Project

(1) UNUSED: h5_munging_pipeline
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

***

Order of Scripts 

"""
Part 1: Initial clustering, tissue mapping, cell name curation, and DEG calculations

"""

(1) orthology_maps_data_inputs.Rmd
This script reads in raw data from Schier, Klein, and 4D and creates dataframes for each. Ultimately, Klein 24hpf and Levine Larva data is used.

(2a_1) zeb_24hpf_clustering.Rmd
-Maps all tissues using Wagner's DEGs in zeb_integrated_50 Seurat Object.

(2a_2) zeb_degs_heatmaps.Rmd
-Gets cells from all clusters from above.
-Calculates top50 DEGs for each cell type.
-Validates clusters by comparing first 20 top50 DEGs with Wagner DEGs. 

(2b) ciona_larvae_clustering.Rmd
-Maps all tissues.
-Gets cells from all clusters.
-Uses clean_chen_larvae_integrated_20 Seurat Object.

"""
Part 2: Attempts to create gene sets.

"""
(3) get_pairwise_zeb_ciona_degs.Rmd
(1) Module v1: Tosches Method
-Makes unique_ciona_deg_vec (444) and unique_zeb_deg_vec (1372)
NOTE: ZEB DEG CALCULATION TOOK 3 HOURS TO RUN!

(4) (munging code directory) 
-unique_ciona_deg_vec (444) and unique_zeb_deg_vec (1372) are manipulated in "get_one_to_one_gene_lists.py" to make ciona_ortho_KHID_vec and zeb_ortho_gene_vec (which are then used for visualization in get_pairwise_zeb_ciona_degs.Rmd)
	

"""
munging_code directory 

"""

(1) make_*_*_to_dict.py
-self-explanatory 

(2) ensembl_get_one_to_one_orthologs.py
-Makes one_to_one_ortho_dict (2993)
-correct, unmapped, many lists.
-Also makes ciona_ENS_to_KHID_dict here 

TO DO: Make many_many list
NOTE: THIS TOOK 3 HOURS TO RUN!

(3) get_one_to_one_gene_lists.py
-Uses above dictionaries, unique_ciona_deg_vec, unique_zeb_deg_vec
 to make ciona_khid_list (6) and zeb_gene list (6), which are copy/pasted back into get_pairwise_zeb_ciona_degs.Rmd as ciona_ortho_KHID_vec and zeb_ortho_gene_vec.




