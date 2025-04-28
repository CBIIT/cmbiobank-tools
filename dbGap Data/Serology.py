import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
<<<<<<< Updated upstream
entity=open("entity_ids.20211206.csv",'r')
=======
entity=open("entity_ids.20211010.csv",'r')
>>>>>>> Stashed changes
serology=open("Serology.csv",'r')
output=open("Serology-output.txt",'w')
serologyfh=csv.reader(serology)
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


#Searching in CMB Serology file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
inter = open("CMB_serology.CSV", 'r')
interfh = csv.reader(inter)
serologyDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
<<<<<<< Updated upstream
            elif i[col]=="RecordPosition":
                RecordPosition=col
=======
>>>>>>> Stashed changes
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="LBTEST_SER":
                LBTEST_SER=col
            elif i[col]=="LBSPEC":
                LBSPEC=col
            elif i[col] == "LBDAT":
                LBDAT = col
            elif i[col] == "LBTIM":
                LBTIM = col
            elif i[col] == "LBORRES":
                LBORRES = col


    else:
        if i[RecordActive]=='0':
            continue
        else:
<<<<<<< Updated upstream
            hh=[i[RecordPosition],i[LBTEST_SER],i[LBSPEC],i[LBDAT],i[LBTIM],i[LBORRES]]
=======
            hh=[i[LBTEST_SER],i[LBSPEC],i[LBDAT],i[LBTIM],i[LBORRES]]
>>>>>>> Stashed changes
            if i[sub] in serologyDict:
                if hh in serologyDict.get(i[sub]):
                    continue
                else:
                    serologyDict[i[sub]].append(hh)
            else:
                serologyDict[i[sub]]=[]
                serologyDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in serologyfh:
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
            if hhh in serologyDict:
                if len(serologyDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), serologyDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(serologyDict.get(hhh)[0]) + "\n")
                else:
                    for each in serologyDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")


