need_files  <- function(){
    if (length(files)==0) {
        cat(str_interp("this strategy requires a path containing CSV files (for arg1)\n"))
        q(save="no",status=1)
    }
}

need_bcr_report <- function(){
    if (is.null(bcr_report)) {
        cat(str_interp("this strategy requires a valid --bcr-file option\n"))
        q(save="no",status=1)
    }
}

need_bcr_slides <- function(){
    if (is.null(bcr_slides)) {
        cat(str_interp("this strategy requires a valid --bcr-slide-file-dir option\n"))
        q(save="no",status=1)
    }
}

dedup_by_fewest_nas  <- function (x, col_want_unique, cols_of_x, tiebreaker) {
    ## remove extra records associated with subspecimens - choose the rec with
    ## the fewest NA entries
    ## if there are more than one such rec, choose the one with the maximum
    ## value of the tiebreaker column (RecordPosition)
    ret <- NULL
    unc  <- enexpr(col_want_unique)
    nac  <- enexpr(cols_of_x)
    tbk  <- enexpr(tiebreaker)
    x_dup  <- x %>% group_by() %>% mutate(ct = n()) %>%
        dplyr::filter(ct > 1)
    if (nrow(x_dup)) {
        x_sing  <- x %>% group_by(!!unc) %>% mutate(ct = n()) %>%
            dplyr::filter(ct == 1) %>% ungroup %>% select( -ct )
        ## now, count the number of NAs among a set of vars that have caused issues
        ## and remove the rows (within each subspec group) that have the most NAs
        x_dedup <- x_dup %>% rowwise() %>%
            mutate( nas = sum(is.na(!!nac)) ) %>%
            ungroup() %>% group_by(!!unc) %>%
            dplyr::filter( nas == min(nas)) %>% 
            dplyr::filter( !!tbk == max(!!tbk) ) %>% ungroup %>%
            select( -ct, -nas) 
        ret  <- bind_rows(x_sing, x_dedup)
    }
    ret %>% unique
}


