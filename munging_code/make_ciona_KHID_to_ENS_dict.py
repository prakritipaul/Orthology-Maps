"""

    Makes dictionary in which KHIDs are mapped to ENS transcipt IDs.
    -> ciona_KHID_to_ENS_dict
    'KH.C6.191'
    # keys = 10866

"""
import csv
import pickle
from collections import defaultdict

ciona_ens_dir = "/Users/prakritipaul/Desktop/correspondanceENSEMBL_KH.txt"

# Make ciona_KHID_to_ENS_dict
with open(ciona_ens_dir) as csv_file:
    ciona_KHID_to_ENS_dict = defaultdict(list)

    csv_reader = csv.reader(csv_file, delimiter="\t")

    for row in csv_reader:
        ciona_ENS = row[0]
        ciona_KHID = row[1]

        ciona_KHID_to_ENS_dict[ciona_KHID].append(ciona_ENS)

def find_len(length):
    len_list = list()
    for key in ciona_KHID_to_ENS_dict:
        value = ciona_KHID_to_ENS_dict[key]
        if len(value) == length:
            len_list.append(key)

    return len_list

# Pickle
PICKLE_OUT = open("ciona_KHID_to_ENS_dict.pickle", "wb")
pickle.dump(ciona_KHID_to_ENS_dict, PICKLE_OUT)
PICKLE_OUT.close()

