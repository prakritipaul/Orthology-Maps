"""

	Pipeline to get 1-1 Ciona and Zeb orthologs.
		(1) 36 Ciona DEGs have 1-1 Orthologs.
		(2) 68 Zeb DEGs have 1-1 Orthologs.
		(3) Only 6 1-1 Orthologs are in common.

	Notes:
		(1) Unique Ciona and Zeb DEGs were generated from 
			v1 module of "get_pairwise_zeb_ciona_degs.Rmd". 
		(2) Refer to mona_meeting_20_06_05.pptx for pipeline details.

"""
import csv
import pickle

###########  Get Dictionaries ###########

PICK_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/gene_set_analyses/pickles/"
ZEB_ENS_TO_GENE_DICT_DIR = PICK_DIR + "zeb_ens_to_gene_dict.pickle"
ONE_TO_ONE_ORTHO_DICT_DIR = PICK_DIR + "one_to_one_ortho_dict.pickle"
CIONA_ENS_TO_KHID_DICT_DIR = PICK_DIR + "ciona_ENS_to_KHID_dict.pickle"
CIONA_KHID_TO_ENS_DICT_DIR = PICK_DIR + "ciona_KHID_to_ENS_dict.pickle"
CIONA_KHID_TO_GENE_DICT_DIR = PICK_DIR + "ciona_KHID_to_gene_dict.pickle"

PICKLE_1 = open(ZEB_ENS_TO_GENE_DICT_DIR, "rb")
PICKLE_2 = open(ONE_TO_ONE_ORTHO_DICT_DIR, "rb")
PICKLE_3 = open(CIONA_ENS_TO_KHID_DICT_DIR, "rb")
PICKLE_4 = open(CIONA_KHID_TO_ENS_DICT_DIR, "rb")
PICKLE_5 = open(CIONA_KHID_TO_GENE_DICT_DIR, "rb")

ZEB_ENS_TO_GENE_DICT = pickle.load(PICKLE_1)
ONE_TO_ONE_ORTHO_DICT = pickle.load(PICKLE_2)
CIONA_ENS_TO_KHID_DICT = pickle.load(PICKLE_3)
CIONA_KHID_TO_ENS_DICT = pickle.load(PICKLE_4)
CIONA_KHID_TO_GENE_DICT = pickle.load(PICKLE_5)


###########  Get DEG Sets  ###########

ENS_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/gene_set_analyses/"
UNIQUE_CIONA_ENS_DIR = ENS_DIR + "unique_ciona_deg_vec.csv"
UNIQUE_ZEB_ENS_DIR = ENS_DIR + "unique_zeb_deg_vec.csv"

# Ciona (444)
UNIQUE_CIONA_KHID_DEG_SET = set()

with open(UNIQUE_CIONA_ENS_DIR) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter="\t")

	for row in csv_reader:
		UNIQUE_CIONA_KHID_DEG_SET.add(row[0])

# Zeb (1372)
UNIQUE_ZEB_GENE_DEG_SET = set()

with open(UNIQUE_ZEB_ENS_DIR) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter="\t")

	for row in csv_reader:
		UNIQUE_ZEB_GENE_DEG_SET.add(row[0])


###########  Get Sets of "Qualified" Genes (1-1 Orthologs)  ###########

# 30
ciona_ortho_KHID_list = list()
ciona_ortho_ENS_list = list()

for ciona_ENS in ONE_TO_ONE_ORTHO_DICT:
	# get ciona_KHID
	ciona_KHID = CIONA_ENS_TO_KHID_DICT[ciona_ENS]
	munged_ciona_KHID = "KH2012:" + ciona_KHID

	if munged_ciona_KHID in UNIQUE_CIONA_KHID_DEG_SET:
		ciona_ortho_KHID_list.append(munged_ciona_KHID)
		ciona_ortho_ENS_list.append(ciona_ENS)

# Helper function to get ENSZ from gene name.
def get_zeb_ens(my_zeb_gene): 
	for zeb_ens, zeb_gene in ZEB_ENS_TO_GENE_DICT.items(): 
		if my_zeb_gene == zeb_gene: 
			return zeb_ens 

# All 1-1 ENSZ.
all_ortho_zeb_ens_list = [item[0] for item in ONE_TO_ONE_ORTHO_DICT.values()]

# 68
zeb_ortho_gene_list = list()
zeb_ortho_ens_list = list()

for zeb_gene in UNIQUE_ZEB_GENE_DEG_SET:
	zeb_ens = get_zeb_ens(zeb_gene)
	if zeb_ens in all_ortho_zeb_ens_list:
		zeb_ortho_gene_list.append(zeb_gene)
		zeb_ortho_ens_list.append(zeb_ens)

# Convert 1-1 ENSC to ENSZ.
ciona_ortho_ENS_to_zeb_ENS_list = [ONE_TO_ONE_ORTHO_DICT[item][0] for item in ciona_ortho_ENS_list]

# Only 6 
common_one_to_one_zeb_ens = set(ciona_ortho_ENS_to_zeb_ENS_list) & set(zeb_ortho_ens_list)

# Helper function to get ENSC from ENSZ.
def get_ciona_ens(my_zeb_ens):
	for ciona_ens, zeb_ens in ONE_TO_ONE_ORTHO_DICT.items():
		real_zeb_ens = zeb_ens[0]
		if my_zeb_ens == real_zeb_ens: 
			return ciona_ens 

# Matching 1-1 KHID and gene names from above. 
ciona_khid_list = list()
zeb_gene_list = list()

for zeb_ens in common_one_to_one_zeb_ens:
	zeb_gene = ZEB_ENS_TO_GENE_DICT[zeb_ens]
	zeb_gene_list.append(zeb_gene)

	print("zeb ens = ", zeb_ens)
	ciona_ens = get_ciona_ens(zeb_ens)
	print("ciona_ens = ", ciona_ens)
	ciona_khid = CIONA_ENS_TO_KHID_DICT[ciona_ens]
	ciona_khid_list.append(ciona_khid)

