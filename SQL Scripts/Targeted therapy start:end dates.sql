select 
distinct(targeted_therapy_administration.Subject),
targeted_therapy_administration.Site,
CTEP_SDC_MED_V10_CD as 'Disease Code',
DSSTDAT_ENROLLMENT_RAW as 'Enrollment Date',
CMSTDAT_RAW as 'Targeted Therapy Start Date',
CMENDAT_RAW as 'Targeted Therapy End Date',
CMTRT_DSL as 'Targeted Therapy'
from targeted_therapy_administration
left join
enrollment on targeted_therapy_administration.Subject=enrollment.Subject
where targeted_therapy_administration.RecordActive=1;