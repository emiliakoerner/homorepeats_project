import os
import csv
from constants import *
import argparse

def parse_readme():
    # Parse the README file to map Proteome IDs to Organism Names. Returns a dictionary
    proteome_to_name = {}
    with open(README_PATH, "r", encoding="utf-8") as readme_file:
        reader = csv.reader(readme_file, delimiter="\t")
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 8:
                proteome_id = row[0].strip()  # UP number
                tax_id = row[1].strip()     # taxonomy ID
                organism_name = row[7].strip()  # Species name
                proteome_to_name[proteome_id] = (organism_name, tax_id)
    return proteome_to_name


def discover_organisms():
    #Scan directories and find all organisms (UP IDs) and creates a dictionary with UP IDs as key, taxon category and
    proteome_to_name = parse_readme()
    organisms = {}                      # file path as values
    for category in TAXON_CATEGORIES:
        category_path = os.path.join(REF_DIR, category)
        if os.path.exists(category_path):
            for organism_id in os.listdir(category_path):
                organism_path = os.path.join(category_path, organism_id)
                if os.path.isdir(organism_path):  # Ensure it's a folder
                    fasta_file = None
                    try:
                        organism_name, tax_id = proteome_to_name[organism_id]
                    except KeyError:
                        print(f"Skipping {organism_id}: not an organism")
                        continue
                    for file in os.listdir(organism_path):
                        if file.endswith(f"{tax_id}.fasta.gz"):
                            fasta_file = os.path.join(organism_path, file)
                            break
                    if fasta_file:
                        #print(f"found fasta file for {organism_id} and {tax_id}")
                        organisms[organism_id] = {
                            "category": category,
                            "fasta_path": fasta_file,
                            "tax_id": tax_id
                        }
                    elif organism_id.startswith("UP_"):
                        print("Discovering organisms...")
                    else: print("fasta file not found for", organism_id)
        else: print("category_path does not exist")
    return organisms

"""def find_fasta_file(organism_dir, up_id):
    for file in os.listdir(organism_dir):
        if file.startswith(up_id) and file.endswith(".fasta"):
            return os.path.join(organism_dir, file)
    return None
"""


def get_filtered_organisms():
    # Return only the selected organisms with paths and names by calling the first 2 functions
    parser = argparse.ArgumentParser(description="Filter organisms for processing.")
    parser.add_argument("--organisms", nargs="*", help="List of selected organisms (UP IDs)")
    parser.add_argument("--taxa", nargs="*", choices=TAXON_CATEGORIES, help="Select organisms by taxonomic group")
    args = parser.parse_args()

    all_organisms = discover_organisms()
    name_mapping = parse_readme()

    for up_id in all_organisms:
        if up_id in name_mapping:
            all_organisms[up_id]["name"] = name_mapping[up_id][0]

    if args.organisms:
        selected_organisms = set(args.organisms)
    elif args.taxa:
        selected_organisms = {k for k, v in all_organisms.items() if v["category"] in args.taxa}
    else:
        selected_organisms = SELECTED_ORGANISMS
    if selected_organisms:
        return {k: v for k, v in all_organisms.items() if k in selected_organisms}
    elif SELECTED_TAXA:
        return {k: v for k, v in all_organisms.items() if v["category"] in SELECTED_TAXA}
    else:
        print("Please select one or more organisms or taxa you want to process by adding \"--organisms UP0000xxxx ...\""
              "or \"--taxa Bacteria ...\" to your command when running the script or by specifying them in constants.py.")

# Execution
organisms = get_filtered_organisms()
# Debugging
"""print("Discovered Organisms:")
for up_id, info in organisms.items():
    print(f"UP ID: {up_id}, Name: {info.get('name', 'Unknown')}, Category: {info['category']}, Fasta Path: {info['fasta_path']}")
"""







"""def get_filtered_organisms():
    # Return only the selected organisms with paths and names by calling the first 2 functions
    all_organisms = discover_organisms()
    name_mapping = parse_readme()

    for up_id in all_organisms:
        if up_id in name_mapping:
            all_organisms[up_id]["name"] = name_mapping[up_id]

    if SELECTED_ORGANISMS:
        # Filter organisms based on selection
        return {k: v for k, v in all_organisms.items() if k in SELECTED_ORGANISMS}
    else:
        return {k: v for k, v in all_organisms.items() if v["category"] in SELECTED_TAXA}
"""