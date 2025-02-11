# README for library scripts constants.py and load_organisms.py

- constants.py: Defines all necessary paths for running the scripts in this repository. Paths to files in this repository are defined relatively to the current working Directory. Do not Change the structure of this repository or define the paths manually in this script.

Configurations:
OUTPUT_BASE_DIR: Your base Directory for all Output files. Default: Same Directory as the root Directory of this repository. Adjust this here - the Folders in this Directory are defined relative to this base dir.
INPUT_BASE_DIR: Your base Directory for the Input files (Reference proteomes). Default: Same Directory as the root Directory of this repository. Adjust this here - the Folders in this Directory are defined relative to this base dir.

SELECTED_ORGANISMS: Organisms that will be processed by the main scripts.
SELECTED_TAXA: Taxa that will be processed by the main scripts.
if SELECTED_ORGANISMS is None, python will consider SELECTED_TAXA instead

- load_organisms.py: Parses README files from Uniprot to find each organisms name, proteome ID and Tax ID, stores data in a dictionary. Then looks for organisms in REF_DIR (folder with reference proteomes) and saves the proteome ID, taxon and the path to the fasta.gz folder in another dictionary. Then filters organisms, using the passed arguments or SELECTED_ORGANISMS or SELECTED_TAXA to filter for the desired organisms.