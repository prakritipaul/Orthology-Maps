"""

Script classifies 1-1 orthologs based on perc_pos

http://may2012.archive.ensembl.org/info/docs/api/compara/compara_schema.html

"""
import pickle
from collections import defaultdict

pickle_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/"
my_pickle_dir = pickle_dir + "one_to_one_ortho_dict.pickle"

pickle_in = open(my_pickle_dir, "rb")
one_to_one_ortho_dict = pickle.load(pickle_in)

id_10 = list()
id_20 = list()
id_30 = list()
id_40 = list()
id_50 = list()
id_60 = list()
id_70 = list()
id_80 = list()
id_90 = list()
id_100 = list()

def get_bin_id(perc_id):
	if perc_id <= 10:
		id_10.append(perc_id)

	if perc_id <= 20:
		id_20.append(perc_id)

	if perc_id <= 30:
		id_30.append(perc_id)

	if perc_id <= 40:
		id_40.append(perc_id)

	if perc_id <= 50:
		id_50.append(perc_id)

	if perc_id <= 60:
		id_60.append(perc_id)

	if perc_id <= 70:
		id_70.append(perc_id)

	if perc_id <= 80:
		id_80.append(perc_id)	

	if perc_id <= 90:
		id_90.append(perc_id)

	if perc_id <= 100:
		id_100.append(perc_id)

###

pos_10 = list()
pos_20 = list()
pos_30 = list()
pos_40 = list()
pos_50 = list()
pos_60 = list()
pos_70 = list()
pos_80 = list()
pos_90 = list()
pos_100 = list()

def get_bin_pos(perc_pos):
	if perc_pos <= 10:
		pos_10.append(perc_pos)

	if perc_pos <= 20:
		pos_20.append(perc_pos)

	if perc_pos <= 30:
		pos_30.append(perc_pos)

	if perc_pos <= 40:
		pos_40.append(perc_pos)

	if perc_pos <= 50:
		pos_50.append(perc_pos)

	if perc_pos <= 60:
		pos_60.append(perc_pos)

	if perc_pos <= 70:
		pos_70.append(perc_pos)

	if perc_pos <= 80:
		pos_80.append(perc_pos)	

	if perc_pos <= 90:
		pos_90.append(perc_pos)

	if perc_pos <= 100:
		pos_100.append(perc_pos)


###
def pipeline():
	for ensc in one_to_one_ortho_dict:
		perc_id = one_to_one_ortho_dict[ensc][1]
		get_bin_id(perc_id) 

		perc_pos = one_to_one_ortho_dict[ensc][2]
		get_bin_pos(perc_pos)


pipeline()





