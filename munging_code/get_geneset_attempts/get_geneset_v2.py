"""
	Unused. 
	
	Module v2: Do we get signal if we use all orthologous genes?

	Notes:
		1) The outputs of this script were used in Module v2 section in
		  "get_gene_set_troubleshooting.Rmd". 
		2) 25 genes were identified.
		3) However, these genes were not 1-1 orthologs.

"""
import csv
import pickle

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

##########

# Get KHIDs for all ENSC_orthos

all_khid_ortho_list = list()

for ensc_ortho in ONE_TO_ONE_ORTHO_DICT:
	khid_ortho = CIONA_ENS_TO_KHID_DICT[ensc_ortho]
	all_khid_ortho_list.append(khid_ortho)

results = [["KH2012:"+khid_ortho] for khid_ortho in all_khid_ortho_list]

results_name = "all_khid_ortho_list.csv"
csvfile = open(results_name, 'w', newline='')
obj = csv.writer(csvfile)
for elem in results:
	obj.writerow(elem)

csvfile.close()

#########

# Get gene names for all ENSD_orthos

all_zeb_gene_ortho_list = list()

for ensc_ortho in ONE_TO_ONE_ORTHO_DICT:
	ensd_ortho = ONE_TO_ONE_ORTHO_DICT[ensc_ortho][0]
	zeb_gene_ortho = ZEB_ENS_TO_GENE_DICT[ensd_ortho]
	all_zeb_gene_ortho_list.append(zeb_gene_ortho)


results = [[zeb_gene_ortho] for zeb_gene_ortho in all_zeb_gene_ortho_list]

results_name = "all_zeb_gene_ortho_list.csv"
csvfile = open(results_name, 'w', newline='')
obj = csv.writer(csvfile)
for elem in results:
	obj.writerow(elem)

csvfile.close()
	

