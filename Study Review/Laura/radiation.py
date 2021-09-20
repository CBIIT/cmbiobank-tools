import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
onco=open("prior_treatmentOutput.txt",'r')
oncofh=onco.readlines()
# oncofh=csv.reader(onco)
socio=open("CMB_prior__radiation_supplement.CSV")
sociofh=csv.reader(socio)
radioList={}

for soc in sociofh:
    if soc[0].startswith("projectid"):
        for col in range(0, len(soc)):
            if soc[col] == "PRTRT_RAD":
                PRTRT_RAD = col
            elif soc[col] == "subjectId":
                # print(line[i],i)
                subId = col
            elif soc[col] == "Subject":
                # print(line[i], i)
                sub = col
            elif soc[col] == "siteid":
                siteid = col
            elif soc[col] == "Site":
                Site = col
            elif soc[col] == "RecordActive":
                RecordActive = col
            elif soc[col] == "project":
                proj = col
            else:
                if soc[col] == "SiteNumber":
                    SiteNum = col
    else:
        if soc[RecordActive]=="0":
            continue
        else:
            search3 = soc[subId]+"_"+soc[sub]+"_"+soc[siteid]+"_"+soc[Site]+"_"+soc[proj]+"_"+soc[SiteNum]
            socEnv=[search3,soc[PRTRT_RAD]]
            final = [x.replace('', "NA") if x == '' else x for x in socEnv]
            if final[0] in radioList:
                radioList[final[0]].append(final[1])
            else:
                radioList[final[0]] = []
                radioList[final[0]].append(final[1])

oncores = open("radiation.txt", 'w')

for value in oncofh:
    value=value.rstrip().split("\t")
    if value[0] in radioList:
        oncores.write("\t".join(value) + "\t" + str(set(radioList.get(value[0]))) + "\n")
    else:
        if "Key" in value[0]:
            oncores.write("\t".join(value) + "\t" + "Procedure Name-Radiation Supplement" "\n")
        else:
            oncores.write("\t".join(value) + "\t" + "NA" + "\n")
#         socioList.append(final)
#
# sociOut=open("radiation.csv",'w')
# for i in oncofh:
#     newlist = [k[0] for k in socioList]
#     if i[0] in newlist:
#         for y in socioList:
#             if i[0] == y[0]:
#                 sociOut.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
#     else:
#         if i[0].startswith("Key"):
#             sociOut.write(",".join(i) + "," + "Radiation Supplement-Procedure Name" + "\n")
#         else:
#             sociOut.write(",".join(i) + "," + "NA" + "\n")
