# Mapping housekeeping lists from different sources to UniProt using underlying data from UniProt ID mapping tool
## Import python modules
``` python
import os
```
## Functions
``` python
# Function to map Housekeeping gene lists to Uniprot using the
# underlying data files of the Uniprot Mapping tool. Has to be done for each organism individually.
# hk list should have Identifier (ENS ID, WBID, Flybase ID, ...) in column 1 (Index 0)
def Housekeeping_mapping_uniprot(hk_file, mapping_file, hk_list):
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
hk_file = "unmapped hk files/human_hk_unmapped.txt"     #original file without Uniprot IDs
mapping_dir = "mapping files"
mapping_file = os.path.join(mapping_dir, "HUMAN_9606_idmapping.txt")        # Mapping file from Uniprot
housekeeping_dir = "housekeeping_lists"
hk_list = os.path.join(housekeeping_dir, "human_hk.txt")        # Output file with both species-specific ID and Uniprot ID

Housekeeping_mapping_uniprot(hk_file, mapping_file, hk_list)
```
