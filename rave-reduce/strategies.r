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
    })



