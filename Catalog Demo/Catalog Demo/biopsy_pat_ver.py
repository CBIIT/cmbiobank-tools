import os,csv

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
merge=open("Merged-Spec-Patient.txt",'r')
mergefh=merge.readlines()
bio=open("biopsy_pathology_verification_and_assessment.CSV",'r')
biofh=csv.reader(bio)
bioList={}

for i in biofh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "MILOC":
                MILOC = col
            # elif i[col] == "ENRICH":
            #     ENRICH = col
            # elif i[col] == "SPLADQFL_X2":
            #     SPLADQFL_X2 = col
            # elif i[col] == "BSREFID_DRV":
            #     BSREFID_DRV = col
            # elif i[col] == "MIORRES_TUCONT_X1":
            #     tumCont1 = col
            # elif i[col] == "MIORRES_TUCONT_X2":
            #     tumCont2 = col
            elif i[col] == "MIREFID":
                MIREFID = col
            # elif i[col] == "COVAL":
            #     COVAL = col
            elif i[col] == "RecordActive":
                RecordActive = col
            elif i[col] == "subjectId":
                # print(line[i],i)
                subId = col
            elif i[col] == "Subject":
                # print(line[i], i)
                sub = col
            elif i[col] == "siteid":
                siteid = col
            elif i[col] == "Site":
                Site = col
            elif i[col] == "project":
                proj = col
            else:
                if i[col] == "SiteNumber":
                    SiteNum = col
    else:
        if i[RecordActive]=='0':
            continue
        else:
            search3 = i[proj]+"_"+i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]+"_"+i[MIREFID]
            if search3 in bioList:
                bioList[search3].append(i[MILOC])

            else:
                bioList[search3]=[]
                bioList[search3].append(i[MILOC])
oncores = open("biopsy_pathOutput.txt", 'w')
oncores.write("Participant ID"+"\t"+"Age at Enrollment"+"\t"+"BirthDate"+"\t"+"Enrollment Date"+"\t"+"Calculated Birth Date"+"\t"+
                    "Primary Diagnosis (MedDRA Disease Code)"+"\t"+"Ethnicity"+"\t"+"SEX"+"\t"+"Race1"+"\t"+"Race2"+"\t"+"Race3"+"\t"+
                    "Race4"+"\t"+"Race5"+"\t"+"Race6"+"\t"+"Race7"+"\t"+"Primary Disease Site"+"\t"+"Treatment Response"+
                    "\t"+"Biomarker Results"+"\t"+"Smoking History"+"\t"+"Smoking Pack Years"+"\t"+"Years Smoked"+"\t"+
                    "Alcohol History"+"\t"+"Carcinogen Exposure"+"\t"+"Tumor Grade"+"\t"+"Disease stage (snoMed)"+"\t"+"Initial Diagnosis date)"+"\t"+
                    "Specimen Collection Date"+"\t"+"Collection Method"+"\t"+"Specimen ID"+"\t"+"Biospecimen Type"+"\t"+"Collection Timepoint"+"\t"+"Tissue Category"+
                    "\t"+"Public Subject ID"+"\t"+"Public specimen ID"+"\t"+"Anatomic Collection Site"+"\n")

#opening the merged file Patient and Specimen information
itemDic={}
for lu in mergefh:
    lu=lu.rstrip().split("\t")
    if lu[0].startswith("Participant ID"):
        # print(lu)
        for gas in range(0, len(lu)):
            if lu[gas] == "Participant ID":
                Participant = gas
            elif lu[gas]=="Specimen ID":
                 SpecimenID=gas
    else:
        keyItem=lu[Participant]+"_"+lu[SpecimenID]
        itemDic[keyItem]=lu
        if keyItem in bioList:
            oncores.write("\t".join(lu)+"\t"+str(bioList.get(keyItem)[0])+"\n")
        else:
            oncores.write("\t".join(lu)+"\t"+"No value"+"\n")









# for d,a in bioList.items():
#     print(d,a)
#     oncores.write(d+"\t"+";".join(a)+"\n")
#
