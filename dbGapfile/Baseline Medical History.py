import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
BaselineMed=open("Baseline Medical History.csv",'r')
output=open("5a_BaselineMedicalHistory.txt",'w')
BaselineMedfh=csv.reader(BaselineMed)
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


#Searching in CMB Baseline Medical History file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("baseline_medical_history.CSV", 'r')
interfh = csv.reader(inter)
BaselineMedDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="MHDAT_RAW":
                MHDAT=col
            elif i[col]=="MHBODSYS_SPD":
                MHBODSYS_SPD=col
            elif i[col]=="MHTERM":
                MHTERM=col

    else:
        xx=i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[RecordId],i[MHDAT],i[MHBODSYS_SPD],i[MHTERM]]
            if i[sub] in BaselineMedDict:
                if hh in BaselineMedDict.get(i[sub]):
                    continue
                else:
                    BaselineMedDict[i[sub]].append(hh)
            else:
                BaselineMedDict[i[sub]]=[]
                BaselineMedDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in BaselineMedfh:
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
            if hhh in BaselineMedDict:
                if len(BaselineMedDict.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), BaselineMedDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(BaselineMedDict.get(hhh)[0]) + "\n")
                else:
                    for each in BaselineMedDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")




