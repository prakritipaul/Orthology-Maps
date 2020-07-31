"""

	Makes KHID:gene name for 1-1 orthologs.
	(ONE_TO_ONE_KHID_GENE_NAME_DICT)  

"""


import csv
import pickle

PICK_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_geneset_attempts/pickles/"
ZEB_ENS_TO_GENE_DICT_DIR = PICK_DIR + "zeb_ens_to_gene_dict.pickle"
ONE_TO_ONE_ORTHO_DICT_DIR = PICK_DIR + "one_to_one_ortho_dict.pickle"
CIONA_ENS_TO_KHID_DICT_DIR = PICK_DIR + "ciona_ENS_to_KHID_dict.pickle"
CIONA_KHID_TO_ENS_DICT_DIR = PICK_DIR + "ciona_KHID_to_ENS_dict.pickle"
# These are human genes!
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

ONE_TO_ONE_KHID_ZEB_GENE_DICT = dict()

seen_khids = set()

for ensc in ONE_TO_ONE_ORTHO_DICT:
	khid = CIONA_ENS_TO_KHID_DICT[ensc]
	if khid in seen_khids:
		print(f"khid {khid} with ensc = {ensc} seen!")
	else:
		seen_khids.add(khid)
	khid_munged = "KH2012:" + khid
	ensz = ONE_TO_ONE_ORTHO_DICT[ensc][0]
	gene_name = ZEB_ENS_TO_GENE_DICT[ensz]
	# print(f"khid_munged = {khid_munged}, ensz = {ensz}, gene_name = {gene_name}")

	ONE_TO_ONE_KHID_ZEB_GENE_DICT[khid_munged] = gene_name

###

# Pickle

OUT_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_geneset_attempts/pickles/"
PICKLE_OUT = open(OUT_DIR + "one_to_one_khid_zeb_gene_dict.pickle", "wb")
pickle.dump(ONE_TO_ONE_KHID_ZEB_GENE_DICT, PICKLE_OUT)
PICKLE_OUT.close()
