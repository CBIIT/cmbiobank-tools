import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
deathsumm=open("Death Summary.csv",'r')
output=open("Death Summary-output.txt",'w')
deathsummfh=csv.reader(deathsumm)
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


#Searching in CMB Death Summary file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("death_summary.CSV", 'r')
interfh = csv.reader(inter)
DeathSummary={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="DSSTDAT_RAW":
                DSSTDAT=col
            elif i[col] == "DSAUTPSY":
                DSAUTPSY = col
            elif i[col] == "DDORRES_X1":
                DDORRES_X1 = col
            elif i[col] == "PRCDTH_DDORRES":
                PRCDTH_DDORRES = col
            elif i[col] == "TULOC":
                TULOC = col

    else:
        xx=i[sub].split("-")
        if i[RecordActive]=='0' or xx[1] > '0125':
            continue
        else:
            hh=[i[DSSTDAT],i[DSAUTPSY],i[DDORRES_X1],i[PRCDTH_DDORRES],i[TULOC]]
            if i[sub] in DeathSummary:
                if hh in DeathSummary.get(i[sub]):
                    continue
                else:
                    DeathSummary[i[sub]].append(hh)
            else:
                DeathSummary[i[sub]]=[]
                DeathSummary[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in deathsummfh:
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
            if hhh in DeathSummary:
                if len(DeathSummary.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), DeathSummary.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(DeathSummary.get(hhh)[0]) + "\n")
                else:
                    for each in DeathSummary.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")

        else:
            output.write(t + "\t" + hhh + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")


