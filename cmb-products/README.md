cmb-products
============

`cmb-products.py` is a script to automate the creation of ID assignment files
and other metadata products that the Cancer Moonshot Biobank needs to 
instantiate and share.

It is a wrapper around the R script [rave-reduce.r](/rave-reduce). It takes
care of a number of bookkeeping tasks and issues a ".audit" file associated
with each product that records the input data files and directories used to
create the corresponding product. 

The conf-file [cmb-products.yaml](./cmb-products.yaml.sample) configures a number of required
source and destination locations.

    usage: cmb-products.py [-h] [--dry-run] [--conf-file CONF_FILE] [--log-file LOG_FILE]
    		       [--no-log-file] [--verbose] [--quiet] [--distribute-only]
    		       [--distribute] [--stage-dir STAGE_DIR] [--fake-file]
    
    optional arguments:
      -h, --help            show this help message and exit
      --dry-run             log rave-reduce commands, but do not run them
      --conf-file CONF_FILE
      --log-file LOG_FILE   Append log to named file
      --no-log-file         Do not log to file
      --verbose, -v
      --quiet, -q
      --distribute-only     Do not run rave-reduce workflow, use currently
                            staged products only
      --distribute          push products to delivery locations
      --stage-dir STAGE_DIR
                           	directory for staging built products
      --fake-file           touch files in stage directory

Default for `--conf-file` option is `cmb-products.yaml`.
Default for `--stage-dir` option is `.cmb-build/`.

# Description

`cmb-products.py` currently automates the creation and distribution of
the following products

* `entity_ids.<datetag>.rds` and `entity_ids.<datetag>.xlsx`
* `cmb-registration-data-for-iroc.<datetag>.txt`
* `slide_data_for_uams.<datetag>.xlsx`
* `slide_metadata_for_tcia.<datetag>.xlsx`

Excel files are written using [XlsxWriter](https://xlsxwriter.readthedocs.io/index.html).

Input data are Rave dump CSVs, VARI sample inventory XLSX, VARI slide
export XLSX.

Filesystem sources for input data and destinations for products are
configured in
[`cmb-products.yaml`](./cmb-products.yaml.sample). Currently, network
sources and destinations must be mounted locally as network volumes.

The hard work is done by executing
[`rave-reduce.r`](../rave-reduce). Note that both the script file and
the rave-reduce config file must be available to `cmb-products` and
specified in the `cmb-products.yaml` configuration.

The script logs events and inputs, including system command lines. The
log file defaults to `cmb-products.log`. Runs append log lines to this
file. The amount of log chatter to the screen can be adjusted with
`-v` and `-q`.


_Staging directory and distribution_: The products are created in the
staging directory (default `.cmb-build`, set by `--stage-dir`). A file
(`cmb-dist-file`) with source and target paths, one such pair per
line, is also created. Best to clear the staging directory before a
production run.

If `cmb-products.py` is run with the
`--distribute` option, a copy from source to target is performed.
Without that option, one can inspect the products before distribution.

Run with the option `--distribute-only` to copy files to destinations
as a second step, without re-creating the product files.

Use `--dry-run` to see what would happen via the log, but not create
or distribute any files.


