#!/usr/bin/env -S Rscript --verbose --no-init-file --slave
suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(stringr))
suppressPackageStartupMessages(library(lubridate))
suppressPackageStartupMessages(library(readxl))
suppressPackageStartupMessages(library(optparse))
suppressPackageStartupMessages(library(config))
options(error = traceback)
## default common columns (denormalized across tables coming from Rave)
com_cols_default <- c("project", "subjectId", "Subject", "siteid", "Site","SiteNumber")

tday <- suppressMessages(stamp("28 Feb 1956"))(today())
lddta <- function(dtadir, nms=NULL) {
    files <<- list.files(dtadir) %>% grep(".*CSV", x=., value=T)
    if (!is.null(nms)) {
        files <- grep(nms, files, value=T)
    }
    tbls  <- (files %>% str_match("^[A-Z_]*(.*)[.].*$"))[,2]
    dta  <-  map(files, function (x) {
        y <- read_csv(file.path(dtadir,x))
        if (nrow(problems(y))) {
            print(dtadir,fo=stderr)
            print(x,fo=stderr)
            print(problems(y),fo=stderr,n=Inf,width=Inf)
        }
        tibble(y) })
    names(dta) <- tbls
    dta
}
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
        problems()
        ## Check for non rave "original id" and purge - caused issue at 03/28/2022 run
        bcr_report <- bcr_report %>% filter( grepl("^10323",`Original Id`) )
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
        bcr_slides <- bcr_slides %>% unique()
        # check for missing data in file name column
        missing  <- bcr_slides %>% dplyr::filter( is.na(`Image File Name`)  | is.null(`Image File Name`) )
        if (nrow(missing)) {
            warning(str_interp("BCR slide files in '${opts$options$bcr_slide_file_dir}' have missing data\n"),
                    immediate.=TRUE)
            missing
        }
        
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
    q(save="no",status=1)
}

stopifnot(!is.null(config$description)) # no such strategy
stopifnot(file.exists(file.path(opts$options$config_dir,config$strategies_file))) # no strategies.r available
source(file.path(opts$options$config_dir,config$strategies_file))

## this sets up some variables used in strategies.r
dta <- suppressMessages(lddta(dtadir))
## now dta is a list of all tables, named appropriately (e.g., dta$specimen_tracking_enrollment, etc.)

## this adds rave_spec_id to the subject_tracking_enrollment table:
dta$specimen_tracking_enrollment <- dta$specimen_tracking_enrollment %>%
    inner_join( dta$administrative_enrollment %>%
                select(Subject, USUBJID)) %>%
    mutate(rave_spec_id = str_c(project, USUBJID, RecordPosition, sep="-"))

## output which tables have no data (but are requested in config.yml) - to stderr
dum <- flatten(map( names(dta), function (x) if (!nrow(dta[[x]])) {dum <- if (x %in% names(config$xtbls)) cat(str_interp("Table ${x} has no data\n"),file=stderr())}))

if( !is.null(config$output) ) {
    for( nm in names(config$output) ) {
        fnm  <- nm
        sg <- config$output[[nm]]
        ## check for errors

        outp  <- try(strategies[[sg$strategy]](pull_date))
        if (!is.null(attr(outp,"condition"))) {
            cat(outp)
            q(save="no",status=1)
        }
        if (fnm == "stdout") {
            print.data.frame(outp, quote=TRUE,row.names=FALSE)
        } else {
            fnm_split  <- strsplit(fnm,"\\.")[[1]]
            if (file.exists(fnm)) {
                fnm  <- str_c( append(fnm_split, as.double(now()),length(fnm_split)-1),collapse=".")
            }
            if (last(fnm_split) == "rds") {
                saveRDS(outp, fnm)
            } else {
                write_delim(outp, fnm, delim=sg$delim)
            }
        }
    }
}


