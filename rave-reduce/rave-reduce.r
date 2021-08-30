#!/usr/bin/env -S Rscript --slave
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
        make_option(c("--config-dir"),action="store",default="/usr/local/rave-reduce",
                    help="configuration directory (location of config.yml, strategies.r; default: %default"),
        make_option(c("-c","--config"),action="store",default="config.yml",
                    help="config file name (default: %default)"),
        make_option(c("-s","--strategy"),action="store",default="default",
                    help="output strategy (default: %default)"),
        make_option(c("--ids-file"),action="store",default="entity_ids.rds",
                     help="ids file (rds format) (default: %default)"),
        make_option(c("--bcr-file"),action="store",default="NONE",
                    help="bcr report file (excel format) (default: NONE)"),
        make_option(c("--bcr-slide-file-dir"),action="store",default="NONE",
                    help="bcr slide report dir (excel format) (default: NONE)"),
        make_option(c("--bcr-date"),action="store",default=NULL,
                    help="date of bcr report file: 'dd MMM yyyy'"),
        make_option(c("-d","--pulldate"),action="store", default=tday,
                    help="pull date to apply to output: 'dd MMM yyyy'"),
        make_option(c("-o","--outfile"),action="store", default=NULL,
                    help="specify output filename for certain strategies"),
        make_option(c("-l","--list"),action="store_true",default=F,
                    help="list strategies with descriptions")
        ))

opts <- parse_args2(oparser)

## param checking - can do better than this
#stopifnot(!is.na(opts$args[1]) && dir.exists(opts$args[1]))
if (is.null(opts$options$config) ) {
    opts$options$config  <- "config.yml"
}

stopifnot(file.exists(file.path(opts$options$config_dir,opts$options$config))) # no config file available

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

if (is.null(opts$options$bcr_slide_file_dir) | (opts$options$bcr_slide_file_dir == "NONE")) {
    bcr_slides  <- NULL
} else {
    if (!file.exists(opts$options$bcr_slide_file_dir)) {
        warning(str_interp("BCR file '${opts$options$bcr_slide_file_dir}' is not found\n"),
            immediate.=TRUE)
        bcr_slides  <- NULL
    } else {
        ff  <- grep("xlsx",dir(opts$options$bcr_slide_file_dir),value=T)
        bcr_slides  <- NULL
        for (f in ff) bcr_slides  <- bcr_slides %>%
                          bind_rows(
                              read_excel(file.path(opts$options$bcr_slide_file_dir,f)))
    }
}

outfile  <-  opts$options$outfile

## list strategies - a help function
if (opts$options$list) {
    cfg  <- yaml::read_yaml(file.path(opts$options$config_dir,opts$options$config))
    cat("rave-reduce strategies (-s):\n")
    for (nm in setdiff(names(cfg),c("default"))) {
        cat(str_interp(" ${nm}:\n   ${cfg[[nm]]$description}"))
    }
    q(save="no")
}

dtadir  <- opts$args[1]
config  <- config::get(config=opts$options$strategy,file=file.path(opts$options$config_dir,opts$options$config))
terms  <- readRDS(file.path(opts$options$config_dir,config$terms_rds_file))
med_to_tcia  <- readRDS(file.path(opts$options$config_dir,config$meddra_tcia_file))
pull_date  <- opts$options$pulldate
bcr_pull_date  <- if (is.null(opts$options$bcr_date)) { pull_date } else { opts$options$bcr_date }

if (is.null(config$description)) {
    if (!(opts$options$strategy=="default")) {
        cat(str_interp("error: no such strategy '${opts$options$strategy}'; use -l to list strategies\n"))
    }
    else {
        cat(str_interp("no strategy selected; use -s, or -l to list strategies\n"));
    }
    q(save="no")
}

stopifnot(!is.null(config$description)) # no such strategy
stopifnot(file.exists(file.path(opts$options$config_dir,config$strategies_file))) # no strategies.r available
source(file.path(opts$options$config_dir,config$strategies_file))

## this sets up some variables used in strategies.r
files <- grep("CSV",dir(dtadir),value=T) # assumes dump in CSV
if (length(files)>0) {
    tbls  <- files %>% str_sub(5,-5)
    dta  <- suppressMessages( map(files, function (x) tibble(read_csv(file.path(dtadir,x)))) )
    names(dta)  <- tbls
    ## now dta is a list of all tables, named appropriately (e.g., dta$specimen_tracking_enrollment, etc.)

    ## this adds rave_spec_id to the subject_tracking_enrollment table:
    dta$specimen_tracking_enrollment %>%
        inner_join( dta$administrative_enrollment %>%
                    select(Subject, USUBJID)) %>%
        mutate(rave_spec_id = str_c(project, USUBJID, RecordPosition, sep="-"))

    ## output which tables have no data (but are requested in config.yml) - to stderr
    dum <- flatten(map( names(dta), function (x) if (!nrow(dta[[x]])) {dum <- if (x %in% names(config$xtbls)) cat(str_interp("Table ${x} has no data\n"),file=stderr())}))
}

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

