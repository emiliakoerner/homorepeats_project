# Mapping housekeeping lists from different sources to UniProt using underlying data from UniProt ID mapping tool
# Import python modules
import os
import sys
sys.path.append(os.path.abspath('../../lib'))
from lib.constants import *

# Function to map Housekeeping gene lists to Uniprot using the
# underlying data files of the Uniprot Mapping tool.
def Housekeeping_mapping_uniprot(hk_file, mapping_file, output_file):
    with open(mapping_file, 'r') as mapping:
        mapping_lines = mapping.readlines()     # Mapping file is read into python storage
    with open(hk_file, 'r') as hk_file, open(hk_list, 'w') as output:
        for line in hk_file:
            listid = line.strip().split("\t")[0]    # Hk genes are stored and iterated through
            for line2 in mapping_lines:
                columns = line2.strip().split("\t")
                mapid = columns[2]     # species-specific IDs are always in the third column of the mapping file
                if listid in mapid:     # If a matching entry in the mapping file is found,
                    uniprot_id = columns[0]     # The Uniprot ID is stored and written into an output file with both IDs
                    output.write(f"{listid}\t{uniprot_id}\n")
                    break

# Define dynamic file paths for each organism
file_paths = {}
for up_id in SELECTED_ORGANISMS:
    file_paths[up_id] = {
        # Data
        'UNMAPPED_HK_LIST_FILE': os.path.join(MAINTABLES_DIR, f"hk_unmapped/{up_id}_hk_unmapped.txt"),
        'HK_LIST_FILE': os.path.join(OUTPUT_DIR, f"housekeeping_lists/{up_id}_hk.txt"),
        # Results
        'MAPPED_HK_POLYX_FILE': os.path.join(CURRENT_DIR, f"proteomes_hrs_hk/{up_id}_hrs_hk.tsv")
    }

for up_id in SELECTED_ORGANISMS:
    hk_file = file_paths[up_id]['UNMAPPED_HK_LIST_FILE']
    mapping_file = globals().get(f"{up_id}_mapping")
    hk_list = file_paths[up_id]['HK_LIST_FILE']

    print(f"Processing {up_id}...")  # Print status update
    Housekeeping_mapping_uniprot(hk_file, mapping_file, hk_list)

