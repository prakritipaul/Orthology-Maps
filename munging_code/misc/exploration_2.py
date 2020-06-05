# exploration_2
import csv

ciona_ENS_to_KHID_dict = dict()
repeats = list()
# ciona_ENS_list = ciona_ENS_to_KHID_dict.keys()

ciona_ens_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/lifechanging_aniseed_files/correspondanceENSEMBL_KH.txt"
with open(ciona_ens_dir) as ciona_ens_file:

	csv_reader = csv.reader(ciona_ens_file, delimiter="\t")

	for row in csv_reader:
		ciona_ENS = row[0]
		ciona_KHID = row[1]

		if ciona_ENS in ciona_ENS_to_KHID_dict:
			repeats.append(ciona_ENS)

		ciona_ENS_to_KHID_dict[ciona_ENS] = ciona_KHID