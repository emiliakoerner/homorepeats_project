# README for scripts related to Housekeeping genes

# Input parameters:
If you want to select organisms manually:
python script.py --organisms UP00xxxxx UP00xxxxxx
If you want to select entire taxa manually:
python script.py --taxa Bacteria Viruses
If no arguments are provided when running the script, it falls back to SELECTED_ORGANISMS in constants.py. If SELECTED_ORGANISMS is None, it falls back to SELECTED_TAXA. Both can be edited in constants.py.

# Mapping_hklists_to_Uniprot.py: Mapping housekeeping lists from different sources to UniProt using underlying data from UniProt ID mapping tool
- Input: Housekeeping list and mapping file for each organism (.txt), both defined in constants.py
- Output: Mapped Housekeeping list for further processing (.txt)
- Dependencies: constants.py and load_organisms.py

## Functions
- Housekeeping_mapping_uniprot(hk_file, mapping_file, output_file): Maps Housekeeping gene lists to Uniprot using the underlying data files of the Uniprot Mapping tool. Paths to mapping files are defined in constants.py and do not need to be changed as long as the repository structure is maintained.


# Create_hrs_hk_file.py: Adds Housekeeping Status to proteome_hrs files (List of Proteins for each proteome with polyxdata)
- Input: {organism}_hrs file (.tsv), list of proteins with length and polyxdata
- Output: {organism}_hrs_hk file (.tsv), list of proteins with length, polyxdata and housekeeping status
- Dependencies: constants.py and load_organisms.py

## Functions
- Process_proteomes: Finds proteome_hrs file for each organism in SELECTED_ORGANISMS or SELECTED_TAXA and defines the file paths dynamically. Processing function that calls the mapping function
- Map_to_hklist(proteome_hrs_path, hk_list_path, output_path): Checks for each protein if it is Housekeeping and creates a new file with an additional column containing the Hk status
