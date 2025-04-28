select enrollment.project,
	enrollment.subjectId,
	enrollment.Subject as 'Participant ID',
	-- administrative_enrollment.INVNAM ,
	enrollment.siteid,
    enrollment.Site,
	AGE as 'Age',
	DSSTDAT_ENROLLMENT_RAW as 'Enrollment Date',
	ETHNIC as 'Ethnicity',
	SEX as 'Sex',
	GENDER as 'Gender',
	concat_ws(',',Race_01,Race_02, Race_03,Race_04,Race_05,Race_06,Race_07) as Race,
	CTEP_SDC_MED_V10_CD as 'Disease Term(MedDRA)',CTEPID as 'Enrolling Site CTEP ID',
	off_study.DSSTDAT_RAW as 'Off Study Date', 
	off_study.DSDECOD_OS as 'Reason for off-study',
	off_study.DSTERM_OTH_OS as 'If other specify- Reason for off study',
	off_study.BESTRESP as 'Best Overall Response',
CASE
	when ravedata.administrative_enrollment.RecordActive =0 Then 'NA'
    else ravedata.administrative_enrollment.INVNAM
    END as 'Primary Investigator'

 from ravedata.enrollment
 join  ravedata.administrative_enrollment on ravedata.enrollment.Subject=ravedata.administrative_enrollment.Subject 
 left join ravedata.off_study on enrollment.Subject=off_study.Subject;
