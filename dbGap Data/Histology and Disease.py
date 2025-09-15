import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
histologyD=open("Histology and Disease.csv",'r')
output=open("Histology and Disease-output.txt",'w')
histologyfh=csv.reader(histologyD)
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


#Searching in CMB Histology and Disease file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("histology_and_disease.CSV", 'r')
interfh = csv.reader(inter)
HistologyDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="RSORRES_DZSTAGE":
                RSORRES_DZSTAGE=col
            elif i[col] == "MIORRES_X1":
                MIORRES_X1= col
            elif i[col]=="SNOMED":
                SNOMED=col
            elif i[col]=="MIORRES_X2":
                MIORRES_X2=col
            elif i[col]=="HISTSUBT":
                HISTSUBT=col
            elif i[col]=="MHSTDAT_DX_RAW":
                MHSTDAT_DX=col
            elif i[col]=="MHSTDAT_CONFIRM_RAW":
                MHSTDAT_CONFIRM=col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] >'0125':
            continue
        else:
            hh=[i[RecordId],i[RSORRES_DZSTAGE],i[MIORRES_X1],i[SNOMED],i[MIORRES_X2],i[HISTSUBT],i[MHSTDAT_DX],i[MHSTDAT_CONFIRM]]
            if i[sub] in HistologyDict:
                if hh in HistologyDict.get(i[sub]):
                    continue
                else:
                    HistologyDict[i[sub]].append(hh)
            else:
                HistologyDict[i[sub]]=[]
                HistologyDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in histologyfh:
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
            if hhh in HistologyDict:
                if len(HistologyDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), HistologyDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(HistologyDict.get(hhh)[0]) + "\n")
                else:
                    for each in HistologyDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")



