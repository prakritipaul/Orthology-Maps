"""
	UNUSED UNUSED UNUSED 

	Refer to ensembl_get_one_to_one_orthologs.py

	Part 1: Creates:
		(1) ciona_ortho_dict = {"ciona_ENS": ["zeb_ortho_ENS"...] ...}
		(2) zeb_ortho_dict = {"zeb_ENS": ["ciona_ortho_ENS"...] ...}

	Part 2: Uses above to Create:
		(1) one_to_one_dict = {"ciona_ENS": "zeb_ENS"}
			# 3397
			# Sad that there are some errors. 
			# e.g. ENSCING00000007924/ENSDARG00000076058
			# e.g. ENSDARG00000069920
			# Don't know how many, but 5 other randomly-sampled ones were correct.

			also weird_list: list of ciona's zeb orthologs that are not
							 present as keys in zeb_ortholog_dict/zeb_ciona.xls
			# 26

		(2) all_ciona_orthos_for_zeb_list = ["ciona_ortho_ENS_1"... 														"ciona_ortho_ENS_n"]
		Note: This is a list of ciona_ortho_ENS's from all zeb_ENS 
		Therefore, there may be repeats of ciona_ortho_ENS's.
			# 19776

		(3) ciona_orthos_for_zeb_dict = {"ciona_ortho_ENS": 
										 # times it appears in 
										 all_ciona_orthos_for_zeb_list}
			# 7720
			# Note: Just because a ciona_ENS appears once doesn't mean
			#		that it is a 1-1 ortholog with another zeb_ENS.

"""
import csv

# Vera directories 
ciona_zeb_ortho_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_1-1_orthologs_methods/biomart_dbOrtho_tests/ciona_zeb_bioDBnet_dbOrtho_200424142515_32497443.txt"
zeb_ciona_ortho_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_1-1_orthologs_methods/biomart_dbOrtho_tests/zeb_ciona_bioDBnet_dbOrtho_200424152221_690826687.txt"


def make_ciona_ortho_dict(ciona_dir):
	with open(ciona_zeb_ortho_dir) as ciona_zeb_csv_file:
		# Make ciona_ortho_dict
		ciona_ortho_dict = dict ()

		csv_reader = csv.reader(ciona_zeb_csv_file, delimiter="\t")
		for row in csv_reader:
			ciona_ENS = row[0]
			zeb_ortho_ENS = row[1].split(";")
			if zeb_ortho_ENS == [""]:
				continue
			ciona_ortho_dict[ciona_ENS] = zeb_ortho_ENS
		ciona_ortho_dict.pop('Ensembl Gene ID')

	return ciona_ortho_dict


def make_zeb_ortho_dict(zeb_dir):
	with open(zeb_ciona_ortho_dir) as zeb_ciona_csv_file:
		zeb_ortho_dict = dict()

		csv_reader = csv.reader(zeb_ciona_csv_file, delimiter="\t")
		for row in csv_reader:
			zeb_ENS = row[0]
			ciona_ortho_ENS = row[1].split(";")
			if ciona_ortho_ENS == [""]:
				continue
			zeb_ortho_dict[zeb_ENS] = ciona_ortho_ENS
		zeb_ortho_dict.pop('Ensembl Gene ID')

	return zeb_ortho_dict


def get_one_to_one_dict(ciona_ortho_dict, zeb_ortho_dict):
	one_to_one_dict = dict()
	weird_zeb_ENS = list()

	for ciona_ENS in ciona_ortho_dict:
		# print(f"START START START with ciona_ENS = {ciona_ENS} \n")
		# Gets ciona's zeb ortholog (zeb_ortho_ENS).
		zeb_ortho_ENS = ciona_ortho_dict[ciona_ENS]
		# print(f"ciona's zeb ortho {zeb_ortho_ENS} \n")

		if len(zeb_ortho_ENS) == 1:
			# If there's only 1 ortholog.
			munged_zeb_ortho_ENS = zeb_ortho_ENS[0]
			# print(f"enter if, with zeb_ortho_ENS = {munged_zeb_ortho_ENS} \n")
			# First checks if zeb_ortho_ENS even exists
			if munged_zeb_ortho_ENS in zeb_ortho_dict:
				# Checks if zeb_ortho_ENS also has 1 ciona ortholog (ciona_ortho_ENS)
				ciona_ortho_ENS = zeb_ortho_dict[munged_zeb_ortho_ENS]
				if len(ciona_ortho_ENS) == 1:
					# Yes it does! 
					munged_ciona_ortho_ENS = ciona_ortho_ENS[0]
					# print(f"YESYESYES \n")
					one_to_one_dict[ciona_ENS] = munged_zeb_ortho_ENS
			else:
				# Keeps track of zeb_ortho_ENS's that didn't exist
				weird_zeb_ENS.append(munged_zeb_ortho_ENS)

	return one_to_one_dict, weird_zeb_ENS

def get_all_ciona_orthos_for_zeb_list(zeb_ortho_dict):
	# Makes a list of ciona_orthos for all zeb_ENS.
	# There are repeats. 
	all_ciona_orthos_for_zeb_list = list()

	i = 0 
	for zeb_ENS in zeb_ortho_dict:
		for ciona_ortho_ENS in zeb_ortho_dict[zeb_ENS]:
			print(f"zeb_ENS = {zeb_ENS} and ciona_ortho_ENS = {ciona_ortho_ENS} \n")
			all_ciona_orthos_for_zeb_list.append(ciona_ortho_ENS)
		# i += 1
		# if i == 5:
		# 	break 


	return all_ciona_orthos_for_zeb_list

def get_ciona_orthos_for_zeb_dict(all_ciona_orthos_for_zeb_list):
	"""
		Makes a dictionary that keeps track of how many times
		a ciona_ortho_ENS appeared in all_ciona_orthos_for_zeb_list
		Therefore, if >1 => 1-many mapping 
	"""
	ciona_orthos_for_zeb_dict = dict()

	for ciona_ortho_ENS in all_ciona_orthos_for_zeb_list:
		print(f"ciona_ortho_ENS = {ciona_ortho_ENS} \n")
		if ciona_ortho_ENS in ciona_orthos_for_zeb_dict:
			print(f"yes it's here \n")
			ciona_orthos_for_zeb_dict[ciona_ortho_ENS] += 1
		else:
			print(f"no it's not yet")
			ciona_orthos_for_zeb_dict[ciona_ortho_ENS] = 1

	return ciona_orthos_for_zeb_dict


if __name__ == "__main__":
	ciona_ortho_dict = make_ciona_ortho_dict(ciona_zeb_ortho_dir)
	zeb_ortho_dict = make_zeb_ortho_dict(zeb_ciona_ortho_dir)

	one_to_one_dict, weird_list = get_one_to_one_dict(ciona_ortho_dict, zeb_ortho_dict)

	all_ciona_orthos_for_zeb_list = get_all_ciona_orthos_for_zeb_list(zeb_ortho_dict)
	ciona_orthos_for_zeb_dict = get_ciona_orthos_for_zeb_dict(all_ciona_orthos_for_zeb_list)

