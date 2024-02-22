import os,csv

<<<<<<< Updated upstream
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
=======
os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
entity=open("entity_ids.20211010.csv",'r')
>>>>>>> Stashed changes
offstudy=open("Off Study.csv",'r')
output=open("Off Study-output.txt",'w')
offstudyfh=csv.reader(offstudy)
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


#Searching in CMB Off Study file to get the data
<<<<<<< Updated upstream
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("off_study.CSV", 'r')
=======
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
inter = open("CMB_off_study.CSV", 'r')
>>>>>>> Stashed changes
interfh = csv.reader(inter)
offstudyDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
<<<<<<< Updated upstream
            elif i[col]=="DSSTDAT_RAW":
=======
            elif i[col]=="DSSTDAT":
>>>>>>> Stashed changes
                DSSTDAT=col
            elif i[col] == "DSDECOD_OS":
                DSDECOD_OS = col
            elif i[col] == "DSTERM_OTH_OS":
                DSTERM_OTH_OS = col
            elif i[col] == "BESTRESP":
                BESTRESP = col
            elif i[col] == "RSDAT_X1":
                RSDAT_X1 = col
            elif i[col] == "RSDAT_X2":
                RSDAT_X2 = col
            elif i[col] == "STORCNSTNY":
                STORCNSTNY = col
            elif i[col] == "MRCNSTNY":
                MRCNSTNY = col

    else:
<<<<<<< Updated upstream
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] >"0125":
=======
        if i[RecordActive]=='0':
>>>>>>> Stashed changes
            continue
        else:
            hh=[i[DSSTDAT],i[DSDECOD_OS],i[DSTERM_OTH_OS],i[BESTRESP],i[RSDAT_X1],i[RSDAT_X2],i[STORCNSTNY],i[MRCNSTNY]]
            if i[sub] in offstudyDict:
                if hh in offstudyDict.get(i[sub]):
                    continue
                else:
                    offstudyDict[i[sub]].append(hh)
            else:
                offstudyDict[i[sub]]=[]
                offstudyDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in offstudyfh:
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
            if hhh in offstudyDict:
                if len(offstudyDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), offstudyDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(offstudyDict.get(hhh)[0]) + "\n")
                else:
                    for each in offstudyDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")
<<<<<<< Updated upstream
        else:
            output.write(t + "\t" + hhh + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")


=======
>>>>>>> Stashed changes


