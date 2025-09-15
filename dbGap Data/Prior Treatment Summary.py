import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
entity=open("entity_ids.20211206.csv",'r')
TreatmentSupp=open("Prior Treatment Summary.csv",'r')
output=open("Prior Treatment Summary-output.txt",'w')
TreatmentSuppfh=csv.reader(TreatmentSupp)
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


#Searching in CMB Prior Treatment Summary file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
inter = open("CMB_prior__treatment_summary.CSV", 'r')
interfh = csv.reader(inter)
TreatmentSuppDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordPosition":
                RecordPosition=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="CMTRT_PRIORTRT":
                CMTRT_PRIORTRT=col
            elif i[col]=="CMOCCUR":
                CMOCCUR=col
            elif i[col] == "CMENDAT":
                CMENDAT= col


    else:
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[RecordPosition],i[CMTRT_PRIORTRT],i[CMOCCUR],i[CMENDAT]]
            if i[sub] in TreatmentSuppDict:
                if hh in TreatmentSuppDict.get(i[sub]):
                    continue
                else:
                    TreatmentSuppDict[i[sub]].append(hh)
            else:
                TreatmentSuppDict[i[sub]]=[]
                TreatmentSuppDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in TreatmentSuppfh:
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
            if hhh in TreatmentSuppDict:
                if len(TreatmentSuppDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), TreatmentSuppDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(TreatmentSuppDict.get(hhh)[0]) + "\n")
                else:
                    for each in TreatmentSuppDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")


