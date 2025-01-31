# Run polyx scanner on all proteomes in data/raw/proteomes
## Import python modules
``` python
import subprocess
import os
import sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(base_dir, "hr_lib"))
import constants  # Import constants.py from hr_lib
```

## Functions
``` python
def run_polyx():
    for organism in constants.organisms:  # Loop through each organism
        print(f"Running PolyX for {organism}...")

        # Get file paths from constants.py
        proteome_path = constants.file_paths[organism]['PROTEOME_FILE']
        polyx_output_path = constants.file_paths[organism]['POLYX_FILE']
	polyx_output_dir = os.path.dirname(polyx_output_path)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(polyx_output_path), exist_ok=True)

        # Set script path
        polyx_script = os.path.join(base_dir, "scripts", "polyx2", "polyx2_standalone.pl")

        # Construct the command
        command = ["perl", polyx_script, proteome_path]

        try:
            # Run polyx.pl from the output directory
            subprocess.run(command, cwd=polyx_output_dir, check=True)
            print(f"PolyX processing complete for {organism}. Output: {polyx_output_path}")

        except subprocess.CalledProcessError as e:
            print(f"Error running PolyX for {organism}: {e}")
```

## Run
``` python
run_polyx()
```
