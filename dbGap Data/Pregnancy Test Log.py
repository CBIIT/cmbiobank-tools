import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
pregnancyTest=open("Pregnancy Test Log.csv",'r')
output=open("Pregnancy Test Log-output.txt",'w')
pregnancyTestfh=csv.reader(pregnancyTest)
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


#Searching in CMB Pregnancy Test Log file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("pregnancy_test_log.csv", 'r')
interfh = csv.reader(inter)
PregTestDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="LBTEST_PREG":
                LBTEST_PREG=col
            elif i[col]=="ASMTTPT":
                ASMTTPT=col
            elif i[col] == "LBSPEC":
                LBSPEC = col
            elif i[col] == "LBDAT_RAW":
                LBDAT = col
            elif i[col] == "LBTIM":
                LBTIM = col
            elif i[col] == "LBORRES_X1":
                LBORRES_X1 = col
            elif i[col] == "LBORRESU":
                LBORRESU = col
            elif i[col] == "LBORNRLO":
                LBORNRLO = col
            elif i[col] == "LBORNRHI":
                LBORNRHI = col


    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1]> "0125":
            continue
        else:
            hh=[i[RecordId],i[LBTEST_PREG],i[ASMTTPT],i[LBSPEC],i[LBDAT],i[LBTIM],i[LBORRES_X1],i[LBORRESU],i[LBORNRLO],i[LBORNRHI]]
            if i[sub] in PregTestDict:
                if hh in PregTestDict.get(i[sub]):
                    continue
                else:
                    PregTestDict[i[sub]].append(hh)
            else:
                PregTestDict[i[sub]]=[]
                PregTestDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in pregnancyTestfh:
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
            if hhh in PregTestDict:
                if len(PregTestDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), PregTestDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(PregTestDict.get(hhh)[0]) + "\n")
                else:
                    for each in PregTestDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")



