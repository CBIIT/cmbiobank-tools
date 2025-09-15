import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
Followup=open("Follow Up.csv",'r')
output=open("Follow Up-output.txt",'w')
FollowUpfh=csv.reader(Followup)
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


#Searching in CMB Follow Up file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("follow_up.CSV", 'r')
interfh = csv.reader(inter)
followUpDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="SSDAT_RAW":
                SSDAT=col
            elif i[col]=="SSORRES_SURVSTAT":
                SSORRES_SURVSTAT=col


    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] > '0125':
            continue
        else:
            hh=[i[SSDAT],i[SSORRES_SURVSTAT]]
            if i[sub] in followUpDict:
                if hh in followUpDict.get(i[sub]):
                    continue
                else:
                    followUpDict[i[sub]].append(hh)
            else:
                followUpDict[i[sub]]=[]
                followUpDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in FollowUpfh:
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
            if hhh in followUpDict:
                if len(followUpDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), followUpDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(followUpDict.get(hhh)[0]) + "\n")
                else:
                    for each in followUpDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")




