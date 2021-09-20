import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
off=open("offStudyOutput.csv",'r')
offh=csv.reader(off)
blood=open("CMB_blood_collection_adverse_event_presence.CSV",'r')
bloodfh=csv.reader(blood)
bloodList=[]

for i in bloodfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "AEYN":
                AEYN = col
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
        bll=[search3,i[AEYN]]
        final = [x.replace('', "NA") if x == '' else x for x in bll]
        bloodList.append(final)

oncores = open("BloodCollection_Output.csv", 'w')

for i in offh:
    newlist = [k[0] for k in bloodList]
    if i[0] in newlist:
        for y in bloodList:
            if i[0] == y[0]:
                oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
    else:
        if i[0].startswith("key"):
            oncores.write(",".join(i) + "," + "AEYN" + "\n")
        else:
            print(i)
            oncores.write(",".join(i) + "," + "NA"+  "\n")