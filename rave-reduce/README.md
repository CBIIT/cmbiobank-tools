rave-reduce.r
=============

`rave-reduce.r` is a command-line R script for performing various
data reduction tasks on CMB Rave data dumps.

## Usage

    Usage: ./rave-reduce.r [OPTIONS] dumpdir

    Options:
    	-c CONFIG, --config=CONFIG
    		config file (default: config.yml)

    	-s STRATEGY, --strategy=STRATEGY
    		output strategy (default: default)

    	--ids-file=IDS-FILE
    		ids file (rds format) (default: entity_ids.rds)

    	-d PULLDATE, --pulldate=PULLDATE
    		pull date to apply to output

    	-l, --list
    		list strategies with descriptions

    	-h, --help
    		Show this help message and exit

## R Package Dependencies

    library(tidyverse)
    library(lubridate)
    library(readxl)
    library(optparse)
    library(config)

## Structure

The script itself is a mini front-end for tasks that are specified 
and configured in an accompanying [config.yml](/rave-reduce/config.yml) file. 

### config.yml

Each task or "strategy" is configured at the top-level of the YAML
data structure. For example, the "iroc" strategy, which creates an updated metadata file for our imaging partners at IROC-Ohio, is configured as follows:

    iroc:
      description: |
        Create a pipe-delimited file of patient registration metadata required by IROC
      xtbls:
        administrative_enrollment:
          - CTEPID
          - DSSTDAT_ENROLLMENT_RAW
          - CTEP_SDC_MED_V10_CD
          - pub_id
          - up_id
      cra_excel: "cra-users.xlsx"
      output:
        cmb_registration_data_for_iroc.txt:
          strategy: iroc
          delim: "|"

Each top-level strategy configuration object has a `description` text field, an `xtbls` object which lists the Rave tables and fields used in the strategy, and an `output` object, which indicates the files to be generated. The keys of the `output` object are the desired output
file names, and the values indicate the name of the function (defined
in [strategies.r](/rave-reduce/strategies.r) to use to generate the 
data frame to be saved in the file.

Multiple files can be generated by adding further key-value pairs to the `output` object, along with appropriate custom functions in `strategies.r`.

The configuration system uses the [config](https://cran.r-project.org/web/packages/config/vignettes/introduction.html) package under the hood.

### strategies.r

Task-specific functions are "hand-coded" in the [strategies.r](/rave-reduce/strategies.r) file,
which contains a single named list of custom functions. These functions are run in the scope of the `rave-reduce.r` script, and so
have the following variables available at runtime:

* `dta` - a list of [tibbles](https://tibble.tidyverse.org/) corresponding to each Rave table

* `entity_ids` - an identifier mapping [tibble](https://tibble.tidyverse.org/)

* `opts` - a list of command line options and arguments entered at runtime (see the [optparse](https://cran.r-project.org/web/packages/optparse/vignettes/optparse.html) package)

* `config` - a list of options as provided in the YAML configuration for the selected strategy