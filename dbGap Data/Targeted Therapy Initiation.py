import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
TargetedIn=open("Targeted Therapy Initiation.csv",'r')
output=open("Targeted Therapy Initiation-output.txt",'w')
TargetedInfh=csv.reader(TargetedIn)
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


#Searching in CMB Targeted Therapy Initiation file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("course_initiation.CSV", 'r')
interfh = csv.reader(inter)
TargetedInDict={}
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
            elif i[col]=="INTVN_BEG_DT_RAW":
                INTVN_BEG_DT=col
            elif i[col]=="MALG_NEO_ANTM_TP":
                MALG_NEO_ANTM_TP=col
            elif i[col]=="WEIGHT_VSORRES":
                WEIGHT_VSORRES=col
            elif i[col]=="HEIGHT_VSORRES":
                HEIGHT_VSORRES=col
            elif i[col]=="BSA_VSORRES":
                BSA_VSORRES=col


    else:
        ee=i[sub].split("-")
        if i[RecordActive]=='0' or ee[1] >"0125":
            continue
        else:
            hh=[i[RecordId],i[TX_CYCLE_NUM],i[INTVN_BEG_DT],i[MALG_NEO_ANTM_TP],i[WEIGHT_VSORRES],i[HEIGHT_VSORRES],i[BSA_VSORRES]]
            if i[sub] in TargetedInDict:
                if hh in TargetedInDict.get(i[sub]):
                    continue
                else:
                    TargetedInDict[i[sub]].append(hh)
            else:
                TargetedInDict[i[sub]]=[]
                TargetedInDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in TargetedInfh:
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
            if hhh in TargetedInDict:
                if len(TargetedInDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), TargetedInDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(TargetedInDict.get(hhh)[0]) + "\n")
                else:
                    for each in TargetedInDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")



