# Constants

import os

# Base directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
print(BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
POLYX_DIR = os.path.join(PROCESSED_DIR, "polyxdata")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# mapping files from Uniprot
human_mapping = os.path.join(RAW_DIR, "mapping files/HUMAN_9606_idmapping.txt")
mouse_mapping = os.path.join(RAW_DIR, "mapping files/MOUSE_10090_idmapping.txt")
fruitfly_mapping = os.path.join(RAW_DIR, "mapping files/DROME_7227_idmapping.txt")
celegans_mapping = os.path.join(RAW_DIR, "mapping files/CAEEL_6239_idmapping.txt")
yeast_mapping = os.path.join(RAW_DIR, "mapping files/YEAST_559292_idmapping.txt")
ecoli_mapping = os.path.join(RAW_DIR, "mapping files/ECOLI_83333_idmapping.txt")
arabidopsis_mapping = os.path.join(RAW_DIR, "mapping files/ARATH_3702_idmapping.txt")

# data file paths
organisms = ['human', 'mouse', 'fruitfly', 'celegans', 'yeast', 'ecoli', 'arabidopsis']
file_paths = {}
for organism in organisms:
    file_paths[organism] = {
        # Data
        'PROTEOME_FILE': os.path.join(RAW_DIR, f"proteomes/{organism}.fasta"),
        'UNMAPPED_HK_LIST_FILE': os.path.join(RAW_DIR, f"hk_unmapped/{organism}_hk_unmapped.txt"),
        'HK_LIST_FILE': os.path.join(PROCESSED_DIR, f"housekeeping_lists/{organism}_hk.txt"),
        'POLYX_FILE': os.path.join(POLYX_DIR, f"{organism}_polyx.txt"),
        # Results
        'MAPPED_HK_FILE': os.path.join(RESULTS_DIR, f"mapped_hk/{organism}_mapped.txt"),
        'MAPPED_HK_POLYX_FILE': os.path.join(RESULTS_DIR, f"mapped_hk_polyx/{organism}_mapped_polyx.tsv")
    }
