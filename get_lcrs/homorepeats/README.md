# README for scripts related to Homorepeats

# Input parameters:
If you want to select organisms manually:
python script.py --organisms UP00xxxxx UP00xxxxxx
If you want to select entire taxa manually:
python script.py --taxa Bacteria Viruses
If no arguments are provided when running the script, it falls back to SELECTED_ORGANISMS in constants.py. If SELECTED_ORGANISMS is None, it falls back to SELECTED_TAXA. Both can be edited in constants.py.

# Runpolyx.py: Runs PolyX2 Scanner on all organisms in SELECTED_ORGANISMS or _TAXA and saves the Output outside of the repository. See constants.py for paths
- Input: Reference proteomes (.fasta)
- Output: Polxydata file (.txt) -> Polyx scanner output. Saved in output/homorepeats/polyxdata/{taxon}/{organism}
- Dependencies: constants.py and load_organisms.py, Perl and Bioperl
- Attention: Will decompress the proteome files in the input folder, adding the unpacked file to the folder of each organism.

## Functions
- Read_fasta_from_gz(gz_file): Reads fasta file from the gz Folder without unpacking it permanently
- Shorten_name(filename, max_length=150): Shortens organism name to a maximum of 200 characters to avoid crashing due to extraordinarily long file names
- process_organism: Runs polyx2_standalone.pl on all organisms selected in constants.py. Calls Read_fasta_from_gz and Shorten_name while doing so. Saves output files as UPID_organism_name_polyx.txt
- run_polyx.py: Executes process_organisms using multiple CPU cores to Speed up the process. Uses 4 cpu cores in parallel 

# process_proteomes_and_polyxdata.py: Reads proteome file and corresponding polyx file (Output from runpolyx.py) and creates a new file with a list of Proteins and their polyx regions.
- Input: Reference proteomes (.fasta) and respective polyx data files (output from runpolyx.py)
- Output: List of proteins with their length and polyx data as attributes. Saved in output/homorepeats/proteomes_hrs/{taxon}/{organism}
- Dependencies: constants.py and load_organisms.py

## Functions
- Proteome_dictionary(proteome): Stores data from proteome file in a dictionary for easy and fast processing.
- Polyx_dictionary(input): Stored polyxdata (output from run_polyx.py) in a dictionary for easy and fast processing.
- Create_final_doc(outputfile): Creates a new document containing a list of all proteins in the proteomedict, adds their length and polyxdata from the polyxdict.
- Processing_proteomes: Processes all proteomes selected in constants.py by finding the correct folder and file path for each organism and polyx file, defining the output path dynamically and calling all 3 functions from above.
