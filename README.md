# The functional relevance of amino acid homorepeats overcomes the evolutionary selective pressure that keeps housekeeping protein sequences shorter
This repository contains the data and code needed to reproduce the results reported in our paper.

**README.md** guides you all over this repository. **The structure of this repository is the next:** 
 - **get_lcrs** contains scripts to get low complexity regions for reference proteomes
	- **iupred** for disordered regions identified by Iupred3
	- **homorepeats** for homorepeats identified by PolyX2 Scanner
		- runpolyx.py
		- polyx2
		- process_proteomes_and_polyxdata.py
 - **housekeeping** contains scripts to map housekeeping lists and add housekeeping status to a list of proteins
	- Mapping_hk_lists_to_Uniprot.py
	- Create_hrs_hk_file.py
- **lib**
	- constants.py: Defines paths for this repository relative to the current working Directory and defines Base directories for Input and Output, by Default relative to the repository Directory.
	- load_organisms.py: Loads reference proteomes from a local storage location defined in constants.py
 - **main_tables** contains tables needed as input, like Housekeeping gene lists (before mapping) and mapping files from Uniprot

### Short guide for running scripts
- **Download Reference proteomes** from UniProt while preserving the structure (ftp.uniprot.org/pub/.../Reference_Proteomes_2024/06).
- Edit constants.py to **define your base directories for Input and Output**. Both will be in the same place as this repository by Default. Change Input_base_dir and Output_base_dir to your desired paths, all other paths are relative to these base directories. 
- Run the script **runpolyx.py**, then **process_proteomes_and_polyxdata.py** from /get_lcrs/homorepeats/
- Run the scripts **Mapping_hk_lists_to_Uniprot.py**, then **Create_hrs_hk_file.py** from /housekeeping/ (mind that this only works for the 7 model organisms mentioned below)
- All scripts will use SELECTED_ORGANISMS from constants.py by default. **Pass your desired organisms or taxa as arguments** like this:

python script.py --organisms UP00xxxxx UP00xxxxxx

or

python script.py --taxa Bacteria Viruses

or **configure SELECTED_ORGANISMS or SELECTED_TAXA in constants.py for a permanent solution**. SELECTED_ORGANISMS has to be None for SELECTED_TAXA to be considered.

That's it!

   ---
### Data: the annotations were downloaded from public repositories

#### Proteins
The [reference proteomes](https://www.uniprot.org/proteomes/?query=*&fil=reference%3Ayes) were downloaded from the Universal Protein Resource ([Uniprot](https://www.uniprot.org/)). Each proteome has a unique Uniprot-identifier (UPID). A [description](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README) of the proteomes is also provided. It contains a table with information on every proteome: UPIDs, taxonomy_ids, species names, etc. All the reference proteomes were downloaded from [Uniprot FTP repository](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/) on 29.01.2024. Note that Uniprot is updated regularly, every eight weeks. 

#### Housekeeping gene lists
The species-specific housekeeping gene lists were obtained from different publications for [Homo sapiens](https://pubmed.ncbi.nlm.nih.gov/32663312/), [Mus musculus](https://pubmed.ncbi.nlm.nih.gov/32663312/), [Drosophila melanogaster](http://www.biomedcentral.com/1471-2164/7/277), [Caenorhabditis elegans](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010295), [Saccharomyces cerevisiae](https://www.nature.com/articles/nature00935), [Escherichia coli](https://journals.asm.org/doi/full/10.1128/jb.185.19.5673-5684.2003) and [Arabidopsis thaliana](https://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-9-438).

### main_tables: Folder with files needed to recreate the results of the 7 organisms mentioned above, except the reference proteomes
- hk_unmapped: Housekeeping gene lists for each of the 7 organisms. The lists for human and mouse can be downloaded from [here](https://housekeeping.unicamp.br/?download). The lists for [C. elegans](https://doi.org/10.1371/journal.pcbi.1010295.s014), [A. thaliana](https://static-content.springer.com/esm/art%3A10.1186%2F1471-2164-9-438/MediaObjects/12864_2008_1631_MOESM13_ESM.xls) and [E. coli](https://www.genome.wisc.edu/Gerdes2003/supplementary_table.html) can be directly downloaded from the source publication. Yeast was obtained from the [DEG database](https://tubic.org/deg/public/index.php/organism/eukaryotes/DEG2001.html) which uses the publication linked above as a source. The list for D. melanogaster was requested directly from an author of the source publication mentioned above. All lists were extracted from the source material and brought into a consistent format for processing: A text file with one single column containing the Gene/Protein identifiers with no header.
- mapping_files: Contains the underlying data from the [UniProt ID mapping tool](https://www.uniprot.org/id-mapping) downloaded on the January 6 2025 for each organism separately. These files are used to map each Identifier from the Housekeeping gene lists to a UniProt ID and therefore to a protein in the proteome. 


### get_lcrs: Contains scripts to fetch low complexity regions via the perl program "PolyX2" [(Mier and Andrade-Navarro, 2022)](https://www.mdpi.com/2073-4425/13/5/758) or with IUPred3
- **iupred**
- **homorepeats**
	- polyx2: Contains the perl script PolyX2 scanner [(Mier and Andrade-Navarro, 2022)](https://www.mdpi.com/2073-4425/13/5/758) downloaded from [here]
(https://cbdm-01.zdv.uni-mainz.de/~munoz/polyx2/) including a README file. Needs Perl + BioPerl
	- runpolyx.py: Python script to run PolyX2 on every reference proteomes defined in constants.py.
	- Process_proteomes_and_polyxdata.py: Creates a list of Proteins from the proteome fasta file and adds polyxdata from the output of runpolyx.py

### lib: Files need to run the main work
- constants.py: Python script to establish file paths needed for the other scripts. Select organisms you want to process here in SELECTED_ORGANISMS and define your desired base directories with OUTPUT_BASE_DIR and INPUT_BASE_DIR
- load_organisms.py: Finds proteome files, collects them in a dictionary, matches UP IDs to scientific organism names and returns the organisms selected in constants.py
