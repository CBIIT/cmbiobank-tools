import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
RadSupp=open("Prior Radiation Supplement.csv",'r')
output=open("Prior Radiation Supplement-output.txt",'w')
RadSuppfh=csv.reader(RadSupp)
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


#Searching in CMB Prior Radiation Supplement file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("prior__radiation_supplement.CSV", 'r')
interfh = csv.reader(inter)
RadSuppDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="PRSTDAT_RAW":
                PRSTDAT=col
            elif i[col]=="PRTRT_RAD":
                PRTRT_RAD=col
            elif i[col] == "PRENDAT_RAW":
                PRENDAT= col
            elif i[col] == "PRLOC":
                PRLOC = col
            elif i[col] == "PRDOSFRQ":
                PRDOSFRQ = col
            elif i[col] == "PRDSTXT":
                PRDSTXT = col
            elif i[col] == "PRDOSU":
                PRDOSU = col
            elif i[col] == "BESTRESP":
                BESTRESP = col
            elif i[col] == "RDTNEXT":
                RDTNEXT = col

    else:
        ss=i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[PRSTDAT],i[PRTRT_RAD],i[PRENDAT],i[PRLOC],i[PRDOSFRQ],i[PRDSTXT],i[PRDOSU],i[BESTRESP],i[RDTNEXT],i[RecordId]]
            if i[sub] in RadSuppDict:
                if hh in RadSuppDict.get(i[sub]):
                    continue
                else:
                    RadSuppDict[i[sub]].append(hh)
            else:
                RadSuppDict[i[sub]]=[]
                RadSuppDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in RadSuppfh:
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
            if hhh in RadSuppDict:
                if len(RadSuppDict.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), RadSuppDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(RadSuppDict.get(hhh)[0]) + "\n")
                else:
                    for each in RadSuppDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")



