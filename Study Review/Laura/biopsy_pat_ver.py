import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
conco=open("oncoOutput.txt",'r')
concofh=conco.readlines()
bio=open("biopsy_pathology_verification_and_assessment.CSV",'r')
biofh=csv.reader(bio)
bioList={}

for i in biofh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "SPLADQFL_X1":
                SPLADQFL_X1 = col
            elif i[col] == "ENRICH":
                ENRICH = col
            elif i[col] == "SPLADQFL_X2":
                SPLADQFL_X2 = col
            elif i[col] == "BSREFID_DRV":
                BSREFID_DRV = col
            elif i[col] == "MIORRES_TUCONT_X1":
                tumCont1 = col
            elif i[col] == "MIORRES_TUCONT_X2":
                tumCont2 = col
            elif i[col] == "MIREFID":
                MIREFID = col
            elif i[col] == "COVAL":
                COVAL = col
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
            search3 = i[proj]+"_"+i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]+"_"+i[MIREFID]+"_"+i[BSREFID_DRV]
            biopsy=[search3,i[SPLADQFL_X1],i[ENRICH],i[SPLADQFL_X2],i[COVAL],i[tumCont1],i[tumCont2]]
            final = [x.replace('', "NA") if x == '' else x for x in biopsy]
            sub_final=final[1:]
            # print(final)
            # print(final,sub_final)
            if final[0] in bioList:
                if bioList.get(search3)[0]==['NA','NA','NA','NA','NA','NA'] and sub_final !=['NA','NA','NA','NA','NA','NA']:
                    # print(final[0],"NO")
                    bioList[search3].append(sub_final)
                    bioList[search3].pop(0)
                    # print(search3,sub_final, "new key with all values")
                elif bioList.get(search3)[0] == ['NA', 'NA', 'NA', 'NA','NA','NA'] and sub_final == ['NA', 'NA', 'NA', 'NA','NA','NA']:
                    # print(search3,sub_final,"same values")
                    continue
                elif bioList.get(search3)[0]==sub_final:
                    print(search3,sub_final)
                    continue
                else:
                    print("ERORRRRRRR",final[0], sub_final)
            else:
                bioList[search3]=[]
                bioList[search3].append(sub_final)
            # print(final[0], sub_final, "myyyyyyy")


oncores = open("biopsy_pathOutput.txt", 'w')
#
for i in concofh:
    i=i.rstrip().split("\t")
    newsearch=i[0]+"_"+i[3]
    print(newsearch,"\t",i[3])
    if newsearch in bioList:
            oncores.write("\t".join(i) + "\t" + "\t".join(bioList.get(newsearch)[0]) + "\n")
    else:
        if i[0].startswith("SubjectID"):
            oncores.write("\t".join(i) + "\t" + "Sample suitable for analysis before Enrichment" + "\t" + "Enrichment Instructions " + "\t" + "Sample suitable for analysis after Enrichment" + "\t" + "Comment " +"\t" + "Estimated Tumor Content Before Enrichment" + "\t" + "Estimated Tumor Content After Enrichment " + "\n")
        else:
            oncores.write("\t".join(i) + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" +"\t" + "NA" + "\t" + "NA" + "\n")
print(len(bioList))
# for x,y in bioList.items():
#     print(x,"value")