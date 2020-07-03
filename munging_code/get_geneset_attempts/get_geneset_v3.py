"""
	Prepares KHID and zeb gene names for Module v3 in "get_geneset_troubleshooting.Rmd"
	Also gets the "translated" zeb gene 

"""

import csv
import pickle

PICK_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_geneset_attempts/pickles/"
ONE_TO_ONE_KHID_ZEB_GENE_DICT_DIR = PICK_DIR + "one_to_one_khid_zeb_gene_dict.pickle"

PICKLE_1 = open(ONE_TO_ONE_KHID_ZEB_GENE_DICT_DIR, "rb")
ONE_TO_ONE_KHID_ZEB_GENE_DICT = pickle.load(PICKLE_1)

###

khid_list = list()
zeb_genes = list()

for key, value in ONE_TO_ONE_KHID_ZEB_GENE_DICT.items():
	khid_list.append([key])
	zeb_genes.append([value])

"""
Write out results into a .csv file
"""

output_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_geneset_attempts/v3/"
output_file_name = "one_to_one_khid_zeb_gene_dict.csv"

with open(output_dir+output_file_name, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    for key, value in ONE_TO_ONE_KHID_ZEB_GENE_DICT.items():
        csvwriter.writerow([key, value])


"""

# Older Implementation 

out_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_geneset_attempts/v3/"

results_name = out_dir + "khid_list.csv"

csvfile = open(results_name, 'w', newline='')
obj = csv.writer(csvfile)
for elem in khid_list:
	obj.writerow(elem)

csvfile.close()

###

results_name_2 = out_dir + "zeb_genes.csv"

csvfile = open(results_name_2, 'w', newline='')
obj = csv.writer(csvfile)
for elem in zeb_genes:
	obj.writerow(elem)

csvfile.close()

"""