# Constants
import os

"""IMPORTANT: Main directories you might need to define here:
Rep_base_dir is the base directory of this project, relative to the location of this script.
Output_base_dir is your base directory for all output file
Input_base_dir is your base directory for all input files
By default, all base dirs (input, output and repository) are in the same root directory.
All other paths are relative to your current working directory or your base dirs!"
"""

# Base directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
REP_BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..")) #  BASE_DIR = low_complexity_project = repository
# Main project directories within the repository
MAINTABLES_DIR = os.path.join(REP_BASE_DIR, "main_tables")
GETLCRS_DIR = os.path.join(REP_BASE_DIR, "get_lcrs")    # scripts for analysing low complexity regions
HR_DIR = os.path.join(GETLCRS_DIR, "homorepeats")   # scripts for analysing homorepeats

# BASE dir for output
OUTPUT_BASE_DIR = os.path.abspath(os.path.join(REP_BASE_DIR, "..")) # Hardddrive directory/root
OUTPUT_DIR = os.path.join(OUTPUT_BASE_DIR, "output", "homorepeats")  # where output files will be stored
POLYX_DIR = os.path.join(OUTPUT_DIR, "polyxdata")           # where polyx scanner output will be moved after creating it
PROTEOMES_HRS_DIR = os.path.join(OUTPUT_DIR, "proteomes_hrs")
PROTEOMES_HRS_HK_DIR = os.path.join(OUTPUT_DIR, "proteomes_hrs_hk")
HK_LISTS_DIR = os.path.join(OUTPUT_DIR, "housekeeping_lists")

# BASE dir for input
INPUT_BASE_DIR = os.path.abspath(os.path.join(REP_BASE_DIR, ".."))
REF_DIR = os.path.join(INPUT_BASE_DIR, "ftp.uniprot.org", "pub", "databases", "uniprot", "current_release",
             "knowledgebase", "reference_proteomes", "Reference_Proteomes_2024_06")
README_PATH = os.path.join(REF_DIR, "README")   # contains information about reference proteomes, from uniprot

# Taxons and the folder structure are defined by Uniprot
TAXON_CATEGORIES = ["Archaea", "Bacteria", "Eukaryota", "Viruses"]
SELECTED_ORGANISMS = None
#Must be None for 'SELECTED_TAXA' to be considered!
#SELECTED_ORGANISMS = {"UP000005640", "UP000000589", "UP000000803", "UP000001940", "UP000006548", "UP000000625", "UP000002311"}
SELECTED_TAXA = {"Viruses"}
# Select organisms or taxa you want to process. All 4 main scripts use this set!

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
