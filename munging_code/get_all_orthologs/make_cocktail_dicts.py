"""

	Makes (1) *_CT_cocktail_dict
	{CT: [cocktail_gene_1... cocktail_gene_n]...}

	Ciona:
		  {"endo": [KHID_1... KHID_n]...}

	Zeb:
		  {"lens": [gene_name_1... gene_name_n]}
		  
		  e.g.
		  {'diff_neus': ['elavl3',
               'nhlh2',
               'onecut1',
               'dlb',
               'otpa',
               'LOC100536821',
               'LOC797032',
               'cplx2l',
               'mllt11',
               'ebf2']...

	###
	
	(2) *_ortho_CT_cocktail_dict
		{CT_1: {cocktail_gene_1: [orthos]}
		           {cocktail_gene_2 : [orthos]...}...
	     CT_n}

	Ciona: 
		 {CT_1 : {KHID_1: [(ortho) gene_name_1... gene_name_n]},
		  CT_2: {KHID_2: [(ortho) gene_name_1... gene_name_n]...
		  }
		  
	Zeb:
		 {CT_1: {gene_name_1: [(ortho) KHID_1... KHID_n]},
		  CT_2: {gene_name_2: [(ortho) KHID_1... KHID_n]}...
		  }
	###

	(3) Convert ciona_ortho_cocktail_dict with zeb gene names.

"""
import csv
import pickle
from pprint import pprint 
from collections import defaultdict

# ## Get ens2_dicts Dicts                           
# pickle_dict_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/"
# ortho_ciona_pickle = "ensC2ensZ_dict.pickle"
# ortho_zeb_pickle = "ensZ2ensC_dict.pickle"

# ciona_in_pickle = open(pickle_dict_dir + ortho_ciona_pickle, "rb")
# ensC2ensZ_dict = pickle.load(ciona_in_pickle)

# zeb_in_pickle = open(pickle_dict_dir + ortho_zeb_pickle, "rb")
# ensZ2ensC_dict = pickle.load(zeb_in_pickle)

######## MAKE COCKTAIL DICTS ########

cocktail_dir = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/get_all_orthologs/CT_cocktails/"
ciona_cocktail_csv = "ciona_top10_df.csv"
zeb_cocktail_csv = "zeb_top10_df.csv"

def make_CT_cocktail_dict(cocktail_csv):
	CT_cocktail_dict = dict()

	with open(cocktail_csv) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			CT = row[0]
			cocktail_genes = row[1:]
			CT_cocktail_dict[CT] = cocktail_genes

	return(CT_cocktail_dict)

ciona_CT_cocktail_dict = make_CT_cocktail_dict(cocktail_dir+ciona_cocktail_csv)
zeb_CT_cocktail_dict = make_CT_cocktail_dict(cocktail_dir+zeb_cocktail_csv)







######## MAKE COCKTAIL DICTS ########
ciona_converted = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/ciona_converted_ortho_dict.pickle"
ciona_pickle = open(ciona_converted, "rb")

ciona_converted_ortho_dict = pickle.load(ciona_pickle) 

zeb_converted = "/home/pprakriti/princeton_google_drive/Levine Lab/Orthology-Maps/all_ortholog_pickles/zeb_converted_ortho_dict.pickle"
zeb_pickle = open(zeb_converted, "rb")

zeb_converted_ortho_dict = pickle.load(zeb_pickle) 

#####################################

def make_ortho_CT_cocktail_dict(CT_cocktail_dict, converted_ortho_dict):
	"""Do below:
		Args:
			CT_cocktail_dict: Dict whose genes you want to find orthologs for.
			ortho_dict: Dict that will help you do that.
		
		Routine: Refer to Script Docstring.

		Returns: ortho_CT_cocktail_dict: Self-explanatory.
	"""
	ortho_CT_cocktail_dict = defaultdict(list)
	not_ortho_list = list()

	for CT in CT_cocktail_dict:
		print("CT = ", CT, "\n")
		cocktail_gene_info = CT_cocktail_dict[CT]
		print("cocktail_gene_info = ", cocktail_gene_info, "\n")
		for cocktail_gene in cocktail_gene_info:
			if cocktail_gene in converted_ortho_dict:
				print("cocktail_gene = ", cocktail_gene)
				ortho_gene_info = converted_ortho_dict[cocktail_gene]
				print("ortho_gene_info = ", ortho_gene_info, "\n\n")
				ortho_CT_cocktail_dict[CT].append((cocktail_gene, ortho_gene_info))
				pprint(ortho_CT_cocktail_dict)
			else:
				not_ortho_list.append(cocktail_gene)
				ortho_CT_cocktail_dict[CT].append(None)

	return(ortho_CT_cocktail_dict, not_ortho_list)

###

# Need to clean zeb_ortho_dict to remove ENSC. 
ciona_ans = make_ortho_CT_cocktail_dict(ciona_CT_cocktail_dict, ciona_converted_ortho_dict)
ciona_ortho_CT_cocktail_dict = ciona_ans[0]
# 58/70
not_ortho_ciona = ciona_ans[1]

# zeb_ans = make_ortho_CT_cocktail_dict(zeb_CT_cocktail_dict, zeb_converted_ortho_dict)
# zeb_ortho_CT_cocktail_dict = zeb_ans[0]

# # 100/140
# not_ortho_zeb = zeb_ans[1]


