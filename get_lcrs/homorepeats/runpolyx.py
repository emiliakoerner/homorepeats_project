# Import required modules
import subprocess
import os
import shutil
import sys
import gzip
import concurrent.futures  # For parallel execution
import tempfile

sys.path.append(os.path.abspath('../../lib'))
from load_organisms import get_filtered_organisms
from constants import *


def read_fasta_from_gz(gz_file):  # Decompress proteome file
    with gzip.open(gz_file, 'rt') as f_in:  # 'rt' = read text mode
        return f_in.read()  # Return file content as a string


def Shorten_name(organism, max_length=200):
    if len(organism) > max_length:
        organism = organism[:max_length]
    return organism

def process_organism(up_id, data):
    """Runs PolyX for a single organism in parallel"""
    polyx_script = os.path.join(HR_DIR, "polyx2", "polyx2_standalone.pl")
    category = data["category"]
    fasta_gz_path = data["fasta_path"]

    # Sanitize organism name for filenames
    raw_organism_name = data["name"].replace(" ", "_").replace("\'", "_").replace("/", "_").replace(":",
                                                                                                    "_")  # Sanitize file name
    safe_organism_name = Shorten_name(raw_organism_name)

    fasta_content = read_fasta_from_gz(fasta_gz_path)  # Decompress fasta file

    organism_output_dir = os.path.join(POLYX_DIR, category, up_id)  # Define output folder
    os.makedirs(organism_output_dir, exist_ok=True)

    filename = f"{up_id}_{safe_organism_name}_polyx.txt"
    output_file = os.path.join(organism_output_dir, filename)

    print(f"Running PolyX for {up_id} ({data['name']})...")

    """# Change working directory to output folder to run PolyX
    os.chdir(organism_output_dir)"""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".fasta") as temp_fasta:
        temp_fasta.write(fasta_content.encode())
        temp_fasta = temp_fasta.name

    command = ["perl", polyx_script, temp_fasta]  # Command to run the Perl script
    try:
        subprocess.run(command, check=True)  # Run PolyX
        temp_output = "output_polyx.txt"  # Temporary output file

        # Move and rename output file
        if os.path.exists(temp_output):
            shutil.move(temp_output, output_file)
            print(f"PolyX completed for {up_id}. Output saved as {output_file}")
        else:
            print(f"Error: output_polyx.txt was not created for {up_id}.")

    except subprocess.CalledProcessError as e:
        print(f"Error running PolyX for {up_id}: {e}")

# Set the number of parallel processes (adjust based on your CPU)
def run_polyx(max_workers = 4):
    """Runs PolyX in parallel for all selected organisms"""
    organisms = get_filtered_organisms()  # Load selected organisms

    # Use a process pool to parallelize execution
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_organism, organisms.keys(), organisms.values())

if __name__ == '__main__':
    import concurrent.futures  # Import inside main to avoid issues on Windows

    run_polyx()

