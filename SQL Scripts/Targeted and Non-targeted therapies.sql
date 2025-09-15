select 
distinct(enrollment.Subject),
enrollment.Site,
CTEP_SDC_MED_V10_CD as 'Disease Code',
DSSTDAT_ENROLLMENT_RAW as 'Enrollment Date',
targeted_therapy_administration.CMSTDAT_RAW as 'Targeted Therapy Start Date',
targeted_therapy_administration.CMENDAT_RAW as 'Targeted Therapy End Date',
targeted_therapy_administration.CMTRT_DSL as 'Targeted Therapy',
prior__therapy_supplement.CMSTDAT_RAW as 'Non-targeted Start Date',
prior__therapy_supplement.CMENDAT_RAW as 'Non-targeted End Date',
prior__therapy_supplement.CMTRT as 'Non-targeted Therapy'
from enrollment
left join
targeted_therapy_administration on enrollment.Subject=targeted_therapy_administration.Subject
left join
prior__therapy_supplement on enrollment.Subject=prior__therapy_supplement.Subject
where targeted_therapy_administration.RecordActive=1
And prior__therapy_supplement.RecordActive=1;