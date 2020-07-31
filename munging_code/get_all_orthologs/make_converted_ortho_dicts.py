"""

	Makes ciona/zeb_converted_ortho_dict
		  {"KHID": ("target_type", [gene_name... ]) ...}
		  {"gene_name" : ("target_type", [KHID...]) ...}

		  ens*2ens*_dict = 'ENSCING00000013657', [('ortholog_one2one', 'ENSDARG00000070426')]
		  				   
		  				   'ENSCING00000007267',
						   [('ortholog_many2many', 'ENSDARG00000098551'),
						   ('ortholog_many2many', 'ENSDARG00000079496'),
						   ('ortholog_many2many', 'ENSDARG00000075571'),
						   ('ortholog_many2many', 'ENSDARG00000079934'),
						   ('ortholog_many2many', 'ENSDARG00000098215')]

						   'ENSCING00000003742', [('ortholog_one2many', 'ENSDARG00000069157')]

		  ciona_ENS_to_KHID_dict = ('ENSCING00000011384', 'KH2012:KH.C2.352')
		  zeb_ens_to_gene_dict = ('ENSDARG00000097685', 'si:ch211-235i11.3')

"""
import pickle
from pprint import pprint 

pickle_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/"
ciona_in = "ensC2ensZ_dict.pickle"
zeb_in = "ensZ2ensC_dict.pickle"

# These are dictionaries that will convert ENSC -> KHID; ENSZ -> gene_name
ciona_convert = "ciona_ENS_to_KHID_dict.pickle"
zeb_convert = "zeb_ens_to_gene_dict.pickle"

# Ciona
ciona_pickle = open(pickle_dir + ciona_in, "rb")
ensC2ensZ_dict = pickle.load(ciona_pickle)

ciona_convert_pickle = open(pickle_dir + ciona_convert, "rb")
ciona_ENS_to_KHID_dict = pickle.load(ciona_convert_pickle)

# Zeb
zeb_pickle = open(pickle_dir + zeb_in, "rb")
ensZ2ensC_dict = pickle.load(zeb_pickle)

zeb_convert_pickle = open(pickle_dir + zeb_convert, "rb")
zeb_ens_to_gene_dict = pickle.load(zeb_convert_pickle)

###

def make_converted_ortho_dict(ens_dict, self_convert_dict, other_convert_dict, verbose=False):
	"""Converts all ENSC and ENSZ to KHID and gene_name in ens*2ens*_dict.

		Args:
			ens_dict: Dictionary to be convert.
					  e.g. ens*2ens*_dict = 'ENSCING00000013657', [('ortholog_one2one', 'ENSDARG00000070426')]

			self_convert_dict: Dictionary that converts keys (ENSC/Z) 
							   in ens_dict to KHID/gene_name.
					  e.g. ciona_ENS_to_KHID_dict for ensC2ensZ_dict

			other_convert_dict: Dictionary that will convert values (ENSZ/C)
			                   in ens_dict to gene_name/KHID.
			          e.g. zeb_ens_to_gene_dict for ensC2ensZ_dict

		Returns:
			ortho_dict: Dictionary with ortho information for KHID and gene_names.
					  e.g. ensC2ensZ_dict = {'ENSCING00000013657', [('ortholog_one2one', 'ENSDARG00000070426')]}
					       ciona_converted_ortho_dict = {'KH2012:KH.C4.409', [('ortholog_one2one', 'chac1')]
	"""
	ortho_dict = dict()

	# All ENSDAR are getting converted- good 
	# i = 0
	for ens in ens_dict:
		# ENSDARG00000100981
		if ens in self_convert_dict:
			# CCDC39
			converted_ens = self_convert_dict[ens]
			print(f"ens = {ens}, converted_ens = {converted_ens}")
		else:
			converted_ens = ens
			print(converted_ens)
			break
		# i += 1 

		converted_target_info_list = list()
		# ens = ENSDARG00000100981
		# all_target_info = [('ortholog_one2many', 'ENSCING00000012337'), ('ortholog_one2many', 'ENSCING00000012339')]
		all_target_info = ens_dict[ens]
		for target_info in all_target_info:
			# 'ortholog_one2many', 'ortholog_one2many'
			ortho_type = target_info[0]
			# 'ENSCING00000012337', 'ENSCING00000012339'
			other_ens = target_info[1]
			if other_ens in other_convert_dict:
				converted_other_ens = other_convert_dict[other_ens]
			else:
				converted_other_ens = other_ens
				print("other ens not in other convert dict ", other_ens)
				break
			# j+=1
			# print("j)

			converted_target_info = (ortho_type, converted_other_ens)
			converted_target_info_list.append(converted_target_info)

			if verbose:
				print(f"target_info = {target_info} and converted_target_info = {converted_target_info}", "\n\n")

		ortho_dict[converted_ens] = converted_target_info_list

	return(ortho_dict)

###

if __name__ == "__main__":
	ciona_converted_ortho_dict = make_converted_ortho_dict(ensC2ensZ_dict, ciona_ENS_to_KHID_dict, zeb_ens_to_gene_dict, verbose=False)
	zeb_converted_ortho_dict = make_converted_ortho_dict(ensZ2ensC_dict, zeb_ens_to_gene_dict, ciona_ENS_to_KHID_dict,verbose=False)

	PICKLE_OUT = open("ciona_converted_ortho_dict.pickle", "wb")
	pickle.dump(ciona_converted_ortho_dict, PICKLE_OUT)
	PICKLE_OUT.close()

	PICKLE_OUT = open("zeb_converted_ortho_dict.pickle", "wb")
	pickle.dump(zeb_converted_ortho_dict, PICKLE_OUT)
	PICKLE_OUT.close()