# Process reference proteomes and Housekeeping gene list to create a list of proteins with their length and Housekeeping status as attributes
# Import python modules
import os
import re
from collections import defaultdict
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hr_lib')))
import constants  # Import constants.py from hr_lib

def Process_proteomes():
    for organism in constants.organisms:  # Loop through each organism
        print(f"Processing {organism}...")

        # Retrieve file paths from constants.py
        proteome_path = constants.file_paths[organism]['PROTEOME_FILE']
        hk_list_path = constants.file_paths[organism]['HK_LIST_FILE']
        mapped_output_path = constants.file_paths[organism]['MAPPED_HK_FILE']

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(mapped_output_path), exist_ok=True)

        # Process proteome and housekeeping lists
        proteome_dict = Proteome_dictionary(proteome_path)
        Map_to_hklist(proteome_dict, hk_list_path, mapped_output_path)
        

def Proteome_dictionary(proteome): #Code to store protein data from proteome in a dict (UniprotID, gene name, sequence)
    proteomedict = defaultdict(lambda: {"gene_name": None, "sequence": ""})  #Create empty dictionary (uniprot -> gn, sequence)
    with open(proteome, 'r') as file:  # Read proteome file
        current_id = None       # Variables to keep track of the current UP ID and its sequence
        current_sequence = []
        for line in file:       # Iterate through each line of the file
            if line.startswith('>'):    # If the line starts with '>', it is a header
                if current_id:          # If there is a protein being processed already, save it to the dictionary
                    proteomedict[current_id]["sequence"] = ''.join(current_sequence)    # Join sequences without a divider
                gn_match = re.search(r"GN=(\S+)", line) # look for gene name
                uniprot_match = re.search(r">.+?\|([^\|]+)\|", line) # look for Uniprot ID

                current_id = uniprot_match.group(1) if uniprot_match else None      # put Uniprot ID as current ID
                gene_name = gn_match.group(1) if gn_match else None                 # store gene name too
                current_sequence = []           # Reset the current sequence for the next protein
                if current_id:
                    proteomedict[current_id]["gene_name"] = gene_name       # save gene name in the dictionary
            else:
                current_sequence.append(line.strip())   # If the line is not a header, store the sequence
        if current_id:
            proteomedict[current_id]["sequence"] = ''.join(current_sequence)  # Save the last protein sequence after loop finishes
    print(len(proteomedict), "proteins in the dictionary")
    return proteomedict

def remove_suffix(uniprot_id):
    return re.sub(r"(-\d+)$", "", uniprot_id)   # Human Uniprot IDs can have suffixes in the mapping file.
def Map_to_hklist(proteomedict, housekeeping_list, mapped):
    global hk_genes
    hk_genes = set()  # Load housekeeping genes from file into a set
    with open(housekeeping_list, 'r') as file:
        for line in file:
            hk_genes.add(line.strip().split("\t")[1].lower())   # Uniprot ID only
    with open(mapped, 'w') as mapped:
        mapped.write(f"gene_name\tuniprot_id\tlength\tHk\n")  # Write header
        hk_count = 0            # Count the hk proteins from the original file
        for uniprot_id, proteindata in proteomedict.items():  # Iterate through each dictionary entry aka protein
            sequence = proteindata["sequence"]  # Variables for Sequence, Length and gene name
            length = len(sequence)
            gene_name = proteindata["gene_name"]
            hk_status = "0"
            if any(remove_suffix(hk_id) in uniprot_id.lower() for hk_id in hk_genes):  #handle uniprot ids with suffixes
                hk_status = "1"
                hk_count += 1
            if uniprot_id in hk_genes:
                hk_status = "1"
                hk_count += 1
            mapped.write(f"{gene_name}\t{uniprot_id}\t{length}\t{hk_status}\n") # write output file
        print("Hk mapping complete:", hk_count, "hk proteins found")

Process_proteomes()

