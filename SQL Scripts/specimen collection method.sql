select 
distinct(specimen_transmittal.Subject),
specimen_transmittal.Site,
SPECID as 'Specimen ID',
SPECCAT as 'Specimen Category',
BECLMETH_SPD as 'Collection Method',
BESPEC_DRV as 'Specimen Type',
CTEP_SDC_MED_V10_CD as 'Disease Code'
 from specimen_transmittal
 join enrollment on specimen_transmittal.Subject=enrollment.Subject
where specimen_transmittal.RecordActive=1
and SPECCAT <> 'Blood';