import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
offtreat=open("Off Treatment.csv",'r')
output=open("Off Treatment-output.txt",'w')
offtreatfh=csv.reader(offtreat)
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


#Searching in CMB Off Treatment file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("off_treatment.CSV", 'r')
interfh = csv.reader(inter)
offTreatDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="TAC01":
                TAC01=col
            elif i[col] == "DSSTDAT_RAW":
                DSSTDAT = col
            elif i[col] == "DSDECOD":
                DSDECOD = col
            elif i[col] == "DSTERM_OTH":
                DSTERM_OTH = col
            elif i[col] == "BESTRESP":
                BESTRESP = col
            elif i[col] == "RSDAT_X1_RAW":
                RSDAT_X1 = col
            elif i[col] == "RSDAT_X2_RAW":
                RSDAT_X2 = col
            elif i[col] == "DSCONT":
                DSCONT = col
            elif i[col] == "DSCONT_FU":
                DSCONT_FU = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] >"0125":
            continue
        else:
            hh=[i[TAC01],i[DSSTDAT],i[DSDECOD],i[DSTERM_OTH],i[BESTRESP],i[RSDAT_X1],i[RSDAT_X2],i[DSCONT],i[DSCONT_FU]]
            if i[sub] in offTreatDict:
                if hh in offTreatDict.get(i[sub]):
                    continue
                else:
                    offTreatDict[i[sub]].append(hh)
            else:
                offTreatDict[i[sub]]=[]
                offTreatDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in offtreatfh:
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub=cont
    else:
        t=con[sub]
        if t in enrollDic:
            hhh=enrollDic.get(t)
            # print(hhh,type(hhh))
            if hhh in offTreatDict:
                if len(offTreatDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), offTreatDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(offTreatDict.get(hhh)[0]) + "\n")
                else:
                    for each in offTreatDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")

        else:
            output.write(t + "\t" + hhh + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")




