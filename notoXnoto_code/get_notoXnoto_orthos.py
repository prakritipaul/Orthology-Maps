"""

	Given all_ciona_notoXnoto_khids (generated in ciona_notoXnoto.Rmd) and 
	all_zeb_notoXnoto_genes (generated in zeb_notoXnoto.Rmd)- these are khids/zeb_genes
	that are the union of genes present in all timepoint matrices.

	Script finds common 1-1 and 1-many orthologs.

	Notes: 
		1. This code is adapted from get_batch_orthos.py

"""
import csv
import pickle
from pprint import pprint
from collections import defaultdict as dd

# (1) Import 1-1 and 1-many ortholog dict.
PARENT_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/"
FILTERED_DICT_NAME = "filtered_one2one2_many_dict.pickle"
FILTERED_DICT_DIR = PARENT_DIR+FILTERED_DICT_NAME

FILTERED_ONE2ONE2_MANY_PICKLE = open(FILTERED_DICT_DIR, "rb")
FILTERED_ONE2ONE2_MANY_DICT = pickle.load(FILTERED_ONE2ONE2_MANY_PICKLE)


# (2) Import csv's.
PARENT_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/1_CURRENT/notoXnoto/"
CIONA_CSV = "all_ciona_notoXnoto_khids.csv"
ZEB_CSV = "all_zeb_notoXnoto_genes.csv"


# (3) Get Gene Lists for Ciona and Zeb. 
# Helper Function
def get_gene_list(YOUR_DIR, to_print=False):
	# Get all genes in csvile (khids/zeb_genes)
	gene_list = list()
	
	with open(YOUR_DIR) as csvfile:
		csvreader = csv.reader(csvfile, delimiter=",")

		for elem in csvreader:
			gene = elem[0]
			gene_list.append(gene)

			if to_print:
				print(elem)

	return(gene_list)

# Inputs.
CIONA_GENES_CSV = PARENT_DIR+CIONA_CSV
ZEB_GENES_CSV = PARENT_DIR+ZEB_CSV

# Outputs. 
ALL_CIONA_NOTOXNOTO_GENES = get_gene_list(CIONA_GENES_CSV)
ALL_ZEB_NOTOXNOTO_GENES = get_gene_list(ZEB_GENES_CSV)

# (4) Get 1-1 and 1-many orthologs.
# 2995/3140
QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT = dict()
# 401 khids present in Ciona noto matrices but do not have orthologs 
# with zeb_genes in Zeb noto matrices.  
UNQUALIFIED_KHIDS = list()

# Perfom the Routine. 

for khid in ALL_CIONA_NOTOXNOTO_GENES:
	if khid in FILTERED_ONE2ONE2_MANY_DICT:
		tsln_khids = FILTERED_ONE2ONE2_MANY_DICT[khid]

		if any(tsln_khid in ALL_ZEB_NOTOXNOTO_GENES for tsln_khid in tsln_khids):
			QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT[khid] = tsln_khids
		else:
			# These genes have zeb orthologs, but the zeb orthologs 
			# are not present in Zeb noto matrices.
			UNQUALIFIED_KHIDS.append(khid)
	else:
		UNQUALIFIED_KHIDS.append(khid)
		print("Not in filtered dict = ", khid, "\n")


# QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT



# Make lists.


# Perform Routine

# Export as... 