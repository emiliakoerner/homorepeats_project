# The functional relevance of amino acid homorepeats overcomes the evolutionary selective pressure that keeps housekeeping protein sequences shorter
This repository contains the data and code needed to reproduce the results reported in our paper.

**README.md** guides you all over this repository. **The structure of this repository is the next:** 
 - **data** Data needed to run the scripts and recreate the results.
        - **raw** Data downloaded from sources like UniProt
        - **processed** Processed data that is not a result.
 - **scripts** Code for recreating results (Python scripts)
        - **suppl_tables** for the supplementary material.
 - **results** Files with lists of proteins and relevant attributes, figures.

   ---
### Data: the annotations were downloaded from public repositories

#### Proteins
The [reference proteomes](https://www.uniprot.org/proteomes/?query=*&fil=reference%3Ayes) were downloaded from the Universal Protein Resource ([Uniprot](https://www.uniprot.org/)). Each proteome has a unique Uniprot-identifier (UPID). A [description](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README) of the proteomes is also provided. It contains a table with information on every proteome: UPIDs, taxonomy_ids, species names, etc. All the reference proteomes were downloaded from [Uniprot FTP repository](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/) on ...2024. Note that Uniprot is updated regularly, every eight weeks. 

### Housekeeping gene lists
The species-specific housekeeping gene lists were obtained from different publications for [Homo sapiens](link), [Mus musculus](link), ...

### main_work: Folder with separate files for each consecutive piece of code
- Mapping_hklists_to_Uniprot.md: Adds matching UniProt IDs (from a mapping file downloaded from Uniprot) to a list of housekeeping genes (Identifiers like WormBaseID, GeneName, ...) for further downstream mapping to the respective proteome
- - Process_polyx.md: 
