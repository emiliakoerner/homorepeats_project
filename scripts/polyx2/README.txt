##  PolyX Scanner // Created by Pablo MIER on 2020 // Copyright © 2020 Pablo MIER. All rights reserved.

##  Description --> The program looks for all polyX in the protein sequence from a given file using a threshold in the form of Y/Z, where Y is the minimum number of same amino acid in window Z. Overlapping polyX are joined; i.e. AAxxAAAAAAxxAA is one polyA using threshold 8/10, although not all of its windows match the threshold. The default threshold value is 8/10.

##	Usage --> perl polyx2_standalone.pl INPUT MINIMUM MAXIMUM

##	Input1 --> INPUT = Fasta file
##	Input2 --> MINIMUM = Minimum number of same amino acid
##	Input3 --> MAXIMUM = Window length

##	Output --> output_polyx.txt --> List of polyX found in input fasta file, with protein ID and coordinates

##	Dependencies --> BioPerl library "Bio:SeqIO"

##	Example --> perl polyx2_standalone.pl hsa.fasta 8 10
##	Results --> 2870 polyX are found in less than 20 seconds from the 20600 human proteins used as input

