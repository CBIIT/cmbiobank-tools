# Cancer Moonshot Biobank to CTDC Transformer

v0.2 (23 Apr 2025)


The file [cmb-transform-ctdc.r](./cmb-transform-ctdc.r) is an R script that uses a [mapping spreadsheet](cmb-dbgap-to-ctdc-mapping.v03-28-25.xlsx) to transform Biobank data in dbGaP submission spreadsheets to TSV (.txt) files suitable for the CRDC Bento data loader.

The transformation as of v0.2 performs the following actions:

* Converts source (Biobank dbGaP) file column names to target (CTDC model) Property names;
* Copies the data values for the desired columns (given in the mapping file) to the appropriate records in the loader files;
* Regroups the desired columns from source data under desired Node in the target model, by creating per-node CSVs, named after the Nodes;
* Correctly maintains the subject id and specimen id relationships with the data records;

The data values themselves are not yet transformed to CTDC model values; this is a planned task that requires data mappings.

## Usage

[R](https://www.r-project.org/) should be installed, along with the following packages (use `install.packages()`):
* tidyverse
* readxl
* optparse
* config

In the repo directory, typing

    ./cmb-transform-ctdc.r --help

should result in this usage message:

    Usage: ./cmb-transform-ctdc.r [options]

    Options:
    	-d DIR, --datadir=DIR
    		Directory containing dbGaP Excel files [default: NULL]

    	-m FILE, --mapfile=FILE
    		Mapping file path [default: NULL]

    	-o DIR, --outdir=DIR
    		Output directory for TSV files [default: NULL]

    	-h, --help
    		Show this help message and exit

Defaults for each option can be set in a `config.yml` file in the working directory. 
See this [example](./config.yml).
