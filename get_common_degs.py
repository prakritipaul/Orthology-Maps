"""

	Script gets commons DEGs between Ciona and Zebrafish.
	                                 (Larva, 24hpf)
	Inputs:
		(1) LOGFC_VAL : Either -1 or 0. 
		(2) results_name: e.g. "one2one_24hpf_larva_khids.csv"
		(3*) Can also change out_dir: e.g. "/home/pprakriti/Desktop/" 


"""

from os import listdir
import pickle
import csv
from pprint import pprint

PICK_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/"
PICK_DIR_2 = "one_to_one_khid_zeb_gene_dict.pickle"
PICK_DIR_3 = "ciona_KHID_to_human_gene_dict.pickle"

ONE2ONE_PICKLE = open(PICK_DIR+PICK_DIR_2, "rb")
ONE2ONE_DICT = pickle.load(ONE2ONE_PICKLE)

KHID_HUMAN_PICKLE = open(PICK_DIR+PICK_DIR_3, "rb")
KHID_HUMAN_DICT = pickle.load(KHID_HUMAN_PICKLE)


"""
	Part 1: Get unique Larva and 24hpf DEGs. 
"""
# Helper Function 

def get_unique_degs(files, logFC_val):
	"""Makes a list of set of DEGs from each tissue and a superset of those DEGs.
	
	Args:
		files: List of filenames.
		e.g. LARVA_FILES = [".../all_larva_DEGs/larva_edgeR_mus.csv"...]

	Returns:
		(master_deg_set_list, unique_deg_set) 
	
	"""
	# Keep track of all degs for each tissue.
	master_deg_set_list = list()
	# Superset of above. 
	unique_deg_set = set()

	for file in files:
		with open(file) as csvfile:
			print("file = ", file)
			csvreader = csv.reader(csvfile, delimiter=",")
			next(csvreader)

			deg_set = set()

			for item in csvreader:
				deg = item[0]
				logFC = float(item[1])
				adj_PValue = float(item[4])

				if logFC <= logFC_val and adj_PValue <= 0.05:
					# Unique DEGs. 
					deg_set.add(deg)
					unique_deg_set.add(deg)

			master_deg_set_list.append(deg_set)

	return (master_deg_set_list, unique_deg_set)


# Global Variables.

## CHANGE ##
LOGFC_VAL = 1
DEG_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/1_CURRENT/one2one_larva_24hpf/"

# Do for Ciona 
LARVA_DIR = "larva_DEGs/"
LARVA_PATH = DEG_DIR+LARVA_DIR  

LARVA_FILES = [LARVA_PATH+f for f in listdir(LARVA_PATH) if ".csv" in f]


# Returns a Set. 
ell, LARVA_UNIQUE_DEGS = get_unique_degs(LARVA_FILES, LOGFC_VAL)


# Do for Zeb
ZEB_DIR = "24hpf_DEGs/"
ZEB_PATH = DEG_DIR+ZEB_DIR

ZEB_FILES = [ZEB_PATH+f for f in listdir(ZEB_PATH) if ".csv" in f]


# Returns a Set. 
zee, ZEB_UNIQUE_DEGS = get_unique_degs(ZEB_FILES, LOGFC_VAL)

"""
	Part 2: Translate khids to zeb genes and get the ones in common.
"""

# Has Ciona DEGs that have 1-1 Orthologs with Zeb 
TSLN_LARVA_DEGS = set()
for khid in LARVA_UNIQUE_DEGS:
	if ONE2ONE_DICT.get(khid) is not None:
		tsln_khid = ONE2ONE_DICT[khid]
		TSLN_LARVA_DEGS.add(tsln_khid)

COMMON_ZEB_DEGS = ZEB_UNIQUE_DEGS & TSLN_LARVA_DEGS

"""
	Part 3: Get names of 1-1 orthologs.
"""

# Helper Function: Get khid given zeb_gene.
def get_khid(your_zeb_deg):
	one2one_items = list(ONE2ONE_DICT.items())

	for one2one_item in one2one_items:
		matched_khid, zeb_gene = one2one_item[0], one2one_item[1]
		if your_zeb_deg == zeb_gene:
			return matched_khid

# Has 1-1 DEG Orthologs in khids. 
ONE2ONE_LARVA_KHID_LIST = list()
ONE2ONE_ZEB_GENE_LIST = list()

for zeb_deg in COMMON_ZEB_DEGS:
	one2one_khid = get_khid(zeb_deg)
	ONE2ONE_LARVA_KHID_LIST.append(one2one_khid)

	ONE2ONE_ZEB_GENE_LIST.append(zeb_deg)


"""
	Part 4: Write out lists to .csv's
"""

LARVA_OUT = [[khid] for khid in ONE2ONE_LARVA_KHID_LIST]
ZEB_OUT = [[tsln_khid] for tsln_khid in ONE2ONE_ZEB_GENE_LIST]


# Helper Function 
def out_csv(results_list, results_name, out_dir):
	"""Takes a list of list of strings and writes them out into a .csv.

	Args: 
		results_list: List of list of strings.
			e.g. [['KH2012:KH.L116.26'], ['KH2012:KH.C14.487']...]
		results_name: Name of .csv
			e.g. "one2one_larva_khids.csv"
		out_dir: Self-explanatory.

	Returns: None. Generates .csv. 

	"""
	final_results_name = out_dir+results_name
	csvfile = open(final_results_name, 'w', newline='')
	obj = csv.writer(csvfile)
	for elem in results_list:
		obj.writerow(elem)

	return None


## CHANGE ## 

# Do for Ciona 
# out_csv(LARVA_OUT, "all_larva_10.csv", "/home/pprakriti/Desktop/")
# # Do for Zeb 
# out_csv(ZEB_OUT, "all_24hpf_10.csv", "/home/pprakriti/Desktop/")

# Print Results
print("\n\n")
print(f"larva unique degs = {len(LARVA_UNIQUE_DEGS)}, 1-1 ciona orthos = {len(TSLN_LARVA_DEGS)}, \
		zeb unique degs = {len(ZEB_UNIQUE_DEGS)}, and common 1-1 DEG orthos = {len(COMMON_ZEB_DEGS)}")
