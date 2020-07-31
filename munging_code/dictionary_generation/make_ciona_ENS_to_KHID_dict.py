"""

	Converts ciona_KHID_to_ENS_dict to ciona_ENS_to_KHID_dict. 

"""
import pickle

def make_ciona_ENS_to_KHID_dict(ciona_KHID_to_ENS_dict):
	ciona_ENS_to_KHID_dict = dict()

	for khid in ciona_KHID_to_ENS_dict:
		new_khid = "KH2012:" + khid
		new_ens = ciona_KHID_to_ENS_dict[khid][0]

		ciona_ENS_to_KHID_dict[new_ens] = new_khid

	return ciona_ENS_to_KHID_dict


if __name__ == "__main__":

	PICKLE_DIR = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_geneset_attempts/pickles/"
	IN_PICKLE = PICKLE_DIR + "ciona_KHID_to_ENS_dict.pickle"
	OUT_PICKLE = PICKLE_DIR + "ciona_ENS_to_KHID_dict.pickle"


	PICKLE = open(IN_PICKLE, "rb")
	ciona_KHID_to_ENS_dict = pickle.load(PICKLE)

	ciona_ENS_to_KHID_dict = make_ciona_ENS_to_KHID_dict(ciona_KHID_to_ENS_dict)

	# Pickle
	PICKLE_OUT = open(OUT_PICKLE, "wb")
	pickle.dump(ciona_ENS_to_KHID_dict, PICKLE_OUT)
	PICKLE_OUT.close()


