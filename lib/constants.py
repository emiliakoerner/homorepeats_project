# Constants
import os

# Base directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..")) #  BASE_DIR = low_complexity_project = repository

# Harddrive with the reference proteomes and where output will be saved:
HD_DIR = os.path.abspath(os.path.join(BASE_DIR, "..")) # Hardddrive directory/root

# Main project directories
MAINTABLES_DIR = os.path.join(BASE_DIR, "main_tables")
GETLCRS_DIR = os.path.join(BASE_DIR, "get_lcrs")
HR_DIR = os.path.join(GETLCRS_DIR, "homorepeats")   # contains scripts to discover hrs in proteomes and create a list of
                                                    # proteins with their homorepeats

# not on Github:  Output
OUTPUT_DIR = os.path.join(HD_DIR, "output", "homorepeats")  # where output files will be stored
POLYX_DIR = os.path.join(OUTPUT_DIR, "polyxdata")           # where polyx scanner output will be moved after creating it

# not on Github: Reference proteomes (order structure from ftp.uniprot.org)
REF_DIR = os.path.join(HD_DIR, "ftp.uniprot.org", "pub", "databases", "uniprot", "current_release",
             "knowledgebase", "reference_proteomes", "Reference_Proteomes_2024_06")
README_PATH = os.path.join(REF_DIR, "README")   # contains information about reference proteomes, from uniprot

# Taxons and the folder structure are defined by Uniprot
TAXON_CATEGORIES = ["Archaea", "Bacteria", "Eukaryota", "Viruses"]
SELECTED_ORGANISMS = None
#Must be None for 'SELECTED_TAXA' to be considered!
#SELECTED_ORGANISMS = {"UP000005640", "UP000000589", "UP000000803", "UP000001940", "UP000006548", "UP000000625", "UP000002311"}
SELECTED_TAXA = {"Eukaryota"}
# Select organisms that you want to process. All 4 main scripts use this set!

# mapping files from Uniprot for housekeeping. Hardcored to preserve the original file names from Uniprot
UP000005640_mapping = os.path.join(MAINTABLES_DIR, "mapping_files\\HUMAN_9606_idmapping.txt")
UP000000589_mapping = os.path.join(MAINTABLES_DIR, "mapping_files\\MOUSE_10090_idmapping.txt")
UP000000803_mapping = os.path.join(MAINTABLES_DIR, "mapping_files\\DROME_7227_idmapping.txt")
UP000001940_mapping = os.path.join(MAINTABLES_DIR, "mapping_files\\CAEEL_6239_idmapping.txt")
UP000002311_mapping = os.path.join(MAINTABLES_DIR, "mapping_files\\YEAST_559292_idmapping.txt")
UP000000625_mapping = os.path.join(MAINTABLES_DIR, "mapping_files\\ECOLI_83333_idmapping.txt")
UP000006548_mapping = os.path.join(MAINTABLES_DIR, "mapping_files\\ARATH_3702_idmapping.txt")


"""# Housekeeping (move to extra file?)
organisms = ["UP000005640", "UP000000589", "UP000000803", "UP000001940", "UP000006548", "UP000000625", "UP000002311"]
file_paths = {}
for up_id in organisms:
    file_paths[up_id] = {
        # Data
        'UNMAPPED_HK_LIST_FILE': os.path.join(MAINTABLES_DIR, f"hk_unmapped/{up_id}_hk_unmapped.txt"),
        'HK_LIST_FILE': os.path.join(OUTPUT_DIR, f"housekeeping_lists/{up_id}_hk.txt"),
        # Results
        'MAPPED_HK_POLYX_FILE': os.path.join(CURRENT_DIR, f"proteomes_hrs_hk/{up_id}_hrs_hk.tsv")
    }"""
