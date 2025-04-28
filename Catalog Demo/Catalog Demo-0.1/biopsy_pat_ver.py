import os,csv

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
# conco=open("oncoOutput.txt",'r')
# concofh=conco.readlines()
bio=open("CMB_biopsy_pathology_verification_and_assessment.CSV",'r')
biofh=csv.reader(bio)
bioList={}
biopsyCC=[]

for i in biofh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            # if i[col] == "SPLADQFL_X1":
            #     SPLADQFL_X1 = col
            # elif i[col] == "ENRICH":
            #     ENRICH = col
            # elif i[col] == "SPLADQFL_X2":
            #     SPLADQFL_X2 = col
            # elif i[col] == "BSREFID_DRV":
            #     BSREFID_DRV = col
            if i[col] == "MIORRES_TUCONT_X1":
                tumCont1 = col
            elif i[col] == "MIORRES_TUCONT_X2":
                tumCont2 = col
            # elif i[col] == "MIREFID":
            #     MIREFID = col
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
            search3 = i[proj]+"_"+i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
            biopsy=[search3,i[tumCont1],i[tumCont2]]
            biopsyCC.append(biopsy)
            if search3 in bioList:
                bioList[search3].append(i[tumCont1])
                bioList[search3].append(i[tumCont2])

            else:
                bioList[search3]=[]
                bioList[search3].append(i[tumCont1])
                bioList[search3].append(i[tumCont2])


oncores = open("biopsy_pathOutput.txt", 'w')
for d,a in bioList.items():
    print(d,a)
    oncores.write(d+"\t"+";".join(a)+"\n")
#
# for i in concofh:
#     i=i.rstrip().split("\t")
#     newsearch=i[0]+"_"+i[3]
#     print(newsearch,"\t",i[3])
#     if newsearch in bioList:
#             oncores.write("\t".join(i) + "\t" + "\t".join(bioList.get(newsearch)[0]) + "\n")
#     else:
#         if i[0].startswith("SubjectID"):
#             oncores.write("\t".join(i) + "\t" + "Sample suitable for analysis before Enrichment" + "\t" + "Enrichment Instructions " + "\t" + "Sample suitable for analysis after Enrichment" + "\t" + "Comment " +"\t" + "Estimated Tumor Content Before Enrichment" + "\t" + "Estimated Tumor Content After Enrichment " + "\n")
#         else:
#             oncores.write("\t".join(i) + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" +"\t" + "NA" + "\t" + "NA" + "\n")
# print(len(bioList))
# for x,y in bioList.items():
#     print(x,"value")