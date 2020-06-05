"""

	Makes  dictionary in which KHIDs are mapped to gene names from Christells's file.
    -> ciona_KHID_to_gene_dict
    'KH2012:KH.S999.4' 
    # keys = 10965

    WARNING:
    	(1) The ENSC of KHID may map to different gene names in Ensembl.
    	(2) Refer to exploration of 10/top50 Ciona DEGs in 
    		"get_pairwise_zeb_ciona_degs.Rmd"  


"""
import csv
import pickle
from collections import defaultdict      

ciona_gene_dir = "/home/pprakriti/Desktop/ANISEED-Cirobu-GeneName-3bestBlastHitHuman.rnames"
with open(ciona_gene_dir) as csv_file:
    ciona_KHID_to_gene_dict = defaultdict(list)

    csv_reader = csv.reader(csv_file, delimiter="\t")

    for row in csv_reader:
        ciona_KHID = row[0]
        ciona_gene = row[1]

        ciona_KHID_to_gene_dict[ciona_KHID].append(ciona_gene)

# Pickle
PICKLE_OUT = open("ciona_KHID_to_gene_dict.pickle", "wb")
pickle.dump(ciona_KHID_to_gene_dict, PICKLE_OUT)
PICKLE_OUT.close()