strategies <- list(
    check_ids = function (pull_date) {
        need_files()
        stopifnot(!is.null(dta$specimen_transmittal))
        dta$specimen_transmittal %>%
        select(Subject,SPECID,BSREFID) %>% unique %>%
        anti_join(entity_ids, by = c("Subject"="ctep_id","SPECID"="rave_spec_id", "BSREFID"="bcr_subspec_id")) %>%
        select(Subject,SPECID,BSREFID) %>%
        mutate("Pull date" = pull_date) 
    },
    entity_ids = function (pull_date) {
        dum  <- entity_ids %>% arrange( pub_subspec_id ) %>% filter( !is.na(ctep_id) )
        if (is.null(outfile)) {
            dum
        } else {
            write_excel_csv(dum, outfile)
        }
    },
    iroc = function (pulldate) {
        need_files()
        ## argument 'pulldate' is ignored in this function
        ## pull_date from the entity_ids file is used
                                        # cras  <- read_excel(config$cra_excel,1)
        pub_ids  <- entity_ids %>%
            filter(!is.na(ctep_id)) %>%
            group_by(ctep_id) %>%
            select(pub_id,up_id,pull_date) %>%
            mutate( date = dmy(pull_date) ) %>%
            arrange(ctep_id, date) %>%
            summarize( pub_id = first(pub_id), up_id = first(up_id), pull_date=first(pull_date), date = first(date) )
        withdrawn <- dta$off_study %>%
            select( Subject, DSDECOD_OS ) %>%
            transmute(Subject,
                      state = str_to_upper(str_extract(DSDECOD_OS, "^[^ ,]+"))) %>%
            inner_join(
                entity_ids %>% filter(!is.na(ctep_id)) %>%
                select(ctep_id, pub_id),
                by=c( "Subject" = "ctep_id"))
        tbl <- dta$enrollment %>% left_join(pub_ids, by=c("Subject" = "ctep_id")) %>%
            select(project, Subject, Site,CTEPID, DSSTDAT_ENROLLMENT_RAW,CTEP_SDC_MED_V10_CD, pub_id,up_id,pull_date) %>%
            left_join( dta$shipping_status %>%
              select(Subject, EMAIL_SHP) %>%
                                        # inner_join(cras,by=c("EMAIL_SHP" = "Email")) %>%
              group_by(Subject) %>%
              filter( !grepl("@vai",EMAIL_SHP) ) %>%
              summarize( CRA = first(EMAIL_SHP)),
              by = c("Subject"))
        if (!is.null(withdrawn)) {
            tbl <- tbl %>% mutate( CRA = if_else(
                                       pub_id %in% withdrawn$pub_id,
                                       map_chr(pub_id,
                                               function(x) (withdrawn %>% filter( pub_id == x ))$state[1]
                                               ),
                                       CRA ) )
        }
        tbl %>%
            transmute("Date Created" = pull_date, #str_interp("${pull_date}"),
                  "Study" = project,
                  "Registration Step" = 1,
                  "Registration Step Description" = str_interp("Enrollment"),
                  "Site Name" = Site,
                  "Site CTEP ID" = CTEPID, "CTEP Patient ID" = Subject, "Registering Site Contact" = CRA,
                  "Current Site Contact" = CRA, "Universal Patient ID" = up_id,
                  "Registration Date" = DSSTDAT_ENROLLMENT_RAW, "Public Patient ID" = pub_id,
                  "Cancer Type" = CTEP_SDC_MED_V10_CD)
    },
    entity_ids_from_xls = function (pull_date) {
        ## munge IDs
        ## this code extremely brittle - depends on the ad hoc format of the IDs excel
        ## rather have an input IDs file that is in the final format (entity_ids) below.
        pub_ids  <- read_excel(config$ids_excel,1)
        pub_spec_ids  <- read_excel(config$ids_excel,2)
        pub_subspec_ids  <- read_excel(config$ids_excel,3)
        ## regularize the column names
        names(pub_ids)  <- c("rnd","rnd_id","pub_id","ctep_id", "up_id","pub_id2","rave_id","ec_id")
        names(pub_spec_ids)  <- c("log_line","ctep_id","up_id","pub_id","rave_spec_id", "pub_spec_id")
        names(pub_subspec_ids)  <- c("ctep_id","pub_id","pub_spec_id","bcr_subspec_id","pub_subspec_id","log_line")
        ## inner join pub_ids and pub_spec_ids on pub_id to get a useful table (sans unmapped ids)
        ## left join that with pub_subspec_ids to acquire subspecimens where available
        entity_ids <- pub_ids %>%
            left_join(pub_spec_ids,by = c("pub_id","ctep_id","up_id")) %>%
            select( pub_id,ctep_id,up_id,rave_spec_id, pub_spec_id) %>%
            left_join(pub_subspec_ids,by=c("pub_id","ctep_id","pub_spec_id")) %>%
            mutate( pull_date = map_chr(ctep_id, function(x)if(is.na(x)) {NA} else {pull_date})) %>% select( -log_line)
    },
    update_ids = function (pull_date) {
        need_files()
        ## patients can be enrolled but without specimen transmittal - 
        ## need to look at enrollment table too
        ## orphans - no pub_id or pub_spec_id yet

        ## bootstrap an 'active' column
        if (!("active" %in% names(entity_ids))) {
            entity_ids  <- entity_ids %>% mutate( active = !is.na(ctep_id) )
        }
        no_specimens  <- dta$enrollment %>% inner_join(dta$administrative_enrollment,by=c("Subject")) %>% select(Subject,USUBJID) %>% anti_join(dta$specimen_transmittal) %>% rename(USUBJID_DRV = USUBJID)
        ## pull orphans from specimen_transmittal form
        orphans <- dta$specimen_transmittal %>%
            select(Subject,SPECID,BSREFID,USUBJID_DRV) %>% unique %>%
            anti_join(entity_ids %>% filter( active ),
                      by = c("Subject"="ctep_id",
                             "SPECID"="rave_spec_id",
                             "BSREFID"="bcr_subspec_id",
                             "USUBJID_DRV"="up_id"))

        ## pull more orphans from receiving_status form
        orphans <- orphans %>%
            full_join(
                dta$receiving_status %>%
                select(Subject,SPECID2_DRV,SUBSPCM) %>%
                filter( !is.na(SUBSPCM) ) %>%
                inner_join(dta$administrative_enrollment, by=c("Subject")) %>%
                select(Subject,SPECID2_DRV,SUBSPCM,USUBJID) %>% unique %>%
                anti_join(entity_ids %>% filter( active ),
                          by = c("Subject" = "ctep_id",
                                 "SPECID2_DRV"="rave_spec_id",
                                 "SUBSPCM"="bcr_subspec_id",
                                 "USUBJID"="up_id")),
                by = c("Subject" = "Subject",
                       "SPECID" = "SPECID2_DRV",
                       "BSREFID" = "SUBSPCM",
                       "USUBJID_DRV" = "USUBJID"))

        ## add those new participants without specimens yet
        orphans <- orphans %>% full_join(no_specimens)
        ## newbies - new patients without pub_id
        newbies  <- orphans %>%
            anti_join(entity_ids %>% filter( active ),
                      by=c("Subject"="ctep_id",
                           "USUBJID_DRV"="up_id"))
        ## unused - public ids that are not yet assigned
        unused  <- entity_ids %>% filter( is.na(ctep_id) ) %>% select(pub_id)
        ## assign unused pub_ids to newbies
        ## note, need to group by Subject only (not by Subject,USUBJID_DRV)
        ## - then row numbers are sequential (rather than all "1",the first
        ##   row in each group, each of which has only one record)
        assgn  <-  newbies %>%
            group_by(Subject) %>%
            summarize(USUBJID_DRV=first(USUBJID_DRV)) %>%
            mutate(num =row_number()) %>%
            inner_join(unused %>% mutate(num = row_number()), by=c("num")) %>% select(-num)
        ## remove the newly assigned pubids from entity_ids
        entity_ids  <- entity_ids %>% anti_join(assgn, by=c("pub_id"))
        ## set the newbies' pub_ids in orphans (adding pub_id column to orphans)
        orphans_a <- bind_rows(
            orphans %>%
            inner_join(entity_ids %>% filter( active ) %>%
                       select(ctep_id,up_id,pub_id) %>%
                       group_by(ctep_id,up_id) %>%
                       summarize(pub_id = first(pub_id)),
                       by = c("Subject" = "ctep_id",
                              "USUBJID_DRV" = "up_id") ),
            orphans %>% inner_join(assgn,by = c("Subject","USUBJID_DRV")))
        ## now handle specimen assignment
        assgn_b <- orphans_a %>%
            anti_join( entity_ids %>% filter( active ),
                      by=c("pub_id",
                           "Subject"="ctep_id",
                           "USUBJID_DRV"="up_id",
                           "SPECID" = "rave_spec_id") ) %>%
            mutate(pub_spec_id = str_c(pub_id,str_pad(str_extract(SPECID,"[0-9]+$"),2,"left","0" ),sep="-"))
        orphans_b  <- rbind(
            orphans_a %>%
            inner_join( entity_ids %>% filter( active ) %>%
                        select(ctep_id,up_id,pub_id,rave_spec_id, pub_spec_id) %>%
                        group_by(pub_spec_id) %>%
                        summarize(ctep_id=first(ctep_id),
                                  up_id=first(up_id),
                                  pub_id=first(pub_id),
                                  rave_spec_id=first(rave_spec_id)),
                       by = c("pub_id",
                              "Subject" = "ctep_id",
                              "USUBJID_DRV"="up_id",
                              "SPECID" = "rave_spec_id")),
            orphans_a %>%
            inner_join(assgn_b))
        ## now handle subspecimen assignment
        nxt  <- entity_ids %>% filter( active ) %>%
            select(pub_spec_id,pub_subspec_id) %>%
            group_by(pub_spec_id) %>%
            mutate( ssid =  as.integer(str_extract(pub_subspec_id,"[0-9]+$"))+1) %>%
            arrange(desc(ssid)) %>%
            summarize(pub_subspec_id = first(pub_subspec_id),ssid = first(ssid)) %>%
            mutate_at(vars(ssid),list(function(x)if_else(is.na(x),1,x)))
        next_ssid  <- NULL
        next_ssid[nxt$pub_spec_id] <- nxt$ssid
        next_ssid_for  <- function(ps_id) {
            if (is.na(next_ssid[ps_id])) {
                next_ssid[ps_id]  <- 1
            }
            n  <- next_ssid[ps_id]
            next_ssid[ps_id]  <<- next_ssid[ps_id]+1
            str_c(ps_id,str_pad(n,2,"left",0),sep="-") }
        orphans_b  <- orphans_b %>% arrange(pub_spec_id,BSREFID)
        ## do not provide a public subspec id to any rec without a BSREFID:
        ss_col  <- map2_chr(
            orphans_b$pub_spec_id,
            orphans_b$BSREFID,
            function (x,y) if (is.na(y)) { NA } else { next_ssid_for(x) })
        orphans_ss  <- orphans_b %>% 
            add_column( pub_subspec_id = ss_col ) %>%
            mutate( pull_date = pull_date, active = TRUE )
        entity_ids_upd  <<- orphans_ss %>% 
            full_join(entity_ids, by=c("Subject"="ctep_id",
                                       "USUBJID_DRV"="up_id",
                                       "SPECID"="rave_spec_id",
                                       "BSREFID"="bcr_subspec_id",
                                       "pub_id","pub_spec_id")) %>%
            mutate( pub_subspec_id = coalesce(pub_subspec_id.x,pub_subspec_id.y)) %>%
            mutate( pull_date = if_else(!is.na(pull_date.y),pull_date.y,pull_date.x)) %>%
            mutate( active = coalesce(active.x, active.y) ) %>%
            select( -pub_subspec_id.x,-pub_subspec_id.y, -pull_date.x,-pull_date.y,
                   -active.x, -active.y) %>%
            rename( ctep_id = Subject, up_id = USUBJID_DRV, rave_spec_id = SPECID, bcr_subspec_id = BSREFID)
        if (!is.null(bcr_report)) {
            cat("updating bcr-only subspecimens\n",file=stderr())
            strategies$update_bcr_ids(bcr_pull_date)
        } else {
            cat("bcr report not provided\n")
        }
        # throw if there are duplicate subspec ids
        if ( length((entity_ids_upd %>% filter(active) %>% filter(!is.na(pub_subspec_id)))$pub_subspec_id) !=
             length((entity_ids_upd %>% filter(active)  %>% filter(!is.na(pub_subspec_id)))$pub_subspec_id %>% unique) ) {
            cat("error: public subspecimen ids are not unique\n")
            q(save="no",status=1)
        }
        entity_ids_upd
    },
    entity_ids_upd = function (pull_date) entity_ids_upd,
    update_bcr_ids = function (pulldate) {
        ## check for changes
        changed_specs  <- bcr_report %>%
            rename( c("rave_spec_id"="Original Id","bcr_subspec_id" = "BSI ID") ) %>%
            inner_join(entity_ids %>% filter( active ),
                       by = c("bcr_subspec_id")) %>%
            select( bcr_subspec_id, rave_spec_id.x, rave_spec_id.y) %>%
            rename( rave_spec_id.old = rave_spec_id.x,
                      rave_spec_id.new = rave_spec_id.y) %>%
            filter( rave_spec_id.old != rave_spec_id.new )
        if (nrow(changed_specs)) {
            cat("Changed bcr subspecimen assignments:\n")
            print(changed_specs %>% print(n=Inf))
            ## following creates a new active column, setting
            ## active to False for any records that have
            ## match an old subspec id in the "changed_specs"
            ## tibble:
            active_upd  <- entity_ids %>%
                left_join(
                    changed_specs,
                    by = c( "bcr_subspec_id" = "bcr_subspec_id",
                           "rave_spec_id" = "rave_spec_id.old")) %>%
                select(rave_spec_id.new, active) %>%
                transmute( active = is.na(rave_spec_id.new)&active )
            entity_ids <- entity_ids %>% select(-active) %>% bind_cols(active_upd)
        }

        orphans_bcr  <- bcr_report %>%
            anti_join(entity_ids %>% filter( active ), by = c("BSI ID" = "bcr_subspec_id")) %>%
            rename( c("rave_spec_id"="Original Id","bcr_subspec_id" = "BSI ID") ) %>%
            transmute( rave_spec_id = str_to_upper(rave_spec_id), bcr_subspec_id) %>% 
            inner_join( entity_ids %>% select(ctep_id, up_id, rave_spec_id,pub_id, pub_spec_id) %>% unique ) %>%
            arrange(pub_spec_id, bcr_subspec_id) 

        nxt  <- entity_ids %>% filter( active ) %>%
            select(pub_spec_id,pub_subspec_id) %>%
            group_by(pub_spec_id) %>% 
            mutate( ssid =  as.integer(str_extract(pub_subspec_id,"[0-9]+$"))+1) %>%
            arrange(desc(ssid)) %>%
            summarize(pub_subspec_id = first(pub_subspec_id),ssid = first(ssid)) %>%
            mutate_at(vars(ssid),list(function(x)if_else(is.na(x),1,x)))
        next_ssid  <- NULL
        next_ssid[nxt$pub_spec_id] <- nxt$ssid
        next_ssid_for  <- function(ps_id) {
            if (is.na(next_ssid[ps_id])) {
                next_ssid[ps_id]  <- 1
            }
            n  <- next_ssid[ps_id]
            next_ssid[ps_id]  <<- next_ssid[ps_id]+1
            str_c(ps_id,str_pad(n,2,"left",0),sep="-") }
        ss_col  <- map2_chr(
            orphans_bcr$pub_spec_id,
            orphans_bcr$bcr_subspec_id,
            function (x,y) if (is.na(y)) { NA } else { next_ssid_for(x) })
        orphans_bcr  <-  orphans_bcr %>%
            add_column(pub_subspec_id = ss_col) %>%
            mutate(pull_date = pulldate, active = TRUE)
        entity_ids_upd  <<- bind_rows(entity_ids,orphans_bcr) %>% arrange(pub_subspec_id)
    },
    slide_table = function (pull_date) {
        need_files()
        need_bcr_report()
        need_bcr_slides()
       slide_mapping  <- entity_ids %>% dplyr::filter( !is.na(pub_subspec_id) ) %>%
           inner_join(bcr_report, by = c("bcr_subspec_id" = "BSI ID")) %>%
           inner_join(
               dta$enrollment %>% select( Subject, CTEP_SDC_MED_V10_CD ) %>%
               group_by(Subject, CTEP_SDC_MED_V10_CD),
               by=c("ctep_id" = "Subject")
           ) %>%
           rename(c( "anatomic_site" = "Anatomic Site",
                    "material_type" = "Material Type",
                    "clinical_diagnosis" = "CTEP_SDC_MED_V10_CD")) %>%
           select(ctep_id, pub_id, pub_spec_id,
                  rave_spec_id, pub_subspec_id, bcr_subspec_id,
                  material_type, anatomic_site, clinical_diagnosis,
                  pull_date) %>%
           dplyr::filter( grepl("Slide",material_type) ) %>%
           select(-material_type)
        slide_mapping  <- slide_mapping %>%
           left_join(dta$specimen_transmittal %>% select(SPECID,TISTYP),
                      by = c( "rave_spec_id" = "SPECID" )) %>%
           left_join(bcr_slides %>% select("Barcode ID","Image File Name"),
                      by = c( "bcr_subspec_id" = "Barcode ID")) %>%
           left_join(med_to_tcia,
                     by = c("clinical_diagnosis" = "MedDRA Term"))  %>%
           rename( c( "tissue_type" = "TISTYP",
                     "filename" = "Image File Name",
                     "tcia_collection" = "TCIA Collection") ) %>%
            unique()
       
        ## final table should meet reqs as of BF-S mtg 8/3/21 and excel "...with column headers needed"
        ## slide_mapping
        slide_mapping
    },
    tcia_metadata = function(pull_date) {
        need_files()
        need_bcr_report()
        need_bcr_slides()
        ## what we're doing here:
        ## we have the information for the slide subspecimens in 'slides'
        ## now we just want to add *specimen* metadata across the subspecimens in slides
        ##  (spec_info, below)
        ## and the participant metadata across the specimens (pt_info, below)
        ## to produce the table needed by tcia
        
        tc_rngs <- c("NO VIABLE TUMOR PRESENT"="0 - 9%",
                     "10% AND 19%" = "10% - 19%",
                     "20% AND 49%" = "20% - 49%",
                     "50% AND 69%" = "50% - 69%",
                     "70%" = ">=70%"
                     )
        getrng <- function (z) map_chr(z, function (y) if (!is.na(y)) tc_rngs[map_lgl( names(tc_rngs), function (x) grepl(x,y))] else NA)
        pt_info <- dta$enrollment %>%
            select( Subject, matches("RACE_.*_STD"),ETHNIC_STD,
                   CTEP_SDC_MED_V10_CD, MHLOC_STD, AGE,
                   SEX_STD, GENDER_STD, DSSTDAT_ENROLLMENT ) %>%
            mutate( RACE = str_squish(
                        str_c(str_replace_na(RACE_01_STD,""),
                              str_replace_na(RACE_02_STD,""),
                              str_replace_na(RACE_03_STD,""),
                              str_replace_na(RACE_04_STD,""),
                              str_replace_na(RACE_05_STD,""),
                              str_replace_na(RACE_06_STD,""),
                              str_replace_na(RACE_07_STD,""),sep=" ") )) %>%
            mutate( DATE_OF_ENROLLMENT = dmy_hms(DSSTDAT_ENROLLMENT) ) %>%
            select( -matches("RACE_.*") ) %>%
            select( -DSSTDAT_ENROLLMENT ) %>%
            unique

        spec_info <- dta$biopsy_pathology_verification_and_assessment %>%
            dplyr::filter(RecordActive == 1) %>%
            select(MIREFID,
                   SPLADQFL_X1_STD,



                   MIORRES_TUCONT_X1_STD,MIORRES_TUCONT_X2_STD,
                   MHTERM_DIAGNOSIS,
                   RecordPosition) %>% unique %>%
            inner_join(dta$specimen_tracking_enrollment %>%
                       select(SPECID_DRV,ASMTTPT_STD),
                       by = c("MIREFID" = "SPECID_DRV")) %>%
            unique
        
        slides <-  bcr_report %>%
            rename( "material_type" = "Material Type") %>%
            dplyr::filter(grepl("Slide",material_type)) %>%
            select("Subject ID","BSI ID",
                   vari_necrosis = "QC % Necrosis (Moonshot)",
                   vari_cellularity = "QC Tumor Cellularity (Moonshot)",
                   date_of_collection = "Collection Date/Time") %>%
            inner_join(entity_ids %>% dplyr::filter(active),
                       by = c("BSI ID"="bcr_subspec_id","Subject ID"="ctep_id")) %>%
                                        #separate(`BSI ID`, into=c("bsi_pfx","bsi_suf"), remove=F) %>%
                                        #select(-bsi_suf)



            unique
        
        datascope <- slides %>%
            inner_join(pt_info, by=c("Subject ID"="Subject")) %>%
            left_join(spec_info, by = c("rave_spec_id" = "MIREFID")) %>%
            unique %>%
            mutate(
                Percent_Tumor_Nuc = getrng(MIORRES_TUCONT_X1_STD),
                Percent_Tumor_Nuc_Enriched = getrng(MIORRES_TUCONT_X2_STD),
                ) %>%
            mutate(
                Percent_Tumor_Nuclei = dplyr::coalesce(Percent_Tumor_Nuc_Enriched, Percent_Tumor_Nuc),
                Is_Enriched = map2_chr(is.na(Percent_Tumor_Nuc),is.na(Percent_Tumor_Nuc_Enriched),function(x,y) if (x) { NA } else if (y) {"N"} else {"Y"})
            ) %>%
            mutate(
                Days_From_Enrollment = round((date_of_collection - DATE_OF_ENROLLMENT)/86400)
            ) %>%
            select( pub_id, pub_subspec_id, bcr_subspec_id = `BSI ID`,
                   Timepoint = ASMTTPT_STD,
                   Topographic_Site = CTEP_SDC_MED_V10_CD,
                   Tumor_Histologic_Type = MHTERM_DIAGNOSIS,
                   Tumor_Segment_Acceptable = SPLADQFL_X1_STD,
                   Percent_Necrosis = vari_necrosis,
                   Percent_Tumor_Nuclei,
                   Is_Enriched,
                   Days_From_Enrollment,
                   Gender = SEX_STD, Age = AGE, Ethnicity = ETHNIC_STD,
                   Race = RACE,
                   RecordPosition) %>%
            mutate(
                Tumor_Histologic_Type = str_to_title(Tumor_Histologic_Type)
            ) %>%
            left_join(med_to_tcia,
                      by = c("Topographic_Site" = "MedDRA Term")) %>%
            rename( "TCIA_Collection" = "TCIA Collection") %>%
            unique
        ## add the filenames available from VARI - use the slide_table function
        slide_tbl <- strategies$slide_table(pull_date)
        ret  <- datascope %>%
            inner_join( slide_tbl %>%
                        select(pub_subspec_id, filename) ) %>%
            ## dplyr::filter( !is.na(filename) ) %>%
            rename( "Filename" = "filename" )
        ## remove extra records associated with subspecimens - choose the latest rec
        ## (by RecordPosition) with the fewest NA entries
        ret <- dedup_by_fewest_nas( ret, pub_subspec_id,
                                   c(Tumor_Segment_Acceptable,Percent_Tumor_Nuclei,Is_Enriched),
                                   RecordPosition ) %>%
            select(-RecordPosition)
        ret
    },
    idc_slide_data = function(pull_date) {
        ## create one minimal excel (worksheets 1,2,3,8, only columns that have data)
        ## per disease type (collection)
        ## use the slide_table function strategy to reduce VARI info
        coll_tbl  <- tibble(
            study_name = c("Cancer Moonshot Biobank"),
            study_acronym = c("CMB"),
            cancer_type = c(NA),
            collection = c(NA),
            number_of_participants = c(0),
            deidentification_method_type = c("manual"),
            deidentification_method_description = c("TCIA pathology de-identification SOP"),
            license = c("CC BY 4.0    https://creativecommons.org/licenses/by/4.0/"),
            citation_or_DOI = c(""),
            phs_accession = c("phs002192"),
            acl = c("open"),
            role_or_affiliation = c("Principal Investigator"),
            first_name = c("Helen"),
            last_name = c("Moore"),
            suffix = c("PhD"),
            email = c("helen.moore@nih.gov"),
            )
        tcia_tbl <- strategies$tcia_metadata(pull_date) 
        idc_tbl   <- tcia_tbl %>%
            rename(c(
                "participant_id" = "pub_id",
                "gender" = "Gender",
                "race" = "Race",
                "ethnicity" = "Ethnicity",
                "primary_diagnosis" = "Topographic_Site",
                "sample_id" = "pub_subspec_id",
                "file_name" = "Filename",
                "collection" = "TCIA_Collection"
                )) %>%
            mutate(
                dbGaP_subject_id = participant_id,
                participant_ID = participant_id,
                file_format = c("SVS"),
                image_modality = c("SM"),
                imaging_equipment_manufacturer = c("Aperio"),
                imaging_equipment_model = c("AT2"),
                embedding_medium = c("Paraffin wax")
            ) %>%
            select(
                collection, participant_id, gender, race, ethnicity, primary_diagnosis, sample_id,
                dbGaP_subject_id, participant_ID, file_name, file_format, image_modality,
                imaging_equipment_manufacturer, imaging_equipment_model,
                embedding_medium
                )
        inventory  <- entity_ids %>% dplyr::filter( !is.na(pub_subspec_id) ) %>%
           inner_join(bcr_report, by = c("bcr_subspec_id" = "BSI ID")) %>%
            select(
                participant_id = pub_id,
                sample_id = pub_subspec_id,
                bcr_subspec_id,
                parent_id = `Parent ID`,
                organ_or_tissue = `Anatomic Site`,
                material_type = `Material Type`,
                tumor_tissue_type = `Tissue Type`,
                tissue_fixative = `Fixative or Additive`,
                collection_event = `Collection Event Name`
                ) %>%
            mutate(
                staining_method = if_else(grepl("H&E",material_type),"Hematoxylin and Eosin Staining Method","")) %>%
            mutate(
                staining_method = if_else(grepl("W-G",material_type), "Wright-Giemsa Staining Method",staining_method))         %>%
            mutate(
                staining_method = if_else(grepl("Unstained",material_type), "Unstained",staining_method))             
        ## now obtain the parent material of slides
        idc_data  <- idc_tbl %>%
            inner_join(inventory, by = c("sample_id")) %>%
            left_join(inventory %>%
                      select(bcr_subspec_id, material_type),
                      by = c("parent_id" = "bcr_subspec_id")) %>%
            rename(
                participant_id = participant_id.x,
                material_type = material_type.x,
                sample_type = material_type.y
                ) %>%
            select( -parent_id, -bcr_subspec_id, -participant_id.y )
        ## add template worksheet and column locations
        idc_mapping  <- read_excel("icd-bb-mapping-2023-10-09.xlsx")
        loc <- names(idc_data) %>% map_chr(function (s) { x <-idc_mapping %>% filter(`Field`== s ) %>% select(Worksheet, Column) ; str_c(x$Worksheet[1], x$Column[1]) })
        loc  <-  data.frame(t(loc))
        names(loc) <- names(idc_data)
        idc_data <- idc_data %>% add_row(loc[1,],.before=1)
        ## now order the columns according to location
        idc_data <- idc_data  %>% select( names(idc_data[1,order(idc_data[1,])]) )
        
    }
)

