import os
import csv
from constants import *
import gzip

def discover_organisms():
    #Scan directories and find all organisms (UP IDs) and creates a dictionary with UP IDs as key, taxon category and
    organisms = {}                      # file path as values
    for category in TAXON_CATEGORIES:
        category_path = os.path.join(REF_DIR, category)
        if os.path.exists(category_path):
            for organism_id in os.listdir(category_path):
                organism_path = os.path.join(category_path, organism_id)
                if os.path.isdir(organism_path):  # Ensure it's a folder
                    fasta_file = None
                    for file in os.listdir(organism_path):
                        if file.endswith(".fasta.gz"):
                            fasta_file = os.path.join(organism_path, file)
                            break
                    if fasta_file:
                        #print(f"found fasta file for {organism_id}")
                        organisms[organism_id] = {
                            "category": category,
                            "fasta_path": fasta_file
                    }
                    else: print("fasta file not found for", organism_id)
        else: print("category_path does not exist")
    return organisms

"""def find_fasta_file(organism_dir, up_id):
    for file in os.listdir(organism_dir):
        if file.startswith(up_id) and file.endswith(".fasta"):
            return os.path.join(organism_dir, file)
    return None
"""

def parse_readme():
    # Parse the README file to map Proteome IDs to Organism Names. Returns a dictionary
    proteome_to_name = {}
    with open(README_PATH, "r", encoding="utf-8") as readme_file:
        reader = csv.reader(readme_file, delimiter="\t")
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 8:
                proteome_id = row[0].strip()  # UP number
                organism_name = row[7].strip()  # Species name
                proteome_to_name[proteome_id] = organism_name
    return proteome_to_name

def get_filtered_organisms():
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

# Execution
organisms = get_filtered_organisms()
print("Discovered Organisms:")
for up_id, info in organisms.items():
    print(f"UP ID: {up_id}, Name: {info.get('name', 'Unknown')}, Category: {info['category']}, Fasta Path: {info['fasta_path']}")
