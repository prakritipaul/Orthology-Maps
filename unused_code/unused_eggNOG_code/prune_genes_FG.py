"""Prunes genes and functional groups, according to Tosches 2018 Method

	Inputs:
		(1) Outputs of 4/24/20 eggNOG run: 
			(a) ciona/zeb protein/pep.all fasta
			(b) Taxonomic Scope=Vertebrates
			(c) Orthology Restrictions=1:1 

"""
import csv

VERA_DIR_STRING = "/home/pprakriti/princeton_google_drive/"
MAC_DIR_STRING = "/Users/prakritipaul/Google Drive (ppaul@princeton.edu)/"

# CIONA_EGGNOG_FILE = VERA_DIR_STRING + "Levine Lab/Orthology-Maps/eggNOG_runs/20_04_24/outputs/ciona20_04_24_ciona_1-1_vert_eggnog_job_MM_qtvhbkz5_annotations.tsv"
# ZEB_EGGNOG_FILE = VERA_DIR_STRING + "Levine Lab/Orthology-Maps/eggNOG_runs/20_04_24/outputs/zeb/20_04_24_zeb_1-1_vert_eggnog_job_MM_kntds0jo_annotations.tsv"


ZEB_EGGNOG_FILE = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/eggNOG_runs/20_04_24/outputs/zeb/20_04_24_zeb_1-1_vert_eggnog_job_MM_kntds0jo_annotations.tsv"
CIONA_EGGNOG_FILE = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/eggNOG_runs/20_04_24/outputs/ciona/ 20_04_24_ciona_1-1_vert_eggnog_job_MM_qtvhbkz5_annotations.tsv"

###############################################################################

with open(ZEB_EGGNOG_FILE, newline="") as eggnog_file:
    eggnog_reader = csv.reader(eggnog_file, delimiter="\t")

    i = 0
    for line in eggnog_reader:
    	print(line, '\n')
    	i += 1
    	if i == 10:
    		break 