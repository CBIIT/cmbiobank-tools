import os

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
spec = open("Patient-Data.txt", 'r')
specfh = spec.readlines()
pat=open("specimen_transmittal_id_output.txt",'r')
patfh=pat.readlines()
outputPatSpec = open("Merged-Spec-Patient.txt", 'w')
outputPatSpec.write("Participant ID"+"\t"+"Age at Enrollment"+"\t"+"BirthDate"+"\t"+"Enrollment Date"+"\t"+"Calculated Birth Date"+"\t"+
                    "Primary Diagnosis (MedDRA Disease Code)"+"\t"+"Ethnicity"+"\t"+"SEX"+"\t"+"Race1"+"\t"+"Race2"+"\t"+"Race3"+"\t"+
                    "Race4"+"\t"+"Race5"+"\t"+"Race6"+"\t"+"Race7"+"\t"+"Primary Disease Site"+"\t"+"Treatment Response"+
                    "\t"+"Biomarker Results"+"\t"+"Smoking History"+"\t"+"Smoking Pack Years"+"\t"+"Years Smoked"+"\t"+
                    "Alcohol History"+"\t"+"Carcinogen Exposure"+"\t"+"Tumor Grade"+"\t"+"Disease stage (snoMed)"+"\t"+"Initial Diagnosis date)"+"\t"+
                    "Specimen Collection Date"+"\t"+"Collection Method"+"\t"+"Specimen ID"+"\t"+"Biospecimen Type"+"\t"+"Collection Timepoint"+"\t"+"Tissue Category"+
                    "\t"+"Public Subject ID"+"\t"+"Public specimen ID"+"\n")

Patient = {}

for i in specfh:
    i=i.rstrip().split("\t")
    if i[0].startswith("Participant ID"):
        for col in range(0, len(i)):
            if i[col] == "Participant ID":
                Participant_ID = col

    else:
        if i[Participant_ID] in Patient:
            print("ERRRRROORRRRRRRRR")
        else:
            Patient[i[Participant_ID]]=i[1:]

for x in patfh:
    x=x.rstrip().split("\t")

for m,n in Patient.items():
    # print(m)
    for x in patfh:
        # print(x)
        x = x.rstrip().split("\t")
        x.pop(2)
        if m == x[0]:
            # print(m+"\t"+"\t".join(n)+"\t"+"\t".join(x[1:])+"\n")
            outputPatSpec.write(m+"\t"+"\t".join(n)+"\t"+"\t".join(x[1:])+"\n")

