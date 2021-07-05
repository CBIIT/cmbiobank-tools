#!/usr/bin/env Rscript --slave
suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(lubridate))
suppressPackageStartupMessages(library(readxl))
suppressPackageStartupMessages(library(optparse))
suppressPackageStartupMessages(library(config))

## default common columns (denormalized across tables coming from Rave)
com_cols_default <- c("project", "subjectId", "Subject", "siteid", "Site","SiteNumber")

## default tables desired
xtbls_default <- c("specimen_tracking_enrollment","enrollment","blood_collection_adverse_even","blood_collection_adverse_eve2","biopsy_adverse_event_presence","biopsy_adverse_events","histology_and_disease","specimen_transmittal","biopsy_pathology_verification","oncomine_result","shipping_status","prior__treatment_summary","intervening_therapy","targeted_therapy_administrati")

## default columns desired

## features
## if a public id transform table is provided, output public pt,spec,subspec IDs
##   and suppress the internal ids
## configure by providing (via a config.yml file):
##  - a list (single column text file) of column ids desired in output
##  - a list of tables desired in output
##  - an RDS version of 10323 term table 
##  - defaults based on Laura's requirements
## report tables with zero rows -
##  - particularly the adverse events tables
## auto-determine the subject-oriented and specimen-oriented tables (using columns)?
## attempt to automate (or specify in config) joins

tday <- suppressMessages(stamp("28 Feb 1956"))(today())
oparser <- OptionParser(
    usage = "%prog dumpdir",
    option_list = list(
        make_option(c("-c","--config"),action="store",default="config.yml",
                    help="config file (default: %default)"),
        make_option(c("-s","--strategy"),action="store",default="default",
                    help="output strategy (default: %default)"),
        make_option(c("--ids-file"),action="store",default="entity_ids.rds",
                     help="ids file (rds format) (default: %default)"),
        make_option(c("--bcr-file"),action="store",default="NONE",
                     help="bcr report file (excel format) (default: NONE)"),
        make_option(c("-d","--pulldate"),action="store", default=tday,
                    help="pull date to apply to output"),
        make_option(c("-l","--list"),action="store_true",default=F,
                    help="list strategies with descriptions")
        ))

opts <- parse_args2(oparser)

## list strategies - a help function
if (opts$options$list) {
    cfg  <- yaml::read_yaml(opts$options$config)
    cat("rave-reduce strategies (-s):\n")
    for (nm in setdiff(names(cfg),c("default"))) {
        cat(str_interp(" ${nm}:\n   ${cfg[[nm]]$description}"))
    }
    q(save="no")
}

## param checking - can do better than this
#stopifnot(!is.na(opts$args[1]) && dir.exists(opts$args[1]))
if (is.null(opts$options$config) ) {
    opts$options$config  <- "config.yml"
}
stopifnot(file.exists(opts$options$config)) # no config file available

if (is.null(opts$options$ids_file)) {
    opts$options$ids_file  <- "entity_ids.rds"
}

if (!file.exists(opts$options$ids_file)) {
    warning(str_interp("IDs file '${opts$options$ids_file}' is not present\n"),
            immediate.=TRUE)
} else {
    entity_ids  <- readRDS(opts$options$ids_file)
}

if (is.null(opts$options$bcr_file) | (opts$options$bcr_file == "NONE")) {
    bcr_report  <- NULL
} else {
    if (!file.exists(opts$options$bcr_file)) {
        warning(str_interp("BCR file '${opts$options$bcr_file}' is not found\n"),
            immediate.=TRUE)
        bcr_report  <- NULL
    } else {
        bcr_report  <- read_excel(opts$options$bcr_file)
    }
}

dtadir  <- opts$args[1]
config  <- config::get(config=opts$options$strategy,file=opts$options$config)
terms  <- readRDS(config$terms_rds_file)
pull_date  <- opts$options$pulldate

stopifnot(!is.null(config$description)) # no such strategy
stopifnot(file.exists(config$strategies_file)) # no strategies.r available
source(config$strategies_file)

files <- grep("CSV",dir(dtadir),value=T) # assumes dump in CSV
stopifnot( length(files) > 0 ) # stop if dtadir has no CSV files
tbls  <- files %>% str_sub(5,-5)
dta  <- suppressMessages( map(files, function (x) tibble(read_csv(file.path(dtadir,x)))) )

names(dta)  <- tbls
## now dta is a list of all tables, named appropriately (e.g., dta$specimen_tracking_enrollment, etc.)

## output which tables have no data (but are requested in config.yml) - to stderr
dum <- flatten(map( names(dta), function (x) if (!nrow(dta[[x]])) {dum <- if (x %in% names(config$xtbls)) cat(str_interp("Table ${x} has no data\n"),file=stderr())}))

if( !is.null(config$output) ) {
    for( nm in names(config$output) ) {
        fnm  <- nm
        sg <- config$output[[nm]]
        if (fnm == "stdout") {
            print.data.frame(strategies[[sg$strategy]](pull_date), quote=TRUE,row.names=FALSE)
        } else {
            fnm_split  <- strsplit(fnm,"\\.")[[1]]
            if (file.exists(fnm)) {
                fnm  <- str_c( append(fnm_split, as.double(now()),length(fnm_split)-1),collapse=".")
            }
            if (last(fnm_split) == "rds") {
                saveRDS(strategies[[sg$strategy]](pull_date), fnm)
            } else {
                write_delim(strategies[[sg$strategy]](pull_date),fnm,
                            delim=sg$delim)
            }
        }
    }
}

