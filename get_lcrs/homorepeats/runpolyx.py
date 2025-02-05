# Import python modules
import subprocess
import os
import shutil
import sys
import gzip
sys.path.append(os.path.abspath('../../lib'))
from lib.load_organisms import get_filtered_organisms
from lib.constants import *

def decompress_fasta(gz_file):  # Decompress proteome file
    uncompressed = gz_file.replace(".gz", "")
    if not os.path.exists(uncompressed):
        with gzip.open(gz_file, 'rb') as f_in, open(uncompressed, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return uncompressed


# Input: Proteome
# Output: Polyx output
def run_polyx():    # Runs polyx2_standalone.pl on all organisms in SELECTED_ORGANISMS defined in constants.py
    polyx_script = os.path.join(HR_DIR, "polyx2", "polyx2_standalone.pl")
    organisms = get_filtered_organisms()    # Calls function from load_organisms.py

    for up_id, data in organisms.items():
        category = data["category"]
        fasta_gz_path = data["fasta_path"]
        organism_name = data["name"].replace(" ", "_").replace("\'", "").replace("/", "_")  # Sanitize file name

        fasta_path = decompress_fasta(fasta_gz_path)    # Decompress fasta file by calling the function

        organism_output_dir = os.path.join(POLYX_DIR, category, up_id)  # Define output folder
        os.makedirs(organism_output_dir, exist_ok=True)

        output_file = os.path.join(organism_output_dir, f"{up_id}_{organism_name}_polyx.txt")   # constructs file name from
                                                                                    # output path, UP ID and organism name
        print(f"Running PolyX for {up_id} ({data['name']})...")

        # Change working directory to output folder to run PolyX
        os.chdir(organism_output_dir)

        command = ["perl", polyx_script, fasta_path]    # command to run the perl script
        try:
            # Run polyx.pl
            subprocess.run(command, check=True)
            temp_output = "output_polyx.txt"    # save output file in a variable

            # Move and rename output file
            if os.path.exists(temp_output):
                shutil.move(temp_output, output_file)
                print(f"PolyX completed for {up_id}. Output saved as {output_file}")
            else:
                print(f"Error: output_polyx.txt was not created for {up_id}.")

        except subprocess.CalledProcessError as e:
            print(f"Error running PolyX for {up_id}: {e}")

run_polyx()
