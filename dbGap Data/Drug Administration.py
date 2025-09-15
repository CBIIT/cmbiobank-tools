import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
DrugAd=open("Drug Administration.csv",'r')
output=open("Drug Administration-output.txt",'w')
DrugAdfh=csv.reader(DrugAd)
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


#Searching in CMB Drug Administration  file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("targeted_therapy_administration.CSV", 'r')
interfh = csv.reader(inter)
DrugAdDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="TX_CYCLE_NUM":
                TX_CYCLE_NUM=col
            elif i[col]=="CMSTDAT_RAW":
                CMSTDAT=col
            elif i[col]=="CMENDAT_RAW":
                CMENDAT=col
            elif i[col]=="CMTRT_DSL":
                CMTRT_DSL=col
            elif i[col]=="CMDOSFRQ":
                CMDOSFRQ=col


    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] >"0125":
            continue
        else:
            hh=[i[RecordId],i[TX_CYCLE_NUM],i[CMSTDAT],i[CMENDAT],i[CMTRT_DSL],i[CMDOSFRQ]]
            if i[sub] in DrugAdDict:
                if hh in DrugAdDict.get(i[sub]):
                    continue
                else:
                    DrugAdDict[i[sub]].append(hh)
            else:
                DrugAdDict[i[sub]]=[]
                DrugAdDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in DrugAdfh:
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
            if hhh in DrugAdDict:
                if len(DrugAdDict.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), DrugAdDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(DrugAdDict.get(hhh)[0]) + "\n")
                else:
                    for each in DrugAdDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")




