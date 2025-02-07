# README for scripts related to Homorepeats

# Input parameters:
# Input parameters:
If you want to select organisms manually:
python script.py --organisms UP00xxxxx UP00xxxxxx
If you want to select entire taxa manually:
python script.py --taxa Bacteria Viruses
If no arguments are provided when running the script, it falls back to SELECTED_ORGANISMS in constants.py. If SELECTED_ORGANISMS is None, it falls back to SELECTED_TAXA. Both can be edited in constants.py.

# Runpolyx.py: Runs PolyX2 Scanner on all organisms in SELECTED_ORGANISMS or _TAXA and saves the Output outside of the repository. See constants.py for paths
- Input: Reference proteomes (.fasta)
- Output: Polxydata file (.txt) -> Polyx scanner output. Saved in output/homorepeats/polyxdata/{taxon}/{organism}
- Dependencies: constants.py and load_organisms.py

## Functions
- decompress_fasta(gz_file): Decompresses proteome file for processing
- Shorten_filename(filename, max_length=150): Shortens output file name to a maximum of 150 characters to avoid crashing due to extraordinarily long organism names
- run_polyx.py: Runs polyx2_standalone.pl on all organisms selected in constants.py. Calls decompress.fasta and Shorten_filename while doing so. Saves output files as UPID_organism_name_polyx.txt

# process_proteomes_and_polyxdata.py: Reads proteome file and corresponding polyx file (Output from runpolyx.py) and creates a new file with a list of Proteins and their polyx regions.
- Input: Reference proteomes (.fasta) and respective polyx data files (output from runpolyx.py)
- Output: List of proteins with their length and polyx data as attributes. Saved in output/homorepeats/proteomes_hrs/{taxon}/{organism}
- Dependencies: constants.py and load_organisms.py

## Functions
- Proteome_dictionary(proteome): Stores data from proteome file in a dictionary for easy and fast processing.
- Polyx_dictionary(input): Stored polyxdata (output from run_polyx.py) in a dictionary for easy and fast processing.
- Create_final_doc(outputfile): Creates a new document containing a list of all proteins in the proteomedict, adds their length and polyxdata from the polyxdict.
- Processing_proteomes: Processes all proteomes selected in constants.py by finding the correct folder and file path for each organism and polyx file, defining the output path dynamically and calling all 3 functions from above.
