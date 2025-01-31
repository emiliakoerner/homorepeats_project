README for scripts
# Run polyx scanner on all proteomes in data/raw/proteomes
## Import python modules
``` python
import subprocess
import os
import sys
import shutil
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(base_dir, "hr_lib"))
import constants  # Import constants.py from hr_lib
```
## Functions

``` python
polyx_script = os.path.join(base_dir, "scripts", "polyx2", "polyx2_standalone.pl")  # Path to polyx.pl
    output_dir = os.path.join(base_dir, "data", "processed", "polyxdata")  # Directory where output files should go

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for organism in constants.organisms:
        print(f"Running PolyX for {organism}...")

        proteome_path = constants.file_paths[organism]['PROTEOME_FILE']
        output_file = os.path.join(output_dir, f"{organism}_polyx.txt")  # Final renamed file

        # Change working directory to output folder to run PolyX
        os.chdir(output_dir)

        command = ["perl", polyx_script, proteome_path]

        try:
            # Run polyx.pl
            subprocess.run(command, check=True)

            # Move and rename output file
            if os.path.exists("output_polyx.txt"):
                shutil.move("output_polyx.txt", output_file)
                print(f"PolyX completed for {organism}. Output saved as {output_file}")
            else:
                print(f"Error: output_polyx.txt was not created for {organism}.")

        except subprocess.CalledProcessError as e:
            print(f"Error running PolyX for {organism}: {e}")
	
```

## Run
``` python
run_polyx()
```

# Mapping housekeeping lists from different sources to UniProt using underlying data from UniProt ID mapping tool
## Import python modules
``` python
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hr_lib')))
import constants
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

for organism in organisms:
    hk_file = file_paths[organism]['UNMAPPED_HK_LIST_FILE']
    mapping_file = mapping_files[organism]
    hk_list = file_paths[organism]['MAPPED_HK_FILE']

    print(f"Processing {organism}...")  # Print status update
    Housekeeping_mapping_uniprot(hk_file, mapping_file, hk_list)

```

# Process Polyx scanner information and create a new file with the Polyx information for each protein
## Import python modules
``` python
import os
from collections import defaultdict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hr_lib')))
import constants  # Import constants.py from hr_lib

```
## Functions
``` python
def Polyx_dictionary(input):   #create dictionary to store information for each protein ID
    global polyxdata
    polyxdata = defaultdict(lambda: {"polyx_count": 0, "polyx_types": [], "polyx_lengths": [], "total_length": 0})
    with open(input) as file:
        next(file)      # skip header
        for line in file:
            parts = line.strip().split("\t")
            protein_info = parts[0]  # First column, e.g., sp|Q8H102|BH128_ARATH
            protein_ID_parts = protein_info.split('|')  # Split to extract protein ID

            if len(protein_ID_parts) < 2:  # Check if the split resulted in the expected number of parts
                print(f"Skipping malformed protein ID: {protein_info}")
                continue

            protein_ID = protein_ID_parts[1]  # The second part is the protein ID (e.g., Q8H102)
            # variables for each column
            polyx_type = parts[3]
            start = int(parts[1])
            end = int(parts[2])
            length = end - start + 1            # Calculating the total length of polyx regions of each region
            # Update the data for polyx count, types and length:
            polyxdata[protein_ID]["polyx_count"] += 1          # Count goes up 1 for every line with that protein ID
            polyxdata[protein_ID]["polyx_types"].append(polyx_type)    # Make a list of each polyx type
            polyxdata[protein_ID]["polyx_lengths"].append(length)
            polyxdata[protein_ID]["total_length"] += length         # Length of each polyX is added to the total length

def Create_final_doc(mapped, outputfile):    #Code to create final document by adding polyx info to the last output file
    with open(mapped, 'r') as input, open(outputfile, 'w') as output:
        output.write(f"Genename\tUniProtID\tLength\tHk\tPolyx_count\tPolyx_types\tPolyx_lengths"
                     f"\tTotal_length\tPption_polyx\tCount_grouped\n") # Header
        next(input)     # Skip header when reading input file
        for line in input:      # Go through each line of the file
            parts = line.strip("\n").split("\t")    # For each line, save each column in a variable
            gene_name = parts[0]
            uniprot_id = parts[1]
            length = parts[2]
            housekeeping = parts[3]
            #score = (annotation_scores.get(uniprot_id, "No score"))
            if uniprot_id in polyxdata:     # If the protein has a polyx region, write polyx data into output file
                data = polyxdata[uniprot_id]
                polyx_count = data["polyx_count"]
                polyx_types_combined = "/".join(data["polyx_types"])    # Join polyxtypes (stored as set) with / as divider
                polyx_lengths = "/".join(map(str, data["polyx_lengths"]))
                total_length = data["total_length"]
                aa_percent = round(int(total_length)/int(length), 4)
                if polyx_count < 2:
                    output.write(f"{gene_name}\t{uniprot_id}\t{length}\t{housekeeping}\t"
                                 f"{polyx_count}\t{polyx_types_combined}\t{polyx_lengths}\t{total_length}\t{aa_percent}\t{polyx_count}\n")
                else:
                    output.write(f"{gene_name}\t{uniprot_id}\t{length}\t{housekeeping}\t"
                                 f"{polyx_count}\t{polyx_types_combined}\t{polyx_lengths}\t{total_length}\t{aa_percent}\t>1\n")
            else:   # If protein has no polyx region, put 0 instead for poly x count, type and length
                output.write(f"{gene_name}\t{uniprot_id}\t{length}\t{housekeeping}\t0\t-\t0\t0\t0\t0\n")

#main processing function for polyx data
def Process_polyxdata():
for organism in constants.organisms:  # Loop through each organism
        mapped_file = constants.FILE_PATHS[organism]["MAPPED_HK_FILE"]
        polyx_file = constants.FILE_PATHS[organism]["POLYX_FILE"]
        output_file = constants.FILE_PATHS[organism]["MAPPED_HK_POLYX_FILE"]

        if not os.path.exists(mapped_file):
            print(f"Skipping {organism} - No mapped file found!")
            continue
        if not os.path.exists(polyx_file):
            print(f"Skipping {organism} - No polyx data file found!")
            continue

        print(f"Processing {organism}...")

        Polyx_dictionary(polyx_file)  # Read polyx scanner output into a dictionary
        Create_final_doc(mapped_file, output_file)  # Generate final file

        print(f"Processed {organism}: created {output_file}")
    
```
## File paths and call function
``` python
Process_polyxdata()
```

# Process reference proteomes and Housekeeping gene list to create a list of proteins with their length and Housekeeping status as attributes
## Import python modules
``` python
import os
import re
from collections import defaultdict
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hr_lib')))
import constants  # Import constants.py from hr_lib
```
## Functions
``` python
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
```
## Running the program on all proteomes in the directory "proteome_dir"
``` python
Process_proteomes()
```

