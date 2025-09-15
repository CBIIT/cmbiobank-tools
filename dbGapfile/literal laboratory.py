import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
lil=open("literal_laboratory temp.csv",'r')
output=open("5a_LiteralLaboratory.txt",'w')
lilfh=csv.reader(lil)
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


#Searching in literal_laboratory file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("literal_laboratory.CSV", 'r')
interfh = csv.reader(inter)
lilLabDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="LBTPT_LL":
                LBTPT_LL=col
            elif i[col] == "LBDAT_RAW":
                LBDAT_RAW= col
            elif i[col]=="LBTIM":
                LBTIM=col
            elif i[col]=="LBTEST_LITERAL":
                LBTEST_LITERAL=col
            elif i[col]=="LBANTREG":
                LBANTREG=col
            elif i[col]=="LBNRIND":
                LBNRIND=col
            elif i[col]=="LBORRES_UNL":
                LBORRES_UNL=col
            elif i[col]=="RPTXFN":
                RPTXFN=col

    else:
        dic=i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[RecordId],i[LBTPT_LL],i[LBDAT_RAW],i[LBTIM],i[LBTEST_LITERAL],i[LBANTREG],i[LBNRIND],i[LBORRES_UNL],i[RPTXFN]]
            if i[sub] in lilLabDict:
                if hh in lilLabDict.get(i[sub]):
                    continue
                else:
                    lilLabDict[i[sub]].append(hh)
            else:
                lilLabDict[i[sub]]=[]
                lilLabDict[i[sub]].append(hh)
#
# for m,n in AMLDict.items():
#     print(m,n)
for con in lilfh:
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
            if hhh in lilLabDict:
                if len(lilLabDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), lilLabDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(lilLabDict.get(hhh)[0]) + "\n")
                else:
                    for each in lilLabDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")

#
