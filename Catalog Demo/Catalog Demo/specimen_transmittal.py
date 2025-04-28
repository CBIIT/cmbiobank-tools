import os,csv,xlsxwriter,xlrd,openpyxl
from CatalogData import catalog

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
filespecimen=open("specimen_transmittal.CSV",'r')
# spec_transOutput=open("specimen_transmittal_output.txt",'w')
# spec_transOutput.write("SubjectID"+"\t"+"BEDAT"+"\t"+"SPECCAT"+"\t"+"BECLMETH_SPD"+"\t"+"SPECID"+"\t"+"BESPEC_DRV"+"\t"+"ASMTTPT_DRV"+"\t"+"TISTYP"+"\t"+"BSTEST"+"\t"+"Sub Specimen ID"+"\n")
filefh=csv.reader(filespecimen)
spec = []
transList={}


for i in filefh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "BEDAT_RAW":
                bedat = col
            elif i[col] == "ASMTTPT_DRV":
                asmttpt = col
            elif i[col] == "TISTYP":
                tistyp = col
            # elif i[col] == "BSTEST":
            #     bstest = col
            elif i[col] == "SPECCAT":
                speccat = col
            elif i[col] == "BECLMETH_SPD":
                colmeth = col
            elif i[col] == "SPECID":
                specid = col
            elif i[col] == "BESPEC_DRV":
                spectype = col
            # elif i[col] == "BSREFID":
            #     BSREFID = col
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
            elif i[col] == "BSPDMRYN":
                BSPDMRYN = col
            elif i[col] == "RecordActive":
                RecordActive = col
            elif i[col] == "project":
                proj = col
            else:
                if i[col] == "SiteNumber":
                    SiteNum = col
    else:
        if i[BSPDMRYN]=="Yes" or i[RecordActive]=="0":
            continue
        else:
            search = i[proj] + "_" + i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
            y=[i[bedat],i[speccat],i[colmeth],i[specid],i[spectype],i[asmttpt],i[tistyp]]
            # spec.append(y)
            if search in transList:
                if y in transList.get(search):
                    continue
                else:
                    transList[search].append(y)

            else:
                transList[search]=[]
                transList[search].append(y)


oncores = open("specimen_transmittal_output.txt",'w')
oncores.write("SubjectID" + "\t" + "BEDAT" + "\t" + "SPECCAT" + "\t" + "BECLMETH_SPD" + "\t" + "SPECID" + "\t" + "BESPEC_DRV" + "\t" + "ASMTTPT_DRV" + "\t" + "TISTYP" + "\t" + "\n")
for g,h in transList.items():
    # print(g,h)
    if len(h)>1:
        for item in h:
            print(item)
            oncores.write(g+"\t"+"\t".join(item)+"\n")
    else:
        oncores.write(g+"\t" + "\t".join(h[0]) + "\n")


