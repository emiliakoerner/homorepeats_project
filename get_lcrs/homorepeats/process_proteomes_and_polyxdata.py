# what do I need?
# polyx scanner output for every single proteome - how?
# then just make a list with uniprot id, gene name, proteome length and then add polyx info.

import os
import re
from collections import defaultdict
import sys
sys.path.append(os.path.abspath('../../lib'))
from lib.constants import *


def Proteome_dictionary(proteome): # Code to store protein data from proteome in a dict (UniprotID, gene name, sequence)
    global proteomedict
    proteomedict = defaultdict(lambda: {"gene_name": None, "sequence": ""})  #Create empty dictionary (uniprot -> gn, sequence)
    with open(proteome, 'r') as file:  # Read proteome file
        current_id = None       # Variables to keep track of the current UP ID and its sequence
        current_sequence = []
        for line in file:       # Iterate through each line of the file
            if line.startswith('>'):    # If the line starts with '>', it is a header
                if current_id:          # If there is a protein being processed already, save it to the dictionary
                    proteomedict[current_id]["sequence"] = ''.join(current_sequence)    # Join sequences without a divider
                gn_match = re.search(r"GN=(\S+)", line) # look for gene name
                uniprot_match = re.search(r">.+?\|([^\|]+)\|", line) # look for UP ID

                current_id = uniprot_match.group(1) if uniprot_match else None      # put UP ID as current ID
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

# function 2: read polyx data into python
def Polyx_dictionary(input):   #create dictionary to store information for each protein ID
    global polyxdata
    polyxdata = defaultdict(lambda: {"polyx_count": 0, "polyx_types": [], "polyx_lengths": [], "total_length": 0})
    with open(input) as file:
        next(file)
        for line in file:
            parts = line.strip().split("\t")
            protein_info = parts[5]  # First column, e.g., sp|Q8H102|BH128_ARATH
            protein_ID_parts = protein_info.split('|')  # Split to extract protein ID

            if len(protein_ID_parts) < 2:  # Check if the split resulted in the expected number of parts
                print(f"Skipping malformed protein ID: {protein_info}")
                continue

            protein_ID = protein_ID_parts[1]  # The second part is the protein ID (e.g., Q8H102)
            # variables for each column
            polyx_type = parts[2]
            start = int(parts[0])
            end = int(parts[1])
            length = end - start + 1            # Calculating the total length of polyx regions of each region
            # Update the data for polyx count, types and length:
            polyxdata[protein_ID]["polyx_count"] += 1          # Count goes up 1 for every line with that protein ID
            polyxdata[protein_ID]["polyx_types"].append(polyx_type)    # Make a list of each polyx type
            polyxdata[protein_ID]["polyx_lengths"].append(length)
            polyxdata[protein_ID]["total_length"] += length

# function 3: create file combining all the data
def Create_final_doc(outputfile):    #Code to create final document by adding polyx info to the last output file
    with open(outputfile, 'w') as output:
        output.write(f"Genename\tUniProtID\tLength\tPolyx_count\tPolyx_types\tPolyx_lengths"
                     f"\tTotal_length\tPption_polyx\tCount_grouped\n") # Header
        for uniprot_id, proteindata in proteomedict.items():  # Iterate through each dictionary entry aka protein
            sequence = proteindata["sequence"]  # Variables for Sequence, Length and gene name
            length = len(sequence)
            gene_name = proteindata["gene_name"]
            if uniprot_id in polyxdata:     # If the protein has a polyx region, write polyx data into output file
                data = polyxdata[uniprot_id]
                polyx_count = data["polyx_count"]
                polyx_types_combined = "/".join(data["polyx_types"])    # Join polyxtypes (stored as set) with / as divider
                polyx_lengths = "/".join(map(str, data["polyx_lengths"]))
                total_length = data["total_length"]
                aa_percent = round(int(total_length)/int(length), 4)
                output.write(f"{gene_name}\t{uniprot_id}\t{length}\t"
                                 f"{polyx_count}\t{polyx_types_combined}\t{polyx_lengths}\t{total_length}\t{aa_percent}\t{polyx_count}\n")
            else:   # If protein has no polyx region, put 0 or - instead for poly x count, type and length
                output.write(f"{gene_name}\t{uniprot_id}\t{length}\t0\t-\t0\t0\t0\t0\n")

# function 4: main processing function
def Processing_proteomes():
    for up_id in SELECTED_ORGANISMS:
        category = next((cat for cat in TAXON_CATEGORIES if os.path.exists(os.path.join(REF_DIR, cat, up_id))), None)
        if not category:
            print(f"Organism {up_id} not found in any category, skipping...")
            continue

        fasta_folder = os.path.join(REF_DIR, category, up_id)
        if not os.path.isdir(fasta_folder):
            continue

# Find the correct FASTA file (UPID_TaxID.fasta)
        fasta_file = next(
            (f for f in os.listdir(fasta_folder) if f.endswith(".fasta") or f.endswith(".fasta.gz")), None
        )
        if not fasta_file:
            print(f"No FASTA file found for {up_id}")
            continue

        proteome_path = os.path.join(fasta_folder, fasta_file)

        # Find the corresponding PolyX output
        polyx_folder = os.path.join(POLYX_DIR, category, up_id)
        if not os.path.exists(polyx_folder):
            print(f"No PolyX folder for {up_id}, skipping...")
            continue

        polyx_file = next(
            (f for f in os.listdir(polyx_folder) if f.endswith("_polyx.txt")), None
        )
        if not polyx_file:
            print(f"No PolyX file found for {up_id}")
            continue

        polyx_path = os.path.join(polyx_folder, polyx_file)
        output_path = os.path.join(OUTPUT_DIR, "proteomes_hrs", category, f"{up_id}_hrs.tsv")

        # Create output category directory if not exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Process the proteome and PolyX data
        Proteome_dictionary(proteome_path)
        Polyx_dictionary(polyx_path)
        Create_final_doc(output_path)
        print(f"Processed {up_id}: created {output_path}")

Processing_proteomes()
