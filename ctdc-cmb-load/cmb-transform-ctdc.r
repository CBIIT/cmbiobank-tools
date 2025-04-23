#!/usr/bin/env -S Rscript --verbose --no-init-file --slave

suppressPackageStartupMessages(library(optparse))
suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(readxl))
suppressPackageStartupMessages(library(config))
filter <- dplyr::filter

# if a config.yml file is available, use to obtain default values
# for the cli options
cfg  <- tryCatch(config::get(), error = \(x) NULL)
if (is.null(cfg)) {
    cfg$datadir  <- NULL
    cfg$mapfile  <- NULL
    cfg$outdir  <- NULL
}

# Define command-line options
option_list <- list(
  make_option(c("-d", "--datadir"), type = "character", default = cfg$datadir,
              help = "Directory containing dbGaP Excel files [default: %default]", metavar = "dir"),
  make_option(c("-m", "--mapfile"), type = "character", default = cfg$mapfile,
              help = "Mapping file path [default: %default]", metavar = "file"),
  make_option(c("-o", "--outdir"), type = "character", default = cfg$outdir,
              help = "Output directory for TSV files [default: %default]", metavar = "dir")
)

# Parse command-line options
opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)

# Assign parsed options to variables
datadir <- opt$datadir
map_file <- opt$mapfile

map_sheet  <- "Sheet1"
data_files <- rev(grep("^[^~].*xlsx", list.files(datadir), value=T))

## actual column names in dbGaP data files:
fields_by_file <- tibble(data_files %>%
                         map_dfr(
                             function (f) {
                                 xx<-read_excel(paste(datadir,f,sep="/"),col_names=F);
                                 data.frame(file = rep(f,length(xx[1,])),
                                            field = as.vector(xx[1,],mode="character"))}))

## Read submitted CMB data

maps  <- read_excel(map_file,sheet=map_sheet) %>%
    filter(!is.na(`CMB Source Data File`)) %>%
    filter(!is.na(`CMB Source Field`)) %>%
    filter(!is.na(`CTDC Destination Node`)) %>%
    filter(!is.na(`CTDC Destination Property`)) %>%
    mutate( `dbGaP code` = str_to_upper( str_sub(`CMB Source Data File`,1,2) ) )

bases  <- maps %>% group_by(`CMB Source Data File`) %>% summarize(base = any(`Base Table`,na.rm=TRUE))

not_processed  <- maps %>% anti_join(fields_by_file, by=c("CMB Source Data File" = "file",
                                                          "CMB Source Field" = "field"))
maps  <- maps %>% semi_join(fields_by_file, by=c("CMB Source Data File" = "file",
                                                          "CMB Source Field" = "field"))
if (length(not_processed) > 0) {
    warning("The above fields in the map file are not present in the data files.\nThey will not be processed.")
    not_processed %>% select(`CMB Source Data File`,`CMB Source Field`) %>% print(n=Inf)
    }

## Transform CMB vocabulary to CTDC model vocabulary

sources <- list()
targets  <- list()
for (m in maps$`CMB Source Data File` %>% unique) {
    fn  <- grep(m, data_files, value=T, fixed=T)
    if (length(fn) == 0) {
        next
        }
    fn  <- paste(datadir,fn[1],sep="/")
    print(fn)
    dbcode  <- as.character( maps %>% dplyr::filter( `CMB Source Data File` == m ) %>%
                             select(`dbGaP code`) %>% group_by(`dbGaP code`) %>% summarize)
    if (!is.na(file.info(fn)$isdir) && !file.info(fn)$isdir ) {
        sources[[m]] <- list(data=read_excel(fn), dbcode=dbcode)
    }
}

for (nd in maps$`CTDC Destination Node` %>% unique) {
    props <- maps %>% filter(`CTDC Destination Node`==nd) %>%
        select(`CTDC Destination Property`, `CMB Source Data File`, `CMB Source Field`) %>%
        rename(pr = `CTDC Destination Property`,
               file = `CMB Source Data File`,
               field = `CMB Source Field`)
    tbls <- (props %>% group_by(file) %>% summarize())[['file']]
    # ensure first tbl in list is a base table - i.e., a table that has the
    # full set of IDs to be filtered out in the ensuing left_joins
    # The following looks up the tbls in bases tbl - orders them by
    # putting the tbls that are marked "TRUE" in bases$base first in the
    # list
    tbls  <- tbls[rev(order(bases$base[match(tbls, bases$`CMB Source Data File`)]))]
    dta  <- NULL
    join_cols <- NULL
    if (nd =='specimen') {
        join_cols  <- c('SAMPLE_ID')
    } else {
        join_cols  <- c('SUBJECT_ID')
    }
    for (t in tbls) {
        flds  <- (props %>% filter(file == {{t}}) %>% select(field))[['field']]
        flds  <- c(join_cols, flds)
        if (is.null(dta)) {
            dta <- sources[[t]]$data %>% select(all_of(flds))
        } else {
            dta  <- dta %>% left_join(sources[[t]]$data %>% select(all_of(flds)),
                                      by=join_cols)
            }
    }
    dta  <- dta %>% unique
    # add CTDC columns and remove CMB columns
    for (i in c(1:length(props$pr))) {
        pr  <-  props$pr[i]
        field  <- props$field[i]
        # see vignette('programming'):
        dta <- dta %>% mutate( {{pr}} := .data[[field]] )
    }
    # must be single symbols in {{ }}, not expressions:
    from_col  <- props$pr[1]
    to_col  <- props$pr[length(props$pr)]
    targets[[nd]]  <- dta %>% select( {{from_col}}:{{to_col}} ) %>% mutate(type = {{nd}})
}

## other transformations

## fix "Bachelor's Degree" in demographic.highest_level_of_education

targets[['demographic']]$highest_level_of_education  <- targets[['demographic']]$highest_level_of_education %>% str_replace("Bachelor.*", "Bachelor's Degree")

## split SNOMED disease field into code and term
targets[['diagnosis']]  <-  targets[['diagnosis']] %>%
    select(!snomed_disease_term) %>%
    separate_wider_delim(snomed_disease_code,
                         delim = " = ",
                         names=c("snomed_disease_term", "snomed_disease_code"))

## remove records without therapy data

targets[['non_targeted_therapy']] <- targets[['non_targeted_therapy']] %>%
    filter( !is.na(non_targeted_therapy) )
targets[['targeted_therapy']] <- targets[['targeted_therapy']] %>%
    filter( !is.na(targeted_therapy) )
targets[['radiotherapy']] <- targets[['radiotherapy']] %>%
    filter( !is.na(radiological_procedure) )
targets[['surgery']] <- targets[['surgery']] %>%
    filter( !is.na(surgical_procedure) )


## Write loader-ready tab-separated value files

for (nd in names(targets)) {
    write_tsv(targets[[nd]],
              paste(file.path(opt$outdir, nd),"txt",sep="."),
              na="")
}
