"""

	Given all_ciona_notoXnoto_khids (generated in ciona_notoXnoto.Rmd) and 
	all_zeb_notoXnoto_genes (generated in zeb_notoXnoto.Rmd)- these are khids/zeb_genes
	that are the intersection of genes present in all timepoint matrices.

	Script finds common 1-1 and 1-many orthologs.

	Makes:
	(1) "export_qualified_one2one_many_notoxnoto_dict.csv" 
		"KH2012:KH.C11.313","foxa2 foxa"
		This actually gets used in the notoXnoto pipelines.

	(2) "qualified_one2one_many_notoxnoto_dict.csv"
		"KH2012:KH.C11.313","['foxa2', 'foxa']"
		This does not.

	Notes: 
		1. This code is adapted from get_batch_orthos.py

"""
import csv
import pickle
from pprint import pprint
from collections import defaultdict as dd

						### Import 1-1 and 1-many ortholog dict. ###
PICKLE = open("/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/ciona_converted_ortho_dict.pickle", "rb")
CIONA_CONVERTED_ORTHO_DICT = pickle.load(PICKLE)

									### Import csv's. ###
PARENT_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/1_CURRENT/notoXnoto/"
CIONA_CSV = "all_ciona_notoXnoto_khids.csv"
ZEB_CSV = "all_zeb_notoXnoto_genes.csv"

						### Get Gene Lists for Ciona and Zeb. ### 
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


							### Get 1-1 and 1-many orthologs. ###

# 4636/7578
QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT = dd(list)

for ciona_notoxnoto_gene in ALL_CIONA_NOTOXNOTO_GENES:
	if ciona_notoxnoto_gene in CIONA_CONVERTED_ORTHO_DICT:
		zeb_ortholog_pre_list = CIONA_CONVERTED_ORTHO_DICT.get(ciona_notoxnoto_gene)

		for zeb_ortholog_pre in zeb_ortholog_pre_list:
			zeb_ortholog = zeb_ortholog_pre[1]

			if zeb_ortholog in ALL_ZEB_NOTOXNOTO_GENES:
				QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT[ciona_notoxnoto_gene].append(zeb_ortholog)


								### Write out as csv file ###

								### Routine 2 ###
					### Turn this into an export dict {khid:"zeb_gene_1 zeb_gene_2"} ###

def make_zeb_string(zeb_list):
	zeb_string = " ".join(zeb_list)
	return(zeb_string)

def make_one2one_many_export_dict(one2one_many_export_dict_pre):
	one2one_many_export_dict = dict()

	for khid in one2one_many_export_dict_pre:
		zeb_list = one2one_many_export_dict_pre[khid]
		zeb_string = make_zeb_string(zeb_list)

		one2one_many_export_dict[khid] = zeb_string
		
	return one2one_many_export_dict

EXPORT_QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT = make_one2one_many_export_dict(QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT)

# Write out as .csv.
def make_csv(output_dict, output_dir, output_file_name):	
	with open(output_dir+output_file_name, "w") as csvfile:
	    csvwriter = csv.writer(csvfile)

	    for key, value in output_dict.items():
	        csvwriter.writerow([key, value])
	return None

OUT_DIR = "/home/pprakriti/Desktop/"
OUT_FILE_NAME = "export_qualified_one2one_many_notoxnoto_dict.csv"

make_csv(EXPORT_QUALIFIED_ONE2ONE_MANY_NOTOXNOTO_DICT, OUT_DIR, OUT_FILE_NAME)

