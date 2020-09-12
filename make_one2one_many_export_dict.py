"""

	From CZ_CONVERTED_DICT {khid: ["ortholog_one2many", ["m_zeb_gene_1"... "m_zeb_gene_n"],
							khid: ["ortholog_one2one", ["o_zeb_gene"]...},
	
	We want both 1-1 and 1-many orthologs.

	Makes: 
	(1) one2one_many_export_dict_pre {khid: ["m_zeb_gene_1", "m_zeb_gene_2" ... "m_zeb_gene_n],
									  khid: ["o_zeb_gene"] ...}

			 {'KH2012:KH.S811.3': ['ap1g1', 
			 					   'ap1g2'],

              'KH2012:KH.S815.1': ['zranb2'], 
              ...}


	(2a) one2one_many_export_dict {khid: "m_zeb_gene_1 m_zeb_gene_2 ... m_zeb_gene_n",
								  khid: "o_zeb_gene" ...}
	The value is one string with names of zeb genes separated by whitespace. 
	Let's call it zeb_gene_string

	This dict is then exported as a csv file in which the khid and zeb_gene_string 
	are comma delimited.

	(2b) filtered_one2one_many_export_dict
		 Contains genes present only in all.ciona/zeb.genes, which are genes
		 present in gene models used in "one2many_orthology_map_generator.Rmd"

	Relevant Variables:
		1) CZ_CONVERTED_DICT
		2) ALL_CIONA_GENES
		3) ALL_ZEB_GENES
"""

import pickle
import csv
from pprint import pprint
from collections import defaultdict

PICK_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/"
PICK_DIR_2 = "ciona_converted_ortho_dict.pickle"

CZ_CONVERTED_PICKLE = open(PICK_DIR+PICK_DIR_2, "rb")
CZ_CONVERTED_DICT = pickle.load(CZ_CONVERTED_PICKLE)

# all.ciona/zeb.genes
ciona_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/1_CURRENT/one2one_many_larva_24hpf/all_ciona_genes.csv"
zeb_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/1_CURRENT/one2one_many_larva_24hpf/all_zeb_genes.csv"

# Lists of above.
# 14433
ALL_CIONA_GENES = list()

with open(ciona_dir) as csvfile:
	csvreader = csv.reader(csvfile, delimiter=",")
	for elem in csvreader:
		khid = elem[0]
		ALL_CIONA_GENES.append(khid)

# 30677
ALL_ZEB_GENES = list()

with open(zeb_dir) as csvfile:
	csvreader = csv.reader(csvfile, delimiter=",")
	for elem in csvreader:
		zeb_gene = elem[0]
		ALL_ZEB_GENES.append(zeb_gene)

# Helper functions
def make_one2one_many_export_dict_pre():
	one2one_many_export_dict_pre = defaultdict(list)

	for khid in CZ_CONVERTED_DICT:
		ortho_type = CZ_CONVERTED_DICT[khid][0][0]	

		if ortho_type == "ortholog_one2one":
			ortho_gene = CZ_CONVERTED_DICT[khid][0][1]
			one2one_many_export_dict_pre[khid].append(ortho_gene)

		if ortho_type == "ortholog_one2many":
			ortho_info = CZ_CONVERTED_DICT[khid]

			for info in ortho_info:
				ortho_gene = info[1]
				one2one_many_export_dict_pre[khid].append(ortho_gene) 

	return one2one_many_export_dict_pre

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

def make_csv(output_dict, output_dir, output_file_name):	
	with open(output_dir+output_file_name, "w") as csvfile:
	    csvwriter = csv.writer(csvfile)

	    for key, value in output_dict.items():
	        csvwriter.writerow([key, value])
	return None

def self_many(khid):
	# Checks if there are many mappings to a khid (self many). 
	ortho_info = CZ_CONVERTED_DICT[khid]
	ortho_type = ortho_info[0][0]
	return len(ortho_info) == 1 and ortho_type == 'ortholog_one2many'



