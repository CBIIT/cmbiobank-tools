import os,csv

#Adding primary Investigators namefrom administrative enrollment form
os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
supp=open("enrollmentData.txt",'r')
suppfh=supp.readlines()
# suppfh=csv.reader(supp)

off=open("administrative_enrollment.CSV",'r')
offh=csv.reader(off)
offList={}
newofflist={}

for i in offh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "ZIPCD":
                ZIPCD = col
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
            offstudy=[search3,i[ZIPCD]]
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



oncores = open("adminEnrollOutput.txt", 'w')

for value in suppfh:
    value=value.rstrip().split("\t")
    if value[0] in offList:
        oncores.write("\t".join(value) + "\t" + str(set(offList.get(value[0]))) + "\n")
    else:
        if "Key" in value[0]:
            oncores.write("\t".join(value) + "\t" + "Zip Code""\n")
        else:
            oncores.write("\t".join(value) + "\n")