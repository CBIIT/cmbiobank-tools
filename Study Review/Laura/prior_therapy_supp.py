import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
prio=open("HistologyOutput.txt",'r')
priofh=prio.readlines()
# priofh=csv.reader(prio)

supp=open("prior__therapy_supplement.CSV")
suppfh=csv.reader(supp)
suppList={}

for i in suppfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "CMTRT":
                CMTRT = col
            elif i[col] == "CMCAT":
                CMCAT = col
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
            else:
                if i[col] == "SiteNumber":
                    SiteNum = col
    else:
        if i[RecordActive]=="0":
            continue
        else:
            search3 = i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[proj] + "_" + i[SiteNum]
            val=[i[CMTRT]+"@CMTRT",i[CMCAT]+"@CMCAT"]
            if search3 in suppList:
                    suppList[search3].append(val)
            else:
                suppList[search3]=[]
                suppList[search3].append(val)

oncores = open("prior_SuppOutput.txt", 'w')

newSupp={}
for x,y in suppList.items():
    print(x,y)
    CMTRT_val=[item[0] for item in y]
    CMCAT_val=[item[1] for item in y]
    finalval=[set(CMTRT_val),set(CMCAT_val)]
    newSupp[x]=finalval

for i in priofh:
    i=i.rstrip().split("\t")
    if i[0] in newSupp:
        oncores.write("\t".join(i)+"\t"+str(newSupp.get(i[0])[0])+"\t"+str(newSupp.get(i[0])[1])+"\n")
    else:
        if "Key" in i[0]:
            oncores.write("\t".join(i) + "\t" + "CMTRT-Prior Therapy" + "\t" + "CMCAT-Prior Therapy" + "\n")
        else:
            oncores.write("\t".join(i)+"\t"+"NA"+"\t"+"NA"+"\n")