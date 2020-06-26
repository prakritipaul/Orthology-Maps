# Scratch 
# Just trying to get the KHIDs of zeb genes 

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

###

zeb_gene_list_dir = "/home/pprakriti/Desktop/test_one_one_var_feats_zeb.csv"

###
# Get ensd's
ensd_list = list()

def get_key(your_value, your_dict):
	for key in your_dict:
		if your_dict[key] == your_value:
			return key


with open(zeb_gene_list_dir) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=",")
	for zeb_gene_pre in csv_reader:
		zeb_gene = zeb_gene_pre[0]
		# print(zeb_gene)
		ensd = get_key(zeb_gene, ZEB_ENS_TO_GENE_DICT)
		ensd_list.append(ensd)

###
# Get ensc's that correspond to these ensd's
ensc_list = list()

for ensc in ONE_TO_ONE_ORTHO_DICT:
	for ensd in ensd_list:
		if ONE_TO_ONE_ORTHO_DICT[ensc][0] == ensd:
			ensc_list.append(ensc)

# Now we want to know the KHIDs of ensc's in ensc_list
khid_list = list()

for ensc in ensc_list:
	khid = CIONA_ENS_TO_KHID_DICT[ensc]
	# print("khid = ", khid)
	khid_list.append(khid)


results = [["KH2012:"+khid] for khid in khid_list]

results_name = "scratch_khid_ortho_list.csv"
csvfile = open(results_name, 'w', newline='')
obj = csv.writer(csvfile)
for elem in results:
	obj.writerow(elem)

csvfile.close()

###

# What are the corresponding gene names for these KHIDs?

test_yes_ciona_dir = "/home/pprakriti/Desktop/test_yes_khid.csv"

# Get rid of 
zeb_gene_list = list()

with open(test_yes_ciona_dir) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=",")
	for khid_pre in csv_reader:
		khid = khid_pre[0]
		khid_munged = khid.split(":")[1]
		print(khid_munged)

		ensc = CIONA_KHID_TO_ENS_DICT[khid_munged][0]
		print(ensc)
		ensd = ONE_TO_ONE_ORTHO_DICT[ensc][0]
		print(ensd)
		zeb_gene = ZEB_ENS_TO_GENE_DICT[ensd]
		zeb_gene_list.append(zeb_gene)


results = [[zeb_gene] for zeb_gene in zeb_gene_list]

results_name = "scratch_25_zeb_gene_list.csv"
csvfile = open(results_name, 'w', newline='')
obj = csv.writer(csvfile)
for elem in results:
	obj.writerow(elem)

csvfile.close()

		