if __name__ == "__main__":
	
	# Dict to be modified downstream.
	ONE2ONE_MANY_EXPORT_DICT_PRE = make_one2one_many_export_dict_pre()
	
	###

	# Make one2one_many_export_dict.
	ONE2ONE_MANY_EXPORT_DICT = make_one2one_many_export_dict(ONE2ONE_MANY_EXPORT_DICT_PRE)

	OUTPUT_DICT = ONE2ONE_MANY_EXPORT_DICT
	OUTPUT_DIR = "/home/pprakriti/Desktop/"
	OUTPUT_FILE_NAME = "one2one_many_export_dict.csv"

	# make_csv(OUTPUT_DICT, OUTPUT_DIR, OUTPUT_FILE_NAME)

	###

	# Post Ciona Filtering. 
	FILTERED_ONE2ONE_MANY_EXPORT_DICT = dict()
	# Post Zeb Filtering -> Final dict. 
	FILTERED_ONE2ONE_MANY_EXPORT_DICT_2 = dict()

	self_list = list()
	# Ciona Self-Many and Genome Model Filtered.
	for khid in ONE2ONE_MANY_EXPORT_DICT_PRE:
		# Remove Self-Many. 
		if self_many(khid):
			print("self many ", khid)
			self_list.append(khid)

		# Make sure it is in Genome Model.
		if khid in ALL_CIONA_GENES and not self_many(khid):
			FILTERED_ONE2ONE_MANY_EXPORT_DICT[khid] = list(set(ONE2ONE_MANY_EXPORT_DICT_PRE[khid]))
	
	# Zeb Genome Model Filtered.
	for khid in FILTERED_ONE2ONE_MANY_EXPORT_DICT:
		zeb_genes = FILTERED_ONE2ONE_MANY_EXPORT_DICT[khid]
		# Ensure that all zeb orthologs (1-1 and 1-many) are in Genome Model.
		if all(zeb_gene in ALL_ZEB_GENES for zeb_gene in zeb_genes):
			FILTERED_ONE2ONE_MANY_EXPORT_DICT_2[khid] = list(set(FILTERED_ONE2ONE_MANY_EXPORT_DICT[khid]))

	# Start Sanity Checks #

	zeb_count = 0
	# Can be a set with unique zeb_genes.
	zeb_gene_list = list()

	for khid in FILTERED_ONE2ONE_MANY_EXPORT_DICT_2:
		# Check that khid is in Ciona Genome Model.
		if khid not in ALL_CIONA_GENES: 
			print(f"khid = {khid} not in CIONA GENES")
			break
		
		# Go through all of khid's zeb orthologs.
		zeb_info = FILTERED_ONE2ONE_MANY_EXPORT_DICT[khid]

		for zeb_gene in zeb_info:
			# Check zeb_genes are in Ciona Zebrafish Model.
			if zeb_gene not in ALL_ZEB_GENES:
				print(f"zeb gene = {zeb_gene} not in ZEB GENES")
				break

			# We only want unique zeb genes. O.w. this implies self-many.
			if zeb_gene in zeb_gene_list:
				print(f"problem! zeb gene = {zeb_gene} was seen")
				break
	
			else:
				zeb_gene_list.append(zeb_gene)
				zeb_count += 1

	# Both should be the same number. 
	print("Number of khids = ", len(FILTERED_ONE2ONE_MANY_EXPORT_DICT_2.keys()), "\n")
	print("Number of unique khids = ", len(set(FILTERED_ONE2ONE_MANY_EXPORT_DICT_2.keys())))
	
	# How many zeb genes got counted.
	print("zeb count = ", zeb_count)

	print("Are all in ciona?")
	print(all(khid in ALL_CIONA_GENES for khid in FILTERED_ONE2ONE_MANY_EXPORT_DICT_2.keys()), "\n")
	
	print("\n Are all in zeb?")
	print(all(zeb_gene in ALL_ZEB_GENES for zeb_gene in zeb_gene_list))

	# Make sure there aren't any zeb gene repeats In FILTERED DICT 2 (final dict).
	# Length of this should be = zeb_count
	unique_zeb_ortho_list = list()
	# Should be 0. 
	seen_zeb_ortho_list = list()

	for khid in FILTERED_ONE2ONE_MANY_EXPORT_DICT_2:
		zeb_orthos = FILTERED_ONE2ONE_MANY_EXPORT_DICT_2[khid]

		if any(zeb_ortho in unique_zeb_ortho_list for zeb_ortho in zeb_orthos):
			seen_zeb_ortho_list.append((khid, zeb_orthos))

		else:
			for zeb_ortho in zeb_orthos:
				unique_zeb_ortho_list.append(zeb_ortho)

	# Keeps track of number of 1-1 orthologs.
	one_count = 0
	for khid in FILTERED_ONE2ONE_MANY_EXPORT_DICT_2:
		zeb_info = FILTERED_ONE2ONE_MANY_EXPORT_DICT_2[khid]
		if len(zeb_info) == 1:
			one_count += 1

	print("Number of 1-1 orthologs = ", one_count, "1-many ", len(FILTERED_ONE2ONE_MANY_EXPORT_DICT_2)-one_count)

	# Make sure there are only 1-1 or 1-many orthologs.
	incorrect_ortholog_list = list()

	for khid in FILTERED_ONE2ONE_MANY_EXPORT_DICT_2:
		ortho_type = CZ_CONVERTED_DICT[khid][0][0]
		if ortho_type not in ["ortholog_one2one", "ortholog_one2many"]:
			print("Error!")
			incorrect_ortholog_list.append(khid)



	# End Sanity Checks #

	FILTERED_ONE2ONE_MANY_EXPORT_DICT = make_one2one_many_export_dict(FILTERED_ONE2ONE_MANY_EXPORT_DICT_2)
	
	OUTPUT_DICT_2 = FILTERED_ONE2ONE_MANY_EXPORT_DICT
	OUTPUT_DIR_2 = "/home/pprakriti/Desktop/"
	OUTPUT_FILE_NAME_2 = "filtered_one2one_many_export_dict_20_09_07.csv"

	# 9/7/20
	make_csv(OUTPUT_DICT_2, OUTPUT_DIR_2, OUTPUT_FILE_NAME_2)
