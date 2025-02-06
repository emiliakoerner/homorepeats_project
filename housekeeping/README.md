# README for scripts related to Housekeeping genes

# Mapping_hklists_to_Uniprot.py
# Mapping housekeeping lists from different sources to UniProt using underlying data from UniProt ID mapping tool
## Import python modules
``` python
import os
import sys
sys.path.append(os.path.abspath('../../lib'))
from lib.constants import *

```
## Define file paths dynamically for each organism (does not Need to be changed when Folder structure of repository is preserved)
``` python
file_paths = {}
for up_id in SELECTED_ORGANISMS:
    file_paths[up_id] = {
        # Data
        'UNMAPPED_HK_LIST_FILE': os.path.join(MAINTABLES_DIR, f"hk_unmapped/{up_id}_hk_unmapped.txt"),
        'HK_LIST_FILE': os.path.join(OUTPUT_DIR, f"housekeeping_lists/{up_id}_hk.txt"),
        # Results
        'MAPPED_HK_POLYX_FILE': os.path.join(CURRENT_DIR, f"proteomes_hrs_hk/{up_id}_hrs_hk.tsv")
    }
```

## Functions
``` python
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
```
## File paths and calling the function
``` python
for up_id in SELECTED_ORGANISMS:
    hk_file = file_paths[up_id]['UNMAPPED_HK_LIST_FILE']
    mapping_file = globals().get(f"{up_id}_mapping")
    hk_list = file_paths[up_id]['HK_LIST_FILE']

    print(f"Processing {up_id}...")  # Print status update
    Housekeeping_mapping_uniprot(hk_file, mapping_file, hk_list)


```

# Create_hrs_hk_file.py: Adds Housekeeping Status to proteome_hrs files (List of Proteins for each proteome with polyxdata)

## Import python modules
``` python
import os
import sys
import re
from collections import defaultdict
from lib.load_organisms import organisms
sys.path.append(os.path.abspath('../../lib'))
from lib.constants import *  # Import constants.py from hr_lib
```

## Functions
``` python
# Finds proteome_hrs file for each organism in SELECTED_ORGANISMS or SELECTED_TAXA and defines the file paths dynamically. Processing function that calls the mapping function
def Process_proteomes():
    for up_id in organisms:  # Loop through each selected organism
        print(f"Processing {up_id}...")

        # Dynamically determine the taxon category based on the file path
        proteome_hrs_path = None
        for category in TAXON_CATEGORIES:  # Loop through the taxon categories
            candidate_path = os.path.join(OUTPUT_DIR, "proteomes_hrs", category, f"{up_id}_hrs.tsv")
            if os.path.exists(candidate_path):  # Check if the file exists in the category folder
                proteome_hrs_path = candidate_path
                print(proteome_hrs_path)
                category = category  # Set the taxon category
                break
        if not proteome_hrs_path:
            print(f"Error: No _hrs file found for {up_id}. Skipping...")
            continue
        # Define paths
        hk_list_path = os.path.join(OUTPUT_DIR, "housekeeping_lists", f"{up_id}_hk.txt")  # Housekeeping gene list path
        output_path = os.path.join(OUTPUT_DIR, "proteomes_hrs_hk", category, f"{up_id}_hrs_hk.tsv")  # Final output path

        # Process proteome and housekeeping lists
        Map_to_hklist(proteome_hrs_path, hk_list_path, output_path)

# Checks for each protein if it is Housekeeping and creates a new file with an additional column containing the Hk status
def Map_to_hklist(proteome_hrs, housekeeping_list, output):
    hk_genes = set()  # Set to store housekeeping genes
    with open(housekeeping_list, 'r') as file:
        for line in file:
            hk_genes.add(line.strip().split("\t")[1].lower())  # Add Uniprot IDs to the set, in lowercase

    with open(proteome_hrs, 'r') as proteome_file, open(output, 'w') as output_file:
        output_file.write("Genename\tUniprot_id\tLength\tPolyx_count\tPolyx_types\tPolyx_lengths"
                          "\tTotal_length\tPption_polyx\tCount_grouped\tHk\n")  # Write header

        # Iterate through each line in the proteome file
        next(proteome_file) # skip header
        for line in proteome_file:
            parts = line.strip().split("\t")
            gene_name = parts[0]  # Gene name from the proteome file
            uniprot_id = parts[1]  # Uniprot ID from the proteome file
            length = parts[2]  # Protein sequence
            count = parts[3]
            types = parts[4]
            lengths = parts[5]
            total_length = parts[6]
            pption = parts[7]
            groups = parts[8]
            hk_status = "0"  # Default to non-housekeeping (0)

            # Check if this Uniprot ID is in the housekeeping list
            if uniprot_id.lower() in hk_genes:
                hk_status = "1"  # If the protein is in the housekeeping list, set status to 1

            # Write the data to the output file
            output_file.write(f"{gene_name}\t{uniprot_id}\t{length}\t{count}\t{types}\t{lengths}\t"
                              f"{total_length}\t{pption}\t{groups}\t{hk_status}\n")

    print(f"Housekeeping mapping complete for {proteome_hrs}")
```
## Call function the function
``` python
Process_proteomes()
```