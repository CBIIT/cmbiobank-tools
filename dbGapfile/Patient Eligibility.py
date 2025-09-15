import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
PatientE=open("Patient Eligibility.csv",'r')
output=open("Patient Eligibility-output.txt",'w')
PatientEfh=csv.reader(PatientE)
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


#Searching in CMB Patient Eligibility file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("patient_eligibility.CSV", 'r')
interfh = csv.reader(inter)
PatientEDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="TIVERS":
                TIVERS=col
            elif i[col]=="PROTDAT_RAW":
                PROTDAT=col
            elif i[col]=="IEYN":
                IEYN=col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[TIVERS],i[PROTDAT],i[IEYN]]
            print(hh)
            if i[sub] in PatientEDict:
                if hh in PatientEDict.get(i[sub]):
                    continue
                else:
                    PatientEDict[i[sub]].append(hh)
            else:
                PatientEDict[i[sub]]=[]
                PatientEDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in PatientEfh:
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
            if hhh in PatientEDict:
                if len(PatientEDict.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), PatientEDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(PatientEDict.get(hhh)[0]) + "\n")
                else:
                    for each in PatientEDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")




