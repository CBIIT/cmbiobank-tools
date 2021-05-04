strategies <- list(
    chkids = function (pull_date) {
        dta$specimen_transmittal %>%
        select(Subject,SPECID,BSREFID) %>% unique %>%
        anti_join(entity_ids, by = c("Subject"="ctep_id","SPECID"="rave_spec_id", "BSREFID"="bcr_subspec_id")) %>%
        select(Subject,SPECID,BSREFID) %>%
        mutate("Pull date" = pull_date) 
    },
    entity_ids = function (pull_date) {
        entity_ids
    },
    iroc = function (pull_date) {
        cras  <- read_excel(config$cra_excel,1)
        dta$enrollment %>% left_join(pub_ids, by=c("Subject" = "ctep_id")) %>%
            select(project, Subject, Site,CTEPID, DSSTDAT_ENROLLMENT_RAW,CTEP_SDC_MED_V10_CD, pub_id,up_id) %>%
            left_join( dta$shipping_status %>%
              select(Subject, EMAIL_SHP) %>%
                                        # inner_join(cras,by=c("EMAIL_SHP" = "Email")) %>%
              group_by(Subject) %>%
              summarize( CRA = first(EMAIL_SHP)),
              by = c("Subject")) %>%
        transmute("Date Created" = str_interp("${pull_date}"),
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
        entity_ids <- pub_ids %>% left_join(pub_spec_ids,by = c("pub_id","ctep_id","up_id")) %>% select( pub_id,ctep_id,up_id,rave_spec_id, pub_spec_id,log_line) %>% left_join(pub_subspec_ids,by=c("pub_id","ctep_id","pub_spec_id"))
    },
    update_ids = function (pull_date) {
        # orphans - no pub_id or pub_spec_id yet
        orphans <- dta$specimen_transmittal %>%
            select(Subject,SPECID,BSREFID,USUBJID_DRV) %>% unique %>%
            anti_join(entity_ids, by = c("Subject"="ctep_id",
                                         "SPECID"="rave_spec_id",
                                         "BSREFID"="bcr_subspec_id",
                                         "USUBJID_DRV"="up_id"))
        ## newbies - new patients without pub_id
        newbies  <- orphans %>% anti_join(entity_ids,
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
            inner_join(unused %>% mutate(num = row_number())) %>% select(-num)
        ## set the newbies' pub_ids in orphans (adding pub_id column to orphans)
        orphans_a <- bind_rows(
            orphans %>%
            inner_join(entity_ids %>%
                       select(ctep_id,up_id,pub_id) %>%
                       group_by(ctep_id,up_id) %>%
                       summarize(pub_id = first(pub_id)),
                       by = c("Subject" = "ctep_id",
                              "USUBJID_DRV" = "up_id") ),
            orphans %>% inner_join(assgn,by = c("Subject","USUBJID_DRV")))
        ## now handle specimen assignment
        assgn_b <- orphans_a %>%
            anti_join( entity_ids,
                      by=c("pub_id",
                           "Subject"="ctep_id",
                           "USUBJID_DRV"="up_id",
                           "SPECID" = "rave_spec_id") ) %>%
            mutate(pub_spec_id = str_c(pub_id,str_pad(str_extract(SPECID,"[0-9]+$"),2,"left","0" ),sep="-"))
        orphans_b  <- rbind(
            orphans_a %>%
            inner_join( entity_ids %>%
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
        nxt  <- entity_ids %>%
            select(pub_spec_id,pub_subspec_id) %>%
            group_by(pub_spec_id) %>% arrange(pub_spec_id) %>%
            summarize(pub_subspec_id = last(pub_subspec_id)) %>%
            mutate( ssid = as.integer(str_extract(pub_subspec_id,"[0-9]+$"))+1) %>%
            mutate_at(vars(ssid),list(function(x)if_else(is.na(x),1,x)))
        next_ssid  <- NULL
        next_ssid[nxt$pub_spec_id] <- nxt$ssid
        next_ssid_for  <- function(ps_id) {
            n <- next_ssid[ps_id] ;
            if (is.na(n)) {
                next_ssid[ps_id] <<- 1
                n  <- 1
            } else {
                next_ssid[ps_id]  <<- next_ssid[ps_id]+1
                n  <- next_ssid[ps_id]
            }
            str_c(ps_id,str_pad(n,2,"left",0),sep="-") }
        orphans_ss  <- orphans_b %>%
            arrange(pub_spec_id,BSREFID) %>%
            add_column(
                pub_subspec_id = sapply(
                (orphans_b %>% arrange(pub_spec_id,BSREFID))$pub_spec_id,
                next_ssid_for, USE.NAMES=F) )
        entity_ids_upd  <- orphans_ss %>%
            full_join(entity_ids, by=c("Subject"="ctep_id",
                                       "USUBJID_DRV"="up_id",
                                       "SPECID"="rave_spec_id",
                                       "BSREFID"="bcr_subspec_id",
                                       "pub_id","pub_spec_id")) %>%
            mutate( pub_subspec_id = coalesce(pub_subspec_id.x,pub_subspec_id.y)) %>%
            select( -pub_subspec_id.x,-pub_subspec_id.y, -log_line.x,-log_line.y) %>%
            rename( ctep_id = Subject, up_id = USUBJID_DRV, rave_spec_id = SPECID, bcr_subspec_id = BSREFID)
    }
)


