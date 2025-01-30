# The functional relevance of amino acid homorepeats overcomes the evolutionary selective pressure that keeps housekeeping protein sequences shorter
This repository contains the data and code needed to reproduce the results reported in our paper.

**README.md** guides you all over this repository. **The structure of this repository is the next:** 
 - **data** contains file needed to run the scripts and recreate the results.
        - **raw** contains data downloaded from sources like UniProt
        - **processed** contains processed data that is not a result.
 - **scripts** contains code for recreating results (Python scripts)
        - **suppl_scripts** for the supplementary material.
 - **results** contains files with lists of proteins and relevant attributes, figures.
 - **hr_lib** contains a script with constants used in this repository, like file paths.

   ---
### Data: the annotations were downloaded from public repositories

#### Proteins
The [reference proteomes](https://www.uniprot.org/proteomes/?query=*&fil=reference%3Ayes) were downloaded from the Universal Protein Resource ([Uniprot](https://www.uniprot.org/)). Each proteome has a unique Uniprot-identifier (UPID). A [description](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README) of the proteomes is also provided. It contains a table with information on every proteome: UPIDs, taxonomy_ids, species names, etc. All the reference proteomes were downloaded from [Uniprot FTP repository](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/) on ...2024. Note that Uniprot is updated regularly, every eight weeks. 

### Housekeeping gene lists
The species-specific housekeeping gene lists were obtained from different publications for [Homo sapiens](https://pubmed.ncbi.nlm.nih.gov/32663312/), [Mus musculus](https://pubmed.ncbi.nlm.nih.gov/32663312/), [Drosophila melanogaster](http://www.biomedcentral.com/1471-2164/7/277), [Caenorhabditis elegans](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010295), [Saccharomyces cerevisiae](https://www.nature.com/articles/nature00935), [Escherichia coli](https://journals.asm.org/doi/full/10.1128/jb.185.19.5673-5684.2003) and [Arabidopsis thaliana](https://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-9-438). 

### scripts: Folder with separate files for each consecutive piece of code
- Mapping_hklists_to_Uniprot.md: Adds matching UniProt IDs (from a mapping file downloaded from Uniprot) to a list of housekeeping genes (Identifiers like WormBaseID, GeneName, ...) for further downstream mapping to the respective proteome.
- Proteome_processing.md: Creates a text file containing a list of proteins from the proteome fasta file, adding the attributes protein length and housekeeping status after checking if the Uniprot ID exists in the respective housekeeping gene list. See results/mapped_hk
- Process_polyx.md: Adds Polyx region information to the list of proteins. See results/mapped_hk_polyx

