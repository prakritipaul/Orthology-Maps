"""

	This script is an adaptation of "get_common_degs.py". 
	Inputs: DEGs from 1 Ciona and 1 Zeb CT. 
	Output: Lists of 1-1 DEG orthologs between those 2 CELL TYPES.

	"get_common_degs.py" was designed to find common 1-1 DEGs 
	between entire Ciona and Zeb embryos. 

	What you can change:
		1. LOGFC = [-1, 0] where -1 = 2fold change.
		2. LARVA/ZEB_PATH
		3. outcsv (names of csv's that contain common DEGs)

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

def get_unique_degs(file, logFC_val):
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

	print("line 1", file, "\n\n")

	with open(file) as csvfile:
		print("line 2 file = ", file, "\n\n")
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
LOGFC_VAL = -1

DEG_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/1_CURRENT/one2one_larva_24hpf/"

# Do for Ciona 
LARVA_DIR = "larva_DEGs/"

## CHANGE ##
LARVA_CSV = "larva_edgeR_noto.csv"
LARVA_FILE = DEG_DIR + LARVA_DIR + LARVA_CSV 

# Returns a Set (size 1). 
ell, LARVA_UNIQUE_DEGS = get_unique_degs(LARVA_FILE, LOGFC_VAL)


# Do for Zeb
ZEB_DIR = "24hpf_DEGs/"

## CHANGE ##
ZEB_CSV = "edgeR_noto.csv"
ZEB_FILE = DEG_DIR + ZEB_DIR + ZEB_CSV

# Returns a Set (size 1).  
zee, ZEB_UNIQUE_DEGS = get_unique_degs(ZEB_FILE, LOGFC_VAL)


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

# "larva_heart_24hpf_2hearts_DEG_logFC0_khids.csv"
# "larva_heart_24hpf_2hearts_DEG_logFC0_zebgenes.csv"

# # Do for Ciona 
# out_csv(LARVA_OUT, "larva_noto_24hpf_noto_DEG_logFC0_khids.csv", "/home/pprakriti/Desktop/")
# # Do for Zeb 
# out_csv(ZEB_OUT, "larva_noto_24hpf_noto_DEG_logFC0_zebgenes.csv", "/home/pprakriti/Desktop/")

# Print Results
print("\n\n")
print(f"larva unique degs = {len(LARVA_UNIQUE_DEGS)} zeb unique degs = {len(ZEB_UNIQUE_DEGS)} \
		1-1 ciona orthos = {len(TSLN_LARVA_DEGS)}, and common 1-1 DEG orthos = {len(COMMON_ZEB_DEGS)}")

print("\n\n")
for item in ONE2ONE_LARVA_KHID_LIST:
	print(item, "= ", KHID_HUMAN_DICT[item])