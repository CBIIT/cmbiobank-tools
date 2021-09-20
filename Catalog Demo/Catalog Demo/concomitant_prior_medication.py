import os, csv
from CatalogData import catalog

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
concomitamt=open("CMB_concomitant_and_prior_medications.CSV",'r')
output=open("Concomitant_and_prior_medication.txt",'w')
output.write("SubjectID" + "\t" + "CMTRT" + "\n")

confh=csv.reader(concomitamt)
concomit=[]

for i in confh :
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "CMTRT":
                cmtrt = col
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
        search = i[proj] + "_" + i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
        v=[search,i[cmtrt]]
        concomit.append(v)

for l,h in catalog.items():
    for j in concomit:
        if l in j:
            output.write("\t".join(j)+"\n")
            print(j)
        else:
            continue