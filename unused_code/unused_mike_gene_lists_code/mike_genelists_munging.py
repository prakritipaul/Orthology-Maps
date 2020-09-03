"""

	Script just munges names for convenience.

"""

import csv
import pickle

general_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/"
ciona_dir = general_dir + "ciona_ENS_to_KHID_dict.pickle"
zeb_dir = general_dir + "zeb_ens_to_gene_dict.pickle"

ciona_pickle = open(ciona_dir, "rb")
ciona_dict = pickle.load(ciona_pickle)

zeb_pickle = open(zeb_dir, "rb")
zeb_dict = pickle.load(zeb_pickle)

#####

# 'KH2012:KH.C3.100'
c_mesp_ens = "ENSCING00000012702"

# lol these are the zeb gene names 
z_mespaa_ens = "ENSDARG00000017078"
z_mespba_ens = "ENSDARG00000068761"
z_mespbab_ens = "ENSDARG00000030347"
z_mespbb_ens = "ENSDARG00000097947"
z_msgn1_ens = "ENSDARG00000070546"

z_mesp_list = [z_mespaa_ens, z_mespba_ens, z_mespbab_ens, z_mespbb_ens, z_msgn1_ens]

c_mesp = ciona_dict[c_mesp_ens]

for z_mesp in z_mesp_list:
	print(zeb_dict[z_mesp])
