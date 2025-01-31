# Process Polyx scanner information and create a new file with the Polyx information for each protein
# Import python modules
import os
from collections import defaultdict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hr_lib')))
import constants  # Import constants.py from hr_lib

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

Process_polyxdata()


