import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
f=open("CourseOutput.txt",'r')
fh=f.readlines()
file=open("CMB_targeted_therapy_administration.CSV",'r')
fileH=csv.reader(file)

TargetList={}
for i in fileH:
        if i[0].startswith("projectid"):
            for col in range(0, len(i)):
                if i[col] == "CMTRT_DSL":
                    CMTRT_DSL = col
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
            search3 = i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[proj] + "_" + i[SiteNum]
            ll=[search3,i[CMTRT_DSL]]
            final = [x.replace('', "NA") if x == '' else x for x in ll]
            if final[0] in TargetList:
                TargetList[final[0]].append(final[1])
            else:
                TargetList[final[0]] = []
                TargetList[final[0]].append(final[1])

oncores = open("Targeted_TherapyOutput.txt", 'w')

for x, y in TargetList.items():
    print(y)

for value in fh:
    value=value.rstrip().split("\t")
    if value[0] in TargetList:
        oncores.write("\t".join(value) + "\t" + str(set(TargetList.get(value[0]))) + "\n")
    else:
        if "Key" in value[0]:
            oncores.write("\t".join(value)+"\t"+"Therapy-Targeted Therapy" + "\n")
        else:
            oncores.write("\t".join(value) + "\t" + "NA" + "\n")
