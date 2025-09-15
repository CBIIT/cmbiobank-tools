import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
histo=open("HistologyOutput.csv",'r')
histofh=csv.reader(histo)
conco=open("CMB_concomitant_and_prior_medications.CSV",'r')
concofh=csv.reader(conco)
concoList=[]

for i in concofh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "CMSTDAT":
                CMSTDAT = col
            elif i[col] == "CMENDAT":
                CMENDAT = col
            elif i[col] == "CMTRT":
                CMTRT = col
            elif i[col] == "CMDOSFRQ":
                CMDOSFRQ = col
            elif i[col] == "CMINDC":
                CMINDC = col
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
        con=[search3,i[CMSTDAT],i[CMENDAT],i[CMTRT],i[CMDOSFRQ],i[CMINDC]]
        final = [x.replace('', "NA") if x == '' else x for x in con]
        concoList.append(final)

oncores = open("Concomitant_prior_medOutput.csv", 'w')

for i in histofh:
    newlist = [k[0] for k in concoList]
    if i[0] in newlist:
        for y in concoList:
            if i[0] == y[0]:
                oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
    else:
        if i[0].startswith("key"):
            oncores.write(",".join(i) + "," + "CMSTDAT" + "," + "CMENDAT" + "," + "CMTRT" + "," + "CMDOSFRQ" + "," + "CMINDC" + "\n")
        else:
            print(i)
            oncores.write(
                ",".join(i) + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "\n")