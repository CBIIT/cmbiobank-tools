import os,csv

<<<<<<< Updated upstream
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
=======
os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
entity=open("entity_ids.20211010.csv",'r')
>>>>>>> Stashed changes
baseline=open("Baseline Lesion.csv",'r')
output=open("BaselineLesion-output.txt",'w')
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
                if itemVal ==enrollDic.get(item):
                    continue
                else:
                    print(item, "ErOOoorRrrrrrRRRR public ID present in dictionary")
            else:
                enrollDic[item]=itemVal
#
#
# for m,n in enrollDic.items():
#     print(m,n)


#Searching in CMB Baseline Lesion file to get the data
<<<<<<< Updated upstream
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
lesion = open("baseline_lesion.CSV", 'r')
=======
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
lesion = open("CMB_baseline_lesion.CSV", 'r')
>>>>>>> Stashed changes
lesionfh = csv.reader(lesion)
BaselineDict={}
for i in lesionfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
<<<<<<< Updated upstream
            elif i[col] == "RecordId":
                RecordId = col
            elif i[col]=="TULNKID":
                TULNKID=col
=======
            elif i[col]=="TULNKID":
                nos=col
>>>>>>> Stashed changes
            elif i[col]=="TULOC":
                TULOC=col
            elif i[col] == "TUORRES_DESC":
                TUORRES_DESC = col
            elif i[col] == "TUORRES_PREVIR":
                TUORRES_PREVIR = col
            elif i[col] == "TUTRGNY":
                TUTRGNY = col
            elif i[col] == "TUORRES_FFRIND":
                TUORRES_FFRIND = col
            elif i[col] == "ASMTTPT":
                ASMTTPT = col
<<<<<<< Updated upstream
=======
            elif i[col] == "RecordPosition":
                RecordPosition = col
>>>>>>> Stashed changes
            elif i[col] == "TRDAT":
                TRDAT = col
            elif i[col] == "TRMETHOD":
                TRMETHOD = col
            elif i[col] == "TRORRES_RELDIAM":
                TRORRES_RELDIAM = col
            elif i[col] == "CKBOX_LONG_X":
                CKBOX_LONG_X = col
            elif i[col] == "TRORRES_PERP":
                TRORRES_PERP = col
            elif i[col] == "CKBOX_LONG_Y":
                CKBOX_LONG_Y = col
            elif i[col] == "LSRESP":
                LSRESP = col
            elif i[col] == "RecordActive":
                RecordActive = col
            elif i[col] == "EVAL_LESION":
                EVAL_LESION = col

    else:
<<<<<<< Updated upstream
        vv=i[sub].split("-")
        if i[RecordActive]=="0" or vv[1]>"0125":
            continue
        else:
            hh=[i[RecordId],i[TULNKID],i[TULOC],i[TUORRES_DESC],i[TUORRES_PREVIR],i[TUTRGNY],i[TUORRES_FFRIND],i[ASMTTPT],i[TRDAT],i[TRMETHOD],i[TRORRES_RELDIAM],i[CKBOX_LONG_X],i[TRORRES_PERP],i[CKBOX_LONG_Y],i[LSRESP],i[EVAL_LESION]]
=======
        if i[RecordActive]=="0":
            continue
        else:
            hh=[i[nos],i[RecordPosition],i[TULOC],i[TUORRES_DESC],i[TUORRES_PREVIR],i[TUTRGNY],i[TUORRES_FFRIND],i[ASMTTPT],i[TRDAT],i[TRMETHOD],i[TRORRES_RELDIAM],i[CKBOX_LONG_X],i[TRORRES_PERP],i[CKBOX_LONG_Y],i[LSRESP],i[EVAL_LESION]]
>>>>>>> Stashed changes
            if i[sub] in BaselineDict:
                if hh in BaselineDict.get(i[sub]):
                    continue
                else:
                    BaselineDict[i[sub]].append(hh)
            else:
                BaselineDict[i[sub]]=[]
                BaselineDict[i[sub]].append(hh)
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
            if hhh in BaselineDict:
                if len(BaselineDict.get(hhh))==1:
<<<<<<< Updated upstream
                    # print (t,enrollDic.get(t),BaselineDict.get(hhh))
=======
                    print (t,enrollDic.get(t),BaselineDict.get(hhh))
>>>>>>> Stashed changes
                    output.write(t+"\t"+hhh+"\t"+"\t".join(BaselineDict.get(hhh)[0])+"\n")
                else:
                    for each in BaselineDict.get(hhh):
                        output.write(t + "\t"+hhh+"\t"+ "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")
<<<<<<< Updated upstream
        else:
            output.write(
                t + "\t" + hhh + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")

=======
>>>>>>> Stashed changes



