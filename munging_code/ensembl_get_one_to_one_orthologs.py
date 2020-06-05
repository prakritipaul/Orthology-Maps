"""

	Python script uses Ensembl REST API to extract 
	1-1 zeb orthologs for all Ciona genes.

	Makes 3 lists (*_ortho_list):
		(1) correct: ENSC with 1-1 zeb orthologs.
		(2) unmapped: ENSC with no ortholog information.
		(3) many: ENSC with 1-many orthologs.

	Also makes ciona_ENS_to_KHID_dict.

	TO DO:
		(1) Also find ENSC with many-many orthologs.

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

def get_one_to_one_ortholog(ciona_ENS, homologies_info_2):
	"""
		If a 1-1 ortholog exists for a given ciona_ENS, function returns
		its homologous zeb_ENS, perc_id, and perc_pos.

		Args:
			ciona_ENS: Ensembl ID of ciona transcript.
			homologies_info_2:
				-it wasn't empty => ciona_ENS had some kind of ortholog 
				-used to make target_dict
				-target_dict keys include align_seq, cigar_line, 
					id, perc_id, perc_pos...

		Returns:
			(ortho_id, ortho_perc_id, ortho_perc_pos)


	"""
	target_dict = homologies_info_2["target"]
	ortho_id = target_dict["id"]
	ortho_perc_id = target_dict["perc_id"]
	ortho_perc_pos = target_dict["perc_pos"]

	return (ortho_id, ortho_perc_id, ortho_perc_pos)

### TEST ###

if __name__ == "__main__":

	# Make a dictionary that maps Ciona ENS transcript IDs to KHIDs
	ciona_ENS_to_KHID_dict = dict()
	ciona_ENS_list = ciona_ENS_to_KHID_dict.keys()

	ciona_ens_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/lifechanging_aniseed_files/correspondanceENSEMBL_KH.txt"
	with open(ciona_ens_dir) as ciona_ens_file:

		csv_reader = csv.reader(ciona_ens_file, delimiter="\t")

		for row in csv_reader:
			ciona_ENS = row[0]
			ciona_KHID = row[1]

			ciona_ENS_to_KHID_dict[ciona_ENS] = ciona_KHID


	### Run the pipeline ###
	# keep track of various ciona_ENS
	correct_ortho_list = list()
	unmapped_ortho_list = list()
	many_ortho_list = list()

	# Make Dictionary of ciona_ENS with 1-1 orthologs
	# {'ENSCING00000000064': ['ENSDARG00000053194', 47.8873, 65.493]
	one_to_one_ortho_dict = dict()

	i = 0
	for ciona_ENS in ciona_ENS_list:
		print("i = ", i, "\n")
		# Defines general URL parameters
		server = "http://rest.ensembl.org/"
		ext_homology = "homology/symbol/ciona_intestinalis/" + ciona_ENS + "?target_species=danio_rerio"
		content_type = "application/json"
		
		# Custom for each ciona_ENS
		homology_info = fetch_endpoint(server, ext_homology, content_type)

		data = homology_info["data"]

		homologies_dict = data[0]
		
		homologies_info = homologies_dict["homologies"]

		# there is some kind of ortholog
		if homologies_info != []:
			
			homologies_info_2 = homologies_info[0]

			ortho_type = homologies_info_2["type"]

			if ortho_type == "ortholog_one2one":
				ortho_id, ortho_perc_id, ortho_perc_pos = get_one_to_one_ortholog(ciona_ENS, homologies_info_2)
				correct_ortho_list.append(ciona_ENS)

				one_to_one_ortho_dict[ciona_ENS] = [ortho_id, ortho_perc_id, ortho_perc_pos]
			
			# many-to-many
			else:
				many_ortho_list.append(ciona_ENS)
		# no ortholog
		else:
			unmapped_ortho_list.append(ciona_ENS)

		i +=1 
	# Pickle the variables

	PICKLE_OUT = open("one_to_one_ortho_dict.pickle", "wb")
	pickle.dump(one_to_one_ortho_dict, PICKLE_OUT)
	PICKLE_OUT.close()

	PICKLE_OUT = open("ciona_ENS_to_KHID_dict.pickle", "wb")
	pickle.dump(ciona_ENS_to_KHID_dict, PICKLE_OUT)
	PICKLE_OUT.close()

	PICKLE_OUT = open("correct_ortho_list.pickle", "wb")
	pickle.dump(correct_ortho_list, PICKLE_OUT)
	PICKLE_OUT.close()

	PICKLE_OUT = open("unmapped_ortho_list.pickle", "wb")
	pickle.dump(unmapped_ortho_list, PICKLE_OUT)
	PICKLE_OUT.close()

	PICKLE_OUT = open("many_ortho_list.pickle", "wb")
	pickle.dump(many_ortho_list, PICKLE_OUT)
	PICKLE_OUT.close()
