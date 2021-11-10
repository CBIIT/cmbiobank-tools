cmb-products
============

`cmb-products.py` is a script to automate the creation of ID assignment files
and other metadata products that the Cancer Moonshot Biobank needs to 
instantiate and share.

It is a wrapper around the R script [rave-reduce.r](/rave-reduce). It takes
care of a number of bookkeeping tasks and issues a ".audit" file associated
with each product that records the input data files and directories used to
create the corresponding product. 

The file [cmb-products.yaml](./cmb-products.yaml) configures a number of required
source and destination locations.

    usage: cmb-products.py [-h] [--dry-run] [--conf-file CONF_FILE] [--verbose]
                           [--quiet] [--stage-dir STAGE_DIR] [--fake-file]
    
    optional arguments:
      -h, --help            show this help message and exit
      --dry-run             log rave-reduce commands, but do not run them
      --conf-file CONF_FILE
      --verbose, -v
      --quiet, -q
      --stage-dir STAGE_DIR
                            directory for staging built products
      --fake-file           touch files in stage directory

