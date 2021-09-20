import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
cour=open("Targeted_TherapyOutput.txt",'r')
courfh=cour.readlines()
# courfh=csv.reader(cour)
hist=open("CMB_histology_and_disease.CSV",'r')
histfh=csv.reader(hist)
histoList={}

for i in histfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "HISTSUBT":
                HISTSUBT = col
            elif i[col] == "subjectId":
                # print(line[i],i)
                subId = col
            elif i[col] == "Subject":
                # print(line[i], i)
                sub = col
            elif i[col] == "siteid":
                siteid = col
            elif i[col] == "RecordActive":
                RecordActive = col
            elif i[col] == "Site":
                Site = col
            elif i[col] == "project":
                proj = col
            else:
                if i[col] == "SiteNumber":
                    SiteNum = col
    else:
        if i[RecordActive]=="0":
            continue
        else:
            search3 = i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[proj] + "_" + i[SiteNum]
            val=[search3,i[HISTSUBT]]
            final = [x.replace('', "NA") if x == '' else x for x in val]
            # histoList.append(final)
            if final[0] in histoList:
                histoList[final[0]].append(final[1])
            else:
                histoList[final[0]]=[]
                histoList[final[0]].append(final[1])

oncores = open("HistologyOutput.txt", 'w')

for value in courfh:
    value=value.rstrip().split("\t")
    if value[0] in histoList:
        oncores.write("\t".join(value) + "\t" + str(set(histoList.get(value[0]))) + "\n")
    else:
        if "Key" in value[0]:
            oncores.write("\t".join(value) +"\t"+"Histologic Subtype" "\n")
        else:
            oncores.write("\t".join(value) + "\t" + "NA" + "\n")
