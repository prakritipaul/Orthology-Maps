"""
	Ciona

	Python script uses Ensembl REST API to extract 
	one2one, one2many, and many2many orthologs for ENSCs. 

	Makes ensC2ensZ_dict.

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

ciona_zeb_orthos_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_all_orthologs/ciona_zeb_orthos.csv"

with open(ciona_zeb_orthos_dir) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=",")

	ensC2ensZ_dict = dict()

	j = 0
	for row in csv_reader:
		ensc = row[0]

		print("j = ", j, ensc, "\n")
		# Defines general URL parameters
		server = "http://rest.ensembl.org/"
		ext_homology = "homology/symbol/ciona_intestinalis/" + ensc + "?target_species=danio_rerio"
		content_type = "application/json"
		
		# Custom for each ensc
		homology_info = fetch_endpoint(server, ext_homology, content_type)

		data = homology_info["data"]
		homologies_dict = data[0]
		homologies_info = homologies_dict["homologies"]

		if homologies_info == []:
			print("Error!!! with ", ensc)
			break

		# Contains ("ortholog_one2many", ENSZ)
		target_info_list = list()

		for i in range(len(homologies_info)):
			homo_dict = homologies_info[i]
			target_type = homo_dict["type"]  
			
			target_dict = homo_dict["target"]
			target_id = target_dict["id"]
			target_info = (target_type, target_id)
			target_info_list.append(target_info)

		ensC2ensZ_dict[ensc] = target_info_list

		j += 1

# pickle
PICKLE_OUT = open("ensC2ensZ_dict.pickle", "wb")
pickle.dump(ensC2ensZ_dict, PICKLE_OUT)
PICKLE_OUT.close()