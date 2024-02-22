import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
<<<<<<< Updated upstream
entity=open("entity_ids.20211206.csv",'r')
=======
entity=open("entity_ids.20211010.csv",'r')
>>>>>>> Stashed changes
transfusion=open("Transfusion.csv",'r')
output=open("Transfusion-output.txt",'w')
transfusionfh=csv.reader(transfusion)
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


#Searching in CMB Transfusion file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
inter = open("CMB_transfusion.CSV", 'r')
interfh = csv.reader(inter)
transfusionDict={}
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
            elif i[col]=="CMSTDAT":
                CMSTDAT=col
            elif i[col]=="CMSTTIM":
                CMSTTIM=col
            elif i[col] == "CMTRT_TRANSF":
                CMTRT_TRANSF = col
            elif i[col] == "CMDOSTXT_TRANSF":
                CMDOSTXT_TRANSF = col


    else:
        if i[RecordActive]=='0':
            continue
        else:
<<<<<<< Updated upstream
            hh=[i[RecordPosition],i[CMSTDAT],i[CMSTTIM],i[CMTRT_TRANSF],i[CMDOSTXT_TRANSF]]
=======
            hh=[i[CMSTDAT],i[CMSTTIM],i[CMTRT_TRANSF],i[CMDOSTXT_TRANSF]]
>>>>>>> Stashed changes
            if i[sub] in transfusionDict:
                if hh in transfusionDict.get(i[sub]):
                    continue
                else:
                    transfusionDict[i[sub]].append(hh)
            else:
                transfusionDict[i[sub]]=[]
                transfusionDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in transfusionfh:
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
            if hhh in transfusionDict:
                if len(transfusionDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), transfusionDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(transfusionDict.get(hhh)[0]) + "\n")
                else:
                    for each in transfusionDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")


