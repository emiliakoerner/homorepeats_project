# The functional relevance of amino acid homorepeats overcomes the evolutionary selective pressure that keeps housekeeping protein sequences shorter
This repository contains the data and code needed to reproduce the results reported in our paper.

**README.md** guides you all over this repository. **The structure of this repository is the next:** 
 - **data** contains file needed to run the scripts and recreate the results.
        - **raw** contains data downloaded from sources like UniProt
        - **processed** contains processed data that is not a result.
 - **scripts** contains code for recreating results (Python scripts)
	- **polyx2** contains the Polyx2 Scanner downloaded from [here](https://cbdm-01.zdv.uni-mainz.de/~munoz/polyx2/)
	- README.md for scripts
 - **results** contains files with lists of proteins and relevant attributes, figures.

   ---
### Data: the annotations were downloaded from public repositories

#### Proteins
The [reference proteomes](https://www.uniprot.org/proteomes/?query=*&fil=reference%3Ayes) were downloaded from the Universal Protein Resource ([Uniprot](https://www.uniprot.org/)). Each proteome has a unique Uniprot-identifier (UPID). A [description](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README) of the proteomes is also provided. It contains a table with information on every proteome: UPIDs, taxonomy_ids, species names, etc. All the reference proteomes were downloaded from [Uniprot FTP repository](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/) on ...2024. Note that Uniprot is updated regularly, every eight weeks. 

### Housekeeping gene lists
The species-specific housekeeping gene lists were obtained from different publications for [Homo sapiens](https://pubmed.ncbi.nlm.nih.gov/32663312/), [Mus musculus](https://pubmed.ncbi.nlm.nih.gov/32663312/), [Drosophila melanogaster](http://www.biomedcentral.com/1471-2164/7/277), [Caenorhabditis elegans](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010295), [Saccharomyces cerevisiae](https://www.nature.com/articles/nature00935), [Escherichia coli](https://journals.asm.org/doi/full/10.1128/jb.185.19.5673-5684.2003) and [Arabidopsis thaliana](https://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-9-438).

### data: Folder with all files needed to recreate the results of the 7 organisms mentioned above.
- raw: data obtained from the sources mentioned above or downloaded from UniProt.
	- proteomes: Reference proteomes for each of the 7 organisms, downloaded on January 7 2025 (October 8 2024 in case of human).
	- hk_unmapped: Housekeeping gene lists for each of the 7 organisms. The lists for human and mouse can be downloaded from [here](https://housekeeping.unicamp.br/?download). The lists for [C. elegans](https://doi.org/10.1371/journal.pcbi.1010295.s014), [A. thaliana](https://static-content.springer.com/esm/art%3A10.1186%2F1471-2164-9-438/MediaObjects/12864_2008_1631_MOESM13_ESM.xls) and [E. coli](https://www.genome.wisc.edu/Gerdes2003/supplementary_table.html) can be directly downloaded from the source publication. Yeast was obtained from the [DEG database](https://tubic.org/deg/public/index.php/organism/eukaryotes/DEG2001.html) which uses the publication linked above as a source. The list for D. melanogaster was requested directly from an author of the source publication mentioned above. All lists were extracted from the source material and brought into a consistent format for processing: A text file with one single column containing the Gene/Protein identifiers with no header.
	- mapping_files: Contains the underlying data from the [UniProt ID mapping tool](https://www.uniprot.org/id-mapping) downloaded on the January 6 2025 for each organism separately. These files are used to map each Identifier from the Housekeeping gene lists to a UniProt ID and therefore to a protein in the proteome. 
- processed:
	- housekeeping_lists: Housekeeping gene lists from "hk_unmapped", with the corresponding UniProt IDs. Created with Mapping_hklists_to_Uniprot.py
	- polydata: Output files of the perl program "PolyX2" [(Mier and Andrade-Navarro, 2022)](https://www.mdpi.com/2073-4425/13/5/758), Created with runpolyx.pl. Contain every polyx region in the respective reference proteome with the threshold 8/10.

### scripts: Folder with separate files for each consecutive piece of code
- README.md: Read for a markdown guide on running the scripts
- polyx2: Contains the perl script PolyX2 scanner [(Mier and Andrade-Navarro, 2022)](https://www.mdpi.com/2073-4425/13/5/758) downloaded from [here]
(https://cbdm-01.zdv.uni-mainz.de/~munoz/polyx2/) including a README file.
- runpolyx.py: Python script to run PolyX2 on every reference proteomes in data/raw/proteomes/.
- constants.py: Python script to establish file paths needed for the other scripts. Needs to be run first before running any other script.
- Mapping_hklists_to_Uniprot.py: Adds matching UniProt IDs (from a mapping file downloaded from Uniprot) to all lists of housekeeping genes in data/raw/hk_unmapped/ (Identifiers like WormBaseID, GeneName, ...) for further downstream mapping to the respective proteome.
- Proteome_processing.py: Creates a text file containing a list of proteins from the proteome fasta file, adding the attributes protein length and housekeeping status after checking if the Uniprot ID exists in the respective housekeeping gene list. Runs automatically on all organisms in data/. See results/mapped_hk
- Process_polyx.py: Adds Polyx region information to the list of proteins. Runs automatically on all organisms in data/ See results/mapped_hk_polyx

### results
- tables: Result files generated with the scripts in scripts/.
	- mapped_hk: A list of proteins from the reference proteomes with 4 columns: Gene name, UniProt ID, protein length and Housekeeping status (1 = yes, 0 = no) for each organism.
	- mapped_hk_polyx: The files from mapped_hk plus the polyx data for each protein. 6 additional columns: Polyx_count (number of polyx regions in the protein), Polyx_types (All polyx region types in the protein; each polyx region is listed individually, even if the amino acid has already been listed), Polyx_lengths (Length of each polyx region in the protein), Total_length (total length of all polyx regions in the protein), Pption_polyx (Proportion of amino acids in the proteins that are part of a polyx region) and Count_grouped (Number of polyx regions in the protein, categorized in 0, 1 and >1 for analysis purposes).
- figures: Figures created with R from the result files in results/tables/mapped_hk_polyx