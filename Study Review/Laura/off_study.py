import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
supp=open("radiation.txt",'r')
suppfh=supp.readlines()
# suppfh=csv.reader(supp)

off=open("CMB_off_study.CSV",'r')
offh=csv.reader(off)
offList={}
newofflist={}

for i in offh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "DSSTDAT_RAW":
                DSSTDAT = col
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
            elif i[col] == "RecordActive":
                RecordActive = col
            elif i[col] == "project":
                proj = col
            elif i[col] == "DSDECOD_OS":
                DSDECOD_OS = col
            elif i[col] == "DSTERM_OTH_OS":
                DSTERM_OTH_OS = col
            else:
                if i[col] == "SiteNumber":
                    SiteNum = col
    else:
        if i[RecordActive]=="0":
            continue
        else:
            search3 = i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[proj] + "_" + i[SiteNum]
            offstudy=[search3,i[DSSTDAT],i[DSDECOD_OS]]
            final = [x.replace('', "NA") if x == '' else x for x in offstudy]

            if final[0] in offList:
                offList[final[0]].append(final[1])
                # offList[final[0]].append(final[2])
                # offList[final[0]].append(final[3])



            else:
                offList[final[0]] = []
                offList[final[0]].append(final[1])
                # offList[final[0]].append(final[2])
                # offList[final[0]].append(final[3])



oncores = open("offStudyOutput.txt", 'w')

for value in suppfh:
    value=value.rstrip().split("\t")
    if value[0] in offList:
        oncores.write("\t".join(value) + "\t" + str(set(offList.get(value[0]))) + "\n")
    else:
        if "Key" in value[0]:
            oncores.write("\t".join(value) + "\t" + "Off Study Date ""\n")
        else:
            oncores.write("\t".join(value) + "\t"+ "NA"+"\t"+"NA" + "\n")
#         offList.append(final)
#
# oncores = open("offStudyOutput.csv", 'w')
#
# for i in suppfh:
#     newlist = [k[0] for k in offList]
#     if i[0] in newlist:
#         for y in offList:
#             if i[0] == y[0]:
#                 oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
#     else:
#         if i[0].startswith("Key"):
#             oncores.write(",".join(i) + "," + "Off Study Date" + "\n")
#         else:
#             print(i)
#             oncores.write(",".join(i) + "," + "NA" + "\n")
