import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
TargetedAss=open("Targeted Therapy Assessment.csv",'r')
output=open("Targeted Therapy Assessment-output.txt",'w')
TargetedAssfh=csv.reader(TargetedAss)
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


#Searching in CMB Targeted Therapy Assessment file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("course_assessment.CSV", 'r')
interfh = csv.reader(inter)
TragetedAssDict={}
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
            elif i[col]=="BESTRESP":
                BESTRESP=col
            elif i[col] == "RSDAT_X1_RAW":
                RSDAT_X1 = col
            elif i[col] == "RSDAT_X2_RAW":
                RSDAT_X2 = col
            elif i[col] == "DSTERM_CD":
                DSTERM_CD = col


    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1]>'0125':
            continue
        else:
            hh=[i[RecordId],i[TX_CYCLE_NUM],i[BESTRESP],i[RSDAT_X1],i[RSDAT_X2],i[DSTERM_CD]]
            if i[sub] in TragetedAssDict:
                if hh in TragetedAssDict.get(i[sub]):
                    continue
                else:
                    TragetedAssDict[i[sub]].append(hh)
            else:
                TragetedAssDict[i[sub]]=[]
                TragetedAssDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in TargetedAssfh:
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
            if hhh in TragetedAssDict:
                if len(TragetedAssDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), TragetedAssDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(TragetedAssDict.get(hhh)[0]) + "\n")
                else:
                    for each in TragetedAssDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")




