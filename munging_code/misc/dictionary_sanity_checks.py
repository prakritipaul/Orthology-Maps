"""
	
	Exploring the various dictionaries that I have- sanity checks.

"""
import csv
import pickle

pick_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/gene_set_analyses/pickles/"
zeb_ens_to_gene_dict_dir = pick_dir + "zeb_ens_to_gene_dict.pickle"
one_to_one_ortho_dict_dir = pick_dir + "one_to_one_ortho_dict.pickle"
ciona_ens_to_khid_dict_dir = pick_dir + "ciona_ENS_to_KHID_dict.pickle"
ciona_khid_to_ens_dict_dir = pick_dir + "ciona_KHID_to_ENS_dict.pickle"
ciona_khid_to_gene_dict_dir = pick_dir + "ciona_KHID_to_gene_dict.pickle"

unmapped_dir = pick_dir + "unmapped_ortho_list.pickle"
many_dir = pick_dir + "many_ortho_list.pickle"
correct_dir = pick_dir + "correct_ortho_list.pickle"

pickle_1 = open(zeb_ens_to_gene_dict_dir, "rb")

pickle_2 = open(one_to_one_ortho_dict_dir, "rb")
pickle_3 = open(ciona_ens_to_khid_dict_dir, "rb")
pickle_4 = open(ciona_khid_to_ens_dict_dir, "rb")
pickle_5 = open(ciona_khid_to_gene_dict_dir, "rb")

pickle_6 = open(unmapped_dir, "rb")
pickle_7 = open(many_dir, "rb")
pickle_8 = open(correct_dir, "rb")

# 37241
zeb_ens_to_gene_dict = pickle.load(pickle_1)
# 
one_to_one_ortho_dict = pickle.load(pickle_2)
# 13007
ciona_ens_to_khid_dict = pickle.load(pickle_3)

ciona_khid_to_ens_dict = pickle.load(pickle_4)

ciona_khid_to_gene_dict = pickle.load(pickle_5)

unmapped_list = pickle.load(pickle_6)

many_list = pickle.load(pickle_7)

correct_list = pickle.load(pickle_8) 

ens_dir = "/home/pprakriti/princeton_google_drive/levine lab/orthology-maps/gene_set_analyses/"
unique_ciona_ens_dir = ens_dir + "unique_ciona_deg_vec.csv"
unique_zeb_ens_dir = ens_dir + "unique_zeb_deg_vec.csv"

