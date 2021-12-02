import os,csv

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
# f=open("CourseOutput.txt",'r')
# fh=f.readlines()
file=open("CMB_targeted_therapy_administration.CSV",'r')
fileH=csv.reader(file)
targetedC=[]
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
            targetedC.append(ll)
            # final = [x.replace('', "NA") if x == '' else x for x in ll]
            if search3 in TargetList:
                TargetList[search3].append(i[CMTRT_DSL])
            else:
                TargetList[search3] = []
                TargetList[search3].append(i[CMTRT_DSL])

oncores = open("Targeted_TherapyOutput.txt", 'w')
for x, y in TargetList.items():
    print(x,y)
    oncores.write(x+"\t"+";".join(y)+"\n")

# for value in fh:
#     value=value.rstrip().split("\t")
#     if value[0] in TargetList:
#         oncores.write("\t".join(value) + "\t" + str(set(TargetList.get(value[0]))) + "\n")
#     else:
#         if "Key" in value[0]:
#             oncores.write("\t".join(value)+"\t"+"Therapy-Targeted Therapy" + "\n")
#         else:
#             oncores.write("\t".join(value) + "\t" + "NA" + "\n")
