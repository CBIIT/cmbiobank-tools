import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
entity=open("entity_ids.20231204.csv",'r')
TherapySupp=open("Prior Therapy Supplement.csv",'r')
output=open("Prior Therapy Supplement-output.txt",'w')
TherapySuppfh=csv.reader(TherapySupp)
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


#Searching in CMB Prior Therapy Supplement file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
inter = open("CMB_prior__therapy_supplement.CSV", 'r')
interfh = csv.reader(inter)
TherapySuppDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordPosition":
                RecordPosition=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="CMCAT":
                CMCAT=col
            elif i[col]=="CMSTDAT":
                CMSTDAT=col
            elif i[col] == "CMTRT":
                CMTRT= col
            elif i[col] == "CMENDAT":
                CMENDAT = col
            elif i[col] == "RGMENDAT":
                RGMENDAT = col
            elif i[col] == "CMDOSFRQ":
                CMDOSFRQ = col
            elif i[col] == "CMDOSRGM":
                CMDOSRGM = col
            elif i[col] == "CMDSTXT":
                CMDSTXT = col
            elif i[col] == "CMDOSU":
                CMDOSU = col
            elif i[col] == "BESTRESP":
                BESTRESP = col
            elif i[col] == "PRPCRGN":
                PRPCRGN = col

    else:
        if i[RecordActive]=='0' and i[RecordPosition]=='0':
            continue
        else:
            hh=[i[CMCAT],i[CMSTDAT],i[CMTRT],i[CMENDAT],i[RGMENDAT],i[CMDOSFRQ],i[CMDOSRGM],i[CMDSTXT],i[CMDOSU],i[BESTRESP],i[RecordPosition],i[PRPCRGN]]
            if i[sub] in TherapySuppDict:
                if hh in TherapySuppDict.get(i[sub]):
                    continue
                else:
                    TherapySuppDict[i[sub]].append(hh)
            else:
                TherapySuppDict[i[sub]]=[]
                TherapySuppDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in TherapySuppfh:
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
            if hhh in TherapySuppDict:
                if len(TherapySuppDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), TherapySuppDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(TherapySuppDict.get(hhh)[0]) + "\n")
                else:
                    for each in TherapySuppDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")


