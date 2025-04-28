import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
SurgerySupp=open("Prior Surgery Supplement.csv",'r')
output=open("5a_NonTargetedSurgerySupplement.txt",'w')
SurgerySuppfh=csv.reader(SurgerySupp)
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


#Searching in CMB Prior Surgery Supplement file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("prior__surgery_supplement.CSV", 'r')
interfh = csv.reader(inter)
SurgerySuppDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordId":
                RecordPosition=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="PRSTDAT_RAW":
                PRSTDAT=col
            elif i[col]=="PRTRT":
                PRTRT=col
            elif i[col] == "PRLOC_SURG":
                PRLOC_SURG= col
            elif i[col] == "PRFIND":
                PRFIND = col
            elif i[col] == "RSDZEXT":
                RSDZEXT = col
            elif i[col] == "THERIND":
                THERIND = col

    else:
        ee= i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[PRSTDAT],i[PRTRT],i[PRLOC_SURG],i[PRFIND],i[RSDZEXT],i[THERIND],i[RecordPosition]]
            if i[sub] in SurgerySuppDict:
                if hh in SurgerySuppDict.get(i[sub]):
                    continue
                else:
                    SurgerySuppDict[i[sub]].append(hh)
            else:
                SurgerySuppDict[i[sub]]=[]
                SurgerySuppDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in SurgerySuppfh:
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub=cont
    else:
        t=con[sub]
        if t in enrollDic:
            hhh=enrollDic.get(t)
            # print(hhh,type(hhh))r
            if hhh in SurgerySuppDict:
                if len(SurgerySuppDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), SurgerySuppDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(SurgerySuppDict.get(hhh)[0]) + "\n")
                else:
                    for each in SurgerySuppDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")



