import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
conPrior=open("Concomitant and Prior Medicatio temp.csv",'r')
output=open("Concomitant and Prior Medication-output.txt",'w')
conPriorfh=csv.reader(conPrior)
entityfh=csv.reader(entity)
enrollDic={}

for x in entityfh:
    # print(x)
    if x[0]=="NA":
        continue
    else:
        if "ctep_id" in x[0]:
            for val in range(0,len(x)):
                # print(x[val])
                if x[val]=="pub_id":
                    pubID=val
                elif "ctep_id" in x[val]:
                    ID=val

        else:
            item=x[pubID]
            itemVal=x[ID]
            # print(itemVal,item)
            if item in enrollDic:
                if itemVal in enrollDic.get(item):
                    continue
                else:
                    print("ERRRRROORRRRRRRRRR present in dictonary")
            else:
                enrollDic[item]=itemVal
                # print(item,itemVal)


#Searching in CMB Concomitant and Prior Medication file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("concomitant_and_prior_medications.CSV", 'r')
interfh = csv.reader(inter)
conPriorDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="CMSTDAT_RAW":
                CMSTDAT=col
            elif i[col]=="CMENDAT_RAW":
                CMENDAT=col
            elif i[col] == "CMTRT":
                CMTRT = col
            elif i[col] == "CMDOSTOT":
                CMDOSTOT = col
            elif i[col] == "CMDOSU":
                CMDOSU = col
            elif i[col] == "CMDOSFRQ":
                CMDOSFRQ = col
            elif i[col] == "CMDOSRGM":
                CMDOSRGM = col
            elif i[col] == "CMINDC":
                CMINDC = col


    else:
        tab= i[sub].split("-")
        if i[RecordActive]=='0' or tab[1] > "0125":
            continue
        else:
            hh=[i[RecordId],i[CMSTDAT],i[CMENDAT],i[CMTRT],i[CMDOSTOT],i[CMDOSU],i[CMDOSFRQ],i[CMDOSRGM],i[CMINDC]]
            if i[sub] in conPriorDict:
                if hh in conPriorDict.get(i[sub]):
                    continue
                else:
                    conPriorDict[i[sub]].append(hh)
            else:
                conPriorDict[i[sub]]=[]
                conPriorDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in conPriorfh:
    if "SUBJECT_ID" in con[0]:
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub=cont
    else:
        t=con[sub]
        if t in enrollDic:
            hhh=enrollDic.get(t)
            # print(hhh,type(hhh))r
            if hhh in conPriorDict:
                if len(conPriorDict.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), conPriorDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(conPriorDict.get(hhh)[0]) + "\n")
                else:
                    for each in conPriorDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")




