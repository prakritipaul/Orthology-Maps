"""
	
	Makes zeb_ENS_to_gene_dict from "zeb_mart_export.txt"
	# 37241 keys

"""
import csv
import pickle

zeb_mart_dir = "/home/pprakriti/Desktop/zeb_mart_export.txt"
with open(zeb_mart_dir) as csv_file:
	zeb_ens_to_gene_dict = dict()

	csv_reader = csv.reader(csv_file, delimiter="\t")
	for row in csv_reader:
		zeb_ens = row[0]
		gene_name = row[1]
		zeb_ens_to_gene_dict[zeb_ens] = gene_name

	zeb_ens_to_gene_dict.pop('Gene stable ID')

pickle_out = open("zeb_ens_to_gene_dict.pickle", "wb")
pickle.dump(zeb_ens_to_gene_dict, pickle_out)
pickle_out.close()
