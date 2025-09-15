Select 
distinct(specimen_transmittal.Subject),
SPECID as 'Specimen ID',
-- BSREFID as 'Sub-Specimen',
enrollment.Site,
CTEP_SDC_MED_V10_CD as 'Disease Code',
STR_TO_DATE(DSSTDAT_ENROLLMENT_RAW,'%d %b %Y') as 'Enrollment Date',
STR_TO_DATE(BSSTDAT_RAW,'%d %b %Y') as 'Start Date of Specimen',
timestampdiff(month,STR_TO_DATE(DSSTDAT_ENROLLMENT_RAW,'%d %b %Y'),STR_TO_DATE(BSSTDAT_RAW,'%d %b %Y')) as 'Months from enrollment',
datediff(STR_TO_DATE(BSSTDAT_RAW,'%d %b %Y'),STR_TO_DATE(DSSTDAT_ENROLLMENT_RAW,'%d %b %Y')) as 'Days from Enrollment',
ravedata.targeted_therapy_administration.CMSTDAT_RAW as 'Start Date of Targeted Therapy',
ravedata.prior__therapy_supplement.CMSTDAT_RAW as ' Date of First Dose Non-Targeted therapy',
ASMTTPT_DRV as 'Assesment Timepoint',
SPECCAT as 'Specimen Category',
BSTEST as 'Biospecimen Test Name',
BECLMETH_SPD as 'Collection Method'



from ravedata.specimen_transmittal
join ravedata.enrollment 
	on specimen_transmittal.Subject=enrollment.Subject
left join ravedata.targeted_therapy_administration 
	on specimen_transmittal.Subject=targeted_therapy_administration.Subject
left join ravedata.prior__therapy_supplement 
	on specimen_transmittal.Subject=prior__therapy_supplement.Subject
    
where 
specimen_transmittal.RecordActive=1 AND 
ASMTTPT_DRV='ON TREATMENT' AND 
BECLMETH_SPD='Blood Draw' AND 
targeted_therapy_administration.RecordActive=1 AND 
prior__therapy_supplement.RecordActive=1
and BSSTDAT_RAW <> 'NULL'
and BSSTDAT_RAW
group by BSSTDAT_RAW;

-- INTO OUTFILE '/Users/amohandas/Desktop/myresults.txt';

