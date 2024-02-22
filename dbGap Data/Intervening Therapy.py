import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
entity=open("entity_ids.20211206.csv",'r')
baseline=open("Intervening Therapy.csv",'r')
output=open("Intervening Therapy-output.txt",'w')
baselinefh=csv.reader(baseline)
entityfh=csv.reader(entity)
enrollDic={}

for x in entityfh:
    # print(x)
    if x[0]=="NA":
        continue
    else:
        if "ctep_id" in x[0]:
            for val in range(0,len(x)):
                print(x[val])
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


#Searching in CMB Intervening Therapy file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
inter = open("CMB_intervening_therapy.CSV", 'r')
interfh = csv.reader(inter)
BaselineDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="CMCAT":
                CMCAT=col
            elif i[col] == "CMSTDAT":
                CMSTDAT = col
            elif i[col] == "CMTRT":
                CMTRT = col
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
            elif i[col] == "RecordPosition":
                RecordPosition = col
            elif i[col] == "CMDOSU":
                CMDOSU = col
            elif i[col] == "BESTRESP":
                BESTRESP = col

    else:
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[RecordPosition],i[CMCAT],i[CMSTDAT],i[CMTRT],i[CMENDAT],i[RGMENDAT],i[CMDOSFRQ],i[CMDOSRGM],i[CMDSTXT],i[CMDOSU],i[BESTRESP]]
            if i[sub] in BaselineDict:
                if hh in BaselineDict.get(i[sub]):
                    continue
                else:
                    BaselineDict[i[sub]].append(hh)
            else:
                BaselineDict[i[sub]]=[]
                BaselineDict[i[sub]].append(hh)

for m,n in BaselineDict.items():
    print(m,n)
for con in baselinefh:
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub=cont
    else:
        t=con[sub]
        if t in enrollDic:
            hhh=enrollDic.get(t)
            print(hhh,type(hhh))
            if hhh in BaselineDict:
                if len(BaselineDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), BaselineDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(BaselineDict.get(hhh)[0]) + "\n")
                else:
                    for each in BaselineDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")


