"""
	
	Zebrafish

	Python script uses Ensembl REST API to extract 
	one2one, one2many, and many2many orthologs for ENSZs. 

	Makes ensZ2ensC_dict.

"""

import csv
import pickle
import requests, sys, json
from pprint import pprint

### HELPER FUNCTIONS ###

def fetch_endpoint(server, request, content_type):

    r = requests.get(server+request, headers={ "Accept" : content_type})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    if content_type == 'application/json':
        return r.json()
    else:
        return r.text

###

zeb_ciona_orthos_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_all_orthologs/zeb_ciona_orthos.csv"

with open(zeb_ciona_orthos_dir) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=",")

	ensZ2ensC_dict = dict()

	j = 0
	for row in csv_reader:
		ensc = row[0]

		print("j = ", j, ensc, "\n")
		# Defines general URL parameters
		server = "http://rest.ensembl.org/"
		ext_homology = "homology/symbol/danio_rerio/" + ensc + "?target_species=ciona_intestinalis"
		content_type = "application/json" 
		
		# Custom for each ensc
		homology_info = fetch_endpoint(server, ext_homology, content_type)
		# pprint(homology_info)

		data = homology_info["data"]
		homologies_dict = data[0]
		homologies_info = homologies_dict["homologies"]

		if homologies_info == []:
			print("Error!!! with ", ensc)
			break

		# contains ("ortholog_one2many", ENSZ)
		target_info_list = list()

		for i in range(len(homologies_info)):
			homo_dict = homologies_info[i]
			target_type = homo_dict["type"]  
			
			target_dict = homo_dict["target"]
			target_id = target_dict["id"]
			target_info = (target_type, target_id)
			target_info_list.append(target_info)

		ensZ2ensC_dict[ensc] = target_info_list

		j += 1

# pickle
PICKLE_OUT = open("ensZ2ensC_dict.pickle", "wb")
pickle.dump(ensZ2ensC_dict, PICKLE_OUT)
PICKLE_OUT.close()

# ### HELPER FUNCTIONS ###

# def fetch_endpoint(server, request, content_type):

#     r = requests.get(server+request, headers={ "Accept" : content_type})

#     if not r.ok:
#         r.raise_for_status()
#         sys.exit()

#     if content_type == 'application/json':
#         return r.json()
#     else:
#         return r.text

# def get_one_to_one_ortholog(ciona_ENS, homologies_info_2):
# 	"""
# 		If a 1-1 ortholog exists for a given ciona_ENS, function returns
# 		its homologous zeb_ENS, perc_id, and perc_pos.

# 		Args:
# 			ciona_ENS: Ensembl ID of ciona transcript.
# 			homologies_info_2:
# 				-it wasn't empty => ciona_ENS had some kind of ortholog 
# 				-used to make target_dict
# 				-target_dict keys include align_seq, cigar_line, 
# 					id, perc_id, perc_pos...

# 		Returns:
# 			(ortho_id, ortho_perc_id, ortho_perc_pos)


# 	"""
# 	target_dict = homologies_info_2["target"]
# 	ortho_id = target_dict["id"]
# 	ortho_perc_id = target_dict["perc_id"]
# 	ortho_perc_pos = target_dict["perc_pos"]

# 	return (ortho_id, ortho_perc_id, ortho_perc_pos)

# ### TEST ###
# # Make Dictionary of ciona_ENS with 1-1 orthologs
# # {'ENSCING00000000064': ['ENSDARG00000053194', 47.8873, 65.493]

# # ENSCING00000013657 -> (ENSDARG00000070426)
# # ENSCING00000002238 -> (ENSDARG00000054191)
# # "ortholog_one2one"
# one2one_test = ["ENSCING00000013657", "ENSCING00000002238"]

# # ENSCING00000021899 -> (ENSDARG00000036894), (ENSDARG00000060036)
# # ENSCING00000000050 -> (ENSDARG00000004452), (ENSDARG00000040031)
# # ortholog_one2many
# one2many_test = ["ENSCING00000021899", "ENSCING00000000050"]

# # ENSCING00000007267 -> (ENSDARG00000075571), (ENSDARG00000079496), 
# # (ENSDARG00000079934), (ENSDARG00000098215), (ENSDARG00000098551)
# # ENSCING00000013897 -> (ENSDARG00000036041), (ENSDARG00000039579)
# # 'ortholog_many2many'
# many2many_test = ["ENSCING00000007267", "ENSCING00000013897"]

# # one2one_dict = dict()
# # one2many_dict = dict()
# # many2many_dict = dict()

# # j = 0
# # ciona_ENS_list = one2one_test + one2many_test + many2many_test

# ensc2ensz_dict = dict()

# for ciona_ENS in ciona_ENS_list:
# 	print("j = ", j, ciona_ENS, "\n")
# 	# Defines general URL parameters
# 	server = "http://rest.ensembl.org/"
# 	ext_homology = "homology/symbol/ciona_intestinalis/" + ciona_ENS + "?target_species=danio_rerio"
# 	content_type = "application/json"
	
# 	# Custom for each ciona_ENS
# 	homology_info = fetch_endpoint(server, ext_homology, content_type)
# 	# pprint(homology_info)

# 	data = homology_info["data"]
# 	homologies_dict = data[0]
# 	homologies_info = homologies_dict["homologies"]

# 	if homologies_info == []:
# 		print("Error!!! with, " ciona_ENS)
# 		break

# 	# contains ("ortholog_one2many", ENSZ)
# 	target_info_list = list()

# 	for i in range(len(homologies_info)):
# 		homo_dict = homologies_info[i]
# 		target_type = homo_dict["type"]  
		
# 		target_dict = homo_dict["target"]
# 		target_id = target_dict["id"]
# 		target_info = (target_type, target_id)
# 		target_info_list.append(target_info)

# 	ensc2ensz_dict[ciona_ENS] = target_info_list

# 	j += 1





# # 	# there is some kind of ortholog
# # 	if homologies_info != []:
		
# # 		homologies_info_2 = homologies_info[0]

# # 		ortho_type = homologies_info_2["type"]

# # 		if ortho_type == "ortholog_one2one":
# # 			ortho_id, ortho_perc_id, ortho_perc_pos = get_one_to_one_ortholog(ciona_ENS, homologies_info_2)
# # 			correct_ortho_list.append(ciona_ENS)

# # 			one_to_one_ortho_dict[ciona_ENS] = [ortho_id, ortho_perc_id, ortho_perc_pos]
		
# # 		# many-to-many
# # 		else:
# # 			many_ortho_list.append(ciona_ENS)
# # 	# no ortholog
# # 	else:
# # 		unmapped_ortho_list.append(ciona_ENS)

# # 	i +=1 
# # # Pickle the variables

