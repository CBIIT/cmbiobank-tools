import os,csv

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
merge=open("dataMerge.txt",'r')
mergefh=merge.readlines()
bio=open("follow_up.CSV",'r')
biofh=csv.reader(bio)
bioList={}

for i in biofh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "SSORRES_SURVSTAT":
                SURSTAT = col
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
            search3 = i[proj]+"_"+i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
            if search3 in bioList:
                bioList[search3].append(i[SURSTAT])

            else:
                bioList[search3]=[]
                bioList[search3].append(i[SURSTAT])
oncores = open("Survival-StatusOutput.txt", 'w')
oncores.write("Participant ID"+"\t"+"Age at Enrollment"+"\t"+"Enrollment Date"+"\t"+"Primary Diagnosis (MedDRA Disease Code)"+"\t"+"Ethnicity"+"\t"+"SEX"+"\t"+"Race"+"\t"+"Primary Disease Site"+"\t"+"Treatment Response"+
                    "\t"+"Biomarker Results"+"\t"+"Smoking History"+"\t"+"Smoking Pack Years"+"\t"+"Years Smoked"+"\t"+
                    "Alcohol History"+"\t"+"Carcinogen Exposure"+"\t"+"Tumor Grade"+"\t"+"Disease stage (snoMed)"+"\t"+"Initial Diagnosis date)"+"\t"+
                    "Specimen Collection Date"+"\t"+"Collection Method"+"\t"+"Specimen ID"+"\t"+"Biospecimen Type"+"\t"+"Collection Timepoint"+"\t"+"Tissue Category"+
                    "\t"+"Public Subject ID"+"\t"+"Public specimen ID"+"\t"+"Anatomic Collection Site"+"\t"+"Survival Status"+"\n")

#opening the merged file Patient and Specimen information
itemDic={}
for lu in mergefh:
    lu=lu.rstrip().split("\t")
    if lu[0].startswith("Participant ID"):
        # print(lu)
        for gas in range(0, len(lu)):
            if lu[gas] == "Participant ID":
                Participant = gas

    else:
        keyItem=lu[Participant]
        itemDic[keyItem]=lu
        if keyItem in bioList:
            oncores.write("\t".join(lu)+"\t"+str(bioList.get(keyItem)[0])+"\n")
        else:
            oncores.write("\t".join(lu)+"\t"+"No value"+"\n")


#
