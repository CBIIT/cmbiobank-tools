import os
from dateutil import parser
import re

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
spec = open("Merged-Spec-Patient.txt", 'r')
specfh = spec.readlines()
outputPatSpec = open("Output-Spec-Patient.txt", 'w')
outputPatSpec.write("Participant ID"+"\t"+"Age at Enrollment"+"\t"+"BirthDate"+"\t"+"Enrollment Date"+"\t"+"Calculated Birth Date"+"\t"+
                    "Primary Diagnosis (MedDRA Disease Code)"+"\t"+"Ethnicity"+"\t"+"SEX"+"\t"+"Race1"+"\t"+"Race2"+"\t"+"Race3"+"\t"+
                    "Race4"+"\t"+"Race5"+"\t"+"Race6"+"\t"+"Race7"+"\t"+"Primary Disease Site"+"\t"+"Anatomic Collection Site"+"\t"+"Treatment Response"+
                    "\t"+"Biomarker Results"+"\t"+"Smoking History"+"\t"+"Smoking Pack Years"+"\t"+"Years Smoked"+"\t"+
                    "Alcohol History"+"\t"+"Carcinogen Exposure"+"\t"+"Tumor Grade"+"\t"+"Disease stage (snoMed)"+"\t"+"Initial Diagnosis date)"+"\t"+
                    "Calculated Specimen Collection Date"+"\t"+"Collection Method"+"\t"+"Specimen ID"+"\t"+"Biospecimen Type"+"\t"+"Collection Timepoint"+"\t"+"Tissue Category"+
                    "\t"+"Public Subject ID"+"\t"+"Public specimen ID"+"\n")

for i in specfh:
    i=i.rstrip().split("\t")
    if i[0].startswith("Participant ID"):
        continue
    elif i[-8]=="":
        outputPatSpec.write("\t".join(i) + "\n")
    else:
        specDate=parser.parse(i[-8])
        enrollDate=parser.parse(i[3])
        specCol=specDate-enrollDate
        # print(specCol)
        if "," in str(specCol):
            specDateC=str(specCol).split(",")
            i.insert(-8,specDateC[0].replace(" days","").replace(" day",""))
            i.pop(-8)
            outputPatSpec.write("\t".join(i)+"\n")
        else:
            i.insert(-8, "0")
            i.pop(-8)
            outputPatSpec.write("\t".join(i) + "\n")


