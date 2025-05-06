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
data_files <- rev(list.files(datadir, pattern=".*xlsx$", recursive=TRUE))

## actual column names in dbGaP data files:
fields_by_file <- tibble(data_files %>%
                         map_dfr(
                             function (f) {
                                 xx<-read_excel(paste(datadir,f,sep="/"),col_names=F);
                                 data.frame(file = rep(f,length(xx[1,])),
                                            field = as.vector(xx[1,],mode="character"))}));
fields_by_file  <- fields_by_file %>% mutate( basename = basename(file) )

## Read submitted CMB data

maps  <- read_excel(map_file,sheet=map_sheet) %>%
    filter(map2_lgl(`CMB Source Data File`,`Fixed Value?`, \(x, y) (!is.na(x) || !is.na(y)))) %>%
    filter(map2_lgl(`CMB Source Field`,`Fixed Value?`, \(x, y) (!is.na(x) || !is.na(y))) ) %>%
    filter(!is.na(`CTDC Destination Node`)) %>%
    filter(!is.na(`CTDC Destination Property`)) %>%
    mutate( `dbGaP code` = str_to_upper( str_sub(`CMB Source Data File`,1,2) ) )

# ensure first tbl in list is a base table - i.e., a table that has the
# full set of IDs to be filtered out in the ensuing left_joins
# The following orders the source table within the dest node them by
# putting the tbls that are marked "TRUE" in 'Base Table' first
# (ensures all base table rows are represented in the left_join result

tbls <- maps %>%
    filter(!is.na(`CMB Source Data File`)) %>%
    group_by(`CTDC Destination Node`,`CMB Source Data File`) %>%
    summarize(base = any(`Base Table`,na.rm=TRUE)) %>%
    arrange(!base, .by_group=TRUE)

not_processed  <- maps %>% anti_join(fields_by_file, by=c("CMB Source Data File" = "basename",
                                                          "CMB Source Field" = "field"))
maps  <- maps %>%
    semi_join(fields_by_file, by=c("CMB Source Data File" = "basename",
                                   "CMB Source Field" = "field")) %>%
    bind_rows(maps %>% filter(!is.na(`Fixed Value?`)))
    

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
        select(`CTDC Destination Property`, `CMB Source Data File`,
               `CMB Source Field`, `Fixed Value?`) %>%
        rename(pr = `CTDC Destination Property`,
               file = `CMB Source Data File`,
               field = `CMB Source Field`,
               fixedv = `Fixed Value?`)
    nd_tbls <- (tbls %>% filter( `CTDC Destination Node` == nd ))$`CMB Source Data File`
    dta  <- NULL
    join_cols <- NULL
    if (nd =='specimen') {
        join_cols  <- c('SAMPLE_ID')
    } else {
        join_cols  <- c('SUBJECT_ID')
    }
    for (t in nd_tbls) {
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
    xfmd_props  <- (props %>% filter(is.na(fixedv)))
    for (i in c(1:length(xfmd_props$pr))) {
        pr  <-  xfmd_props$pr[i]
        field  <- xfmd_props$field[i]
        # see vignette('programming'):
        dta <- dta %>% mutate( {{pr}} := .data[[field]] )
    }
    # must be single symbols in {{ }}, not expressions:
    from_col  <- xfmd_props$pr[1]
    to_col  <- xfmd_props$pr[length(xfmd_props$pr)]
    dta  <- dta %>% select( {{from_col}}:{{to_col}} ) %>% mutate(type = {{nd}})

    #add any fixed value fields
    
    for (p in (props %>% filter(!is.na(fixedv)))$pr) {
        fv = (props %>% filter(pr == p))$fixedv
        dta  <- dta %>% mutate( {{p}} := {{fv}} )
    }
    targets[[nd]]  <- dta
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
              paste(file.path(opt$outdir, nd),"tsv",sep="."),
              na="")
}
