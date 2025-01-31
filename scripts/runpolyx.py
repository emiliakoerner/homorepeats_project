# Run polyx scanner on all proteomes in data/raw/proteomes
# Import python modules
import subprocess
import os
import sys
import shutil
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(base_dir, "hr_lib"))
import constants  # Import constants.py from hr_lib

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
	
run_polyx()
