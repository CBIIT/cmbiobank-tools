import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
bio=open("prior_SuppOutput.txt",'r')
biofh=bio.readlines()
# biofh=csv.reader(bio)

prior=open("CMB_prior__surgery_supplement.CSV",'r')
priorfh=csv.reader(prior)
ptList={}

for i in priorfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "THERIND":
                THERIND = col
            elif i[col] == "PRTRT":
                PRTRT = col
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
            pt=[search3,i[THERIND],i[PRTRT]]
            final = [x.replace('', "NA") if x == '' else x for x in pt]
            val_dic = [final[1] + "@THERIND", final[-1] + "@PRTRT"]
            if final[0] in ptList:
                ptList[final[0]].append(val_dic)
            else:
                ptList[final[0]] = []
                ptList[final[0]].append(val_dic)

        # ptList.append(final)

newSupp={}
for x,y in ptList.items():
    # print(x,y)
    THERIND=[item[1] for item in y]
    PRTRT=[item[0] for item in y]
    finalval=[set(THERIND),set(PRTRT)]
    newSupp[x]=finalval
out=open("prior_treatmentOutput.txt",'w')
for x in biofh:
    x=x.rstrip().split("\t")
    if x[0] in newSupp:
        print(x[0])
        out.write("\t".join(x) + "\t" + str(newSupp.get(x[0])[0]) + "\t" + str(newSupp.get(x[0])[1]) + "\n")
    else:
        if "Key" in x[0]:
            out.write("\t".join(x)+"\t"+"Therapeutic Intent"+"\t"+"Procedure Name-Prior Surgery Supplement" + "\n")
        else:
            out.write("\t".join(x) + "\t" + "NA" + "\t" + "NA" + "\n")

