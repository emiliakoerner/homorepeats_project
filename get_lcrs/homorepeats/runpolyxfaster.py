# Import required modules
import subprocess
import os
import shutil
import sys
import gzip
import concurrent.futures  # For parallel execution

sys.path.append(os.path.abspath('../../lib'))
from lib.load_organisms import get_filtered_organisms
from lib.constants import *


def decompress_fasta(gz_file):  # Decompress proteome file
    uncompressed = gz_file.replace(".gz", "")
    if not os.path.exists(uncompressed):
        with gzip.open(gz_file, 'rb') as f_in, open(uncompressed, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return uncompressed


def Shorten_filename(filename, max_length=150):
    return filename[:max_length] if len(filename) > max_length else filename


def process_organism(up_id, data):
    """Runs PolyX for a single organism in parallel"""
    polyx_script = os.path.join(HR_DIR, "polyx2", "polyx2_standalone.pl")
    category = data["category"]
    fasta_gz_path = data["fasta_path"]

    # Sanitize organism name for filenames
    organism_name = data["name"].replace(" ", "_").replace("\'", "_").replace("/", "_").replace(":", "_")

    fasta_path = decompress_fasta(fasta_gz_path)  # Decompress fasta file

    organism_output_dir = os.path.join(POLYX_DIR, category, up_id)  # Define output folder
    os.makedirs(organism_output_dir, exist_ok=True)

    raw_filename = f"{up_id}_{organism_name}_polyx.txt"
    safe_filename = Shorten_filename(raw_filename)
    output_file = os.path.join(organism_output_dir, safe_filename)

    print(f"Running PolyX for {up_id} ({data['name']})...")

    # Change working directory to output folder to run PolyX
    os.chdir(organism_output_dir)

    command = ["perl", polyx_script, fasta_path]  # Command to run the Perl script
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


def run_polyx():
    """Runs PolyX in parallel for all selected organisms"""
    organisms = get_filtered_organisms()  # Load selected organisms

    # Set the number of parallel processes (adjust based on your CPU)
    max_workers = min(4, os.cpu_count())  # Use up to 4 processes or max CPU cores

    # Use a process pool to parallelize execution
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_organism, organisms.keys(), organisms.values())

if __name__ == '__main__':
    import concurrent.futures  # Import inside main to avoid issues on Windows

    run_polyx()

