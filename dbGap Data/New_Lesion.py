import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
newLesion=open("New Lesion.csv",'r')
output=open("New Lesion-output.txt",'w')
newLesionfh=csv.reader(newLesion)
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


#Searching in CMB New Lesion file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("new_lesion.CSV", 'r')
interfh = csv.reader(inter)
NewLesionDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col] == "RecordId":
                RecordId = col
            elif i[col] == "TULNKID":
                TULNKID = col
            elif i[col] == "TULOC":
                TULOC = col
            elif i[col] == "TUORRES_DESC":
                TUORRES_DESC = col
            elif i[col] == "TUORRES_FFRIND":
                TUORRES_FFRIND = col
            elif i[col] == "ASMTTPT":
                ASMTTPT = col
            elif i[col] == "TRDAT":
                TRDAT = col
            elif i[col] == "TRMETHOD":
                TRMETHOD = col
            elif i[col] == "TRORRES_X":
                TRORRES_X = col
            elif i[col] == "CKBOX_LONG_X":
                CKBOX_LONG_X = col
            elif i[col] == "TRORRES_Y":
                TRORRES_Y = col
            elif i[col] == "CKBOX_LONG_Y":
                CKBOX_LONG_Y = col
            elif i[col] == "LSRESP_NEW":
                LSRESP_NEW = col
            elif i[col] == "EVAL_LESION":
                EVAL_LESION = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] >'0125':
            continue
        else:
            hh=[i[RecordId],i[TULNKID],i[TULOC],i[TUORRES_DESC],i[TUORRES_FFRIND],i[ASMTTPT],i[TRDAT],i[TRMETHOD],i[TRORRES_X],i[CKBOX_LONG_X],i[TRORRES_Y],i[CKBOX_LONG_Y],i[LSRESP_NEW],i[EVAL_LESION]]
            if i[sub] in NewLesionDict:
                if hh in NewLesionDict.get(i[sub]):
                    continue
                else:
                    NewLesionDict[i[sub]].append(hh)
            else:
                NewLesionDict[i[sub]]=[]
                NewLesionDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in newLesionfh:
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
            if hhh in NewLesionDict:
                if len(NewLesionDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), NewLesionDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(NewLesionDict.get(hhh)[0]) + "\n")
                else:
                    for each in NewLesionDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t"+ "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")


