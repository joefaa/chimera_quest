Chimera Quest help

Chimera Quest is powered by Oncofuse, BioPython, MySQL and BioSQL. The literature database was populated with information downloaded from the ChimerDB database. The ChimerDB database is itself a compilation of literature references from four literature databases: PubMed, OMIM, Sanger Cancer Genome Project and the Mitelman database.

Running Chimera Quest

Running Chimera Quest is easy, and fun! If you already have the file you need to input, you're most of the way there. For more information about the acceptable input file types, and tissue types see the Oncofuse help section below.

Once you have your file ready, select the file-type from the first radio selector, and the tissue-type from the second radio selector. Then, upload your file and hit Run Oncofuse. A loader icon will appear while the analysis is being performed, and the results window will appear after the analysis is finished.

A report for each oncogenic transcript will be available by clicking the symbol for that fused gene and clicking either Show Oncofuse report, to see the oncofuse report, or Show literature report, to see a report generated from the results of the literature database search.

ChimerDB info

ChimerDB is made available by the Ewha Woman's University, the website is linked here: http://biome.ewha.ac.kr:8080/FusionGene/. The ChimerDB intergrated knowledgebase is available for download at http://biome.ewha.ac.kr:8080/FusionGene/Download.jsp. The section below about the input and output of oncofuse is copied from the Oncofuse read me.

Oncofuse help

Oncofuse is made available by the Universidad de Navarra, the website is linked here: http://www.unav.es/genetica/oncofuse.html. Oncofuse is available for download from github at https://github.com/mikessh/oncofuse/releases/tag/1.1.1. The section below about the input and output of oncofuse is copied from the Oncofuse read me.

Oncofuse help

Oncofuse is made available by the Universidad de Navarra, the website is linked here: http://www.unav.es/genetica/oncofuse.html. Oncofuse is available for download from github at https://github.com/mikessh/oncofuse/releases/tag/1.1.1. The section below about the input and output of oncofuse is copied from the Oncofuse read me.

INPUT

This tool is designed to predict the oncogenic potential of fusion genes found by Next-Generation Sequencing in cancer cells. It also provides information on hallmarks of driver gene fusions, such as expression gain of resulting fusion gene, retained protein interaction interfaces and resulting protein domain functional profile.

Supported tissue types (tissue of origin for gene fusion): EPI (epithelial), HEM (hematopoietic), MES (mesenchymal), AVG (averaged, when tissue of origin is unknown)

Supported input types:

input_type = "coord" (Default format accepted by Oncofuse)

Tab-delimited file with lines containing 5' and 3' breakpoint positions (first nucleotide lost upon fusion) and tissue of origin:

5' chrom \t 5' coord \t 3' chrom \t 3' coord \t tissue_type

For this format tissue of origin is set individually for each entry in input file and tissue_type argument should be set as "-"

input_type = "tophat"

Default output file of Tophat-fusion and Tophat2 (usually fusions.out file in results folder). Tophat-fusion-post is also supported with extended input type argument "tophat-post".

input_type = "fcatcher"

Default output file of FusionCatcher software. Tissue type has to be set using tissue_type argument.

input_type = "rnastar"

Default output file of RNASTAR software. Data is pre-filtered based on number of spanning N>=1 and total number of supporting reads M>=2 reads. These parameters could be changed with extended input type argument "rnastar-N-M". Tissue type has to be set using tissue_type argument.

OUTPUT

A tab-delimited table with the following columns

SAMPLE_ID	The ID of sample for tophat-post, input file name otherwise

FUSION_ID	The original line number in input file

TISSUE	As specified by library argument or in 'coord' input file

GENOMIC	Chromosomal coordinates for both breakpoints (as in input file)

SPANNING_READS	Number of reads that cover fusion junction

ENCOMPASSING_READS	Number of reads that map discordantly with one mate mapping to 5'FPG (fusion partner gene) and other mapping to 3'FPG

5_FPG_GENE_NAME	The HGNC symbol of 5' fusion partner gene

5_IN_CDS?	Indicates whether breakpoint is within the CDS of this gene

5_SEGMENT_TYPE	Indicates whether breakpoint is located within either exon or intron

5_SEGMENT_ID	Indicates number of exon or intron where breakpoint is located

5_COORD_IN_SEGMENT	Indicates coordinates for breakpoint within that exon/intron

5_FULL_AA	Length of translated 5' FPG in full amino acids

5_FRAME	Frame of translated 5' FPG

(Same as 7 lines above for the 3' fusion partner gene)

FPG_FRAME_DIFFERENCE	The resulting frame of fusion gene, if equals to 0 then the fusion is in-frame

P_VAL_CORR	The Bayesian probability of fusion being a passenger (class 0), given as Bonferroni-corrected P-value

DRIVER_PROB	The Bayesian probability of fusion being a driver (class 1)

EXPRESSION_GAIN	Expression gain of fusion calculated as [(expression of 5' gene)/(expression of 3' gene)]-1

5_DOMAINS_RETAINED	List of protein domains retained in 5' fusion partner gene

3_DOMAINS_RETAINED	List of protein domains retained in 3' fusion partner gene

5_DOMAINS_BROKEN	List of protein domains that overlap breakpoint in 5' fusion partner gene

3_DOMAINS_BROKEN	List of protein domains that overlap breakpoint in 3' fusion partner gene

5_PII_RETAINED	List of protein interaction interfaces retained in 5' fusion partner gene

3_PII_RETAINED	List of protein interaction interfaces retained in 3' fusion partner gene

CTF, G, H, K, P and TF	Corresponding functional family association scores (log-transformed, scaled to the largest score obtained from classifier training set).
