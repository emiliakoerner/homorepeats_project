# Run polyx scanner on all proteomes in data/raw/proteomes
# Import python modules
import subprocess
import os
import shutil
import constants
base_dir = constants.BASE_DIR

def run_polyx():
    polyx_script = os.path.join(base_dir, "scripts", "polyx2", "polyx2_standalone.pl")  # Path to polyx.pl
    output_dir = os.path.join(base_dir, "data", "processed", "polyxdata")  # Directory where output files should go

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for organism in constants.organisms:
        print(f"Running PolyX for {organism}...")

        proteome_path = constants.file_paths[organism]['PROTEOME_FILE']
        print(proteome_path)
        output_file = constants.file_paths[organism]['POLYX_FILE']

        # Change working directory to output folder to run PolyX
        os.chdir(output_dir)

        command = ["perl", polyx_script, proteome_path]

        try:
            # Run polyx.pl
            subprocess.run(command, check=True)
            print("Files in out directory", os.listdir(output_dir))
            # Move and rename output file
            if os.path.exists("output_polyx.txt"):
                shutil.move("output_polyx.txt", output_file)
                print(f"PolyX completed for {organism}. Output saved as {output_file}")
            else:
                print(f"Error: output_polyx.txt was not created for {organism}.")

        except subprocess.CalledProcessError as e:
            print(f"Error running PolyX for {organism}: {e}")

run_polyx()
