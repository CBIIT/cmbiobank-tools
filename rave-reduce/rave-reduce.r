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
        make_option(c("-d","--pulldate"),action="store", default=tday,
                    help="pull date to apply to output")
        ))

opts <- parse_args2(oparser)

## param checking - can do better than this    
stopifnot(!is.null(opts$args[1]) && dir.exists(opts$args[1]))
if (is.null(opts$options$config) ) {
    opts$options$config  <- "config.yml"
}
stopifnot(file.exists(opts$options$config))

if (is.null(opts$options$terms_rds_file )) {
    opts$options$terms_rds_file  <- "form-terms.rds"
}
stopifnot(file.exists(opts$options$terms_rds_file))

if (is.null(opts$options$ids_file)) {
    opts$options$ids_file  <- "Random IDs.xlsx"
}
stopifnot(file.exists(opts$options$ids_file))


dtadir  <- opts$args[1]
config  <- config::get(config=opts$options$strategy,file=opts$options$config)
terms  <- readRDS(opts$options$terms_rds_file)
pull_date  <- opts$options$pulldate

## munge IDs
## this code extremely brittle - depends on the ad hoc format of the IDs excel
## rather have an input IDs file that is in the final format (entity_ids) below.
pub_ids  <- read_excel(opts$options$ids_file,1)
pub_spec_ids  <- read_excel(opts$options$ids_file,2)
pub_subspec_ids  <- read_excel(opts$options$ids_file,3)
## regularize the column names
names(pub_ids)  <- c("rnd","rnd_id","pub_id","ctep_id", "up_id","pub_id2","rave_id","ec_id")
names(pub_spec_ids)  <- c("log_line","ctep_id","up_id","pub_id","rave_spec_id", "pub_spec_id")
names(pub_subspec_ids)  <- c("ctep_id","pub_id","pub_spec_id","bcr_subspec_id","pub_subspec_id","log_line")
## inner join pub_ids and pub_spec_ids on pub_id to get a useful table (sans unmapped ids)
## left join that with pub_subspec_ids to acquire subspecimens where available
entity_ids <- pub_ids %>% inner_join(pub_spec_ids,by = c("pub_id","ctep_id","up_id")) %>% select( pub_id,ctep_id,up_id,rave_spec_id, pub_spec_id,log_line) %>% left_join(pub_subspec_ids,by=c("pub_id","ctep_id","pub_spec_id"))
files <- grep("CSV",dir(dtadir),value=T) # line assumes csv, other formats poss.
tbls  <- files %>% str_sub(5,-5)
dta  <- suppressMessages( map(files, function (x) tibble(read_csv(file.path(dtadir,x)))) )

names(dta)  <- tbls
## now dta is a list of all tables, named appropriately (e.g., dta$specimen_tracking_enrollment, etc.)

## output which tables have no data (but are requested in config.yml) - to stderr
dum <- flatten(map( names(dta), function (x) if (!nrow(dta[[x]])) {dum <- if (x %in% names(config$xtbls)) cat(str_interp("Table ${x} has no data\n"),file=stderr())}))

if( !is.null(config$output) ) {
    for( nm in names(config$output) ) {
        fnm  <- nm
        if (fnm == "stdout") {
            print.data.frame(eval(str2lang(config$output[[nm]]$func))(pull_date), quote=TRUE,row.names=FALSE)
        }
        else {
            if (file.exists(fnm)) fnm  <- paste(nm, as.double(now()),sep=".");
            write_delim(eval(str2lang(config$output[[nm]]$func))(pull_date),fnm,
                        delim=config$output[[nm]]$delim)
        }
    }
}

