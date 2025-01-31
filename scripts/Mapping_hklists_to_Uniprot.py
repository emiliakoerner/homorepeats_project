# Mapping housekeeping lists from different sources to UniProt using underlying data from UniProt ID mapping tool
# Import python modules
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hr_lib')))
import constants

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

for organism in organisms:
    hk_file = file_paths[organism]['UNMAPPED_HK_LIST_FILE']
    mapping_file = mapping_files[organism]
    hk_list = file_paths[organism]['MAPPED_HK_FILE']

    print(f"Processing {organism}...")  # Print status update
    Housekeeping_mapping_uniprot(hk_file, mapping_file, hk_list)

