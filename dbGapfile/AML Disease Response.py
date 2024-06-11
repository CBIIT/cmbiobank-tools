import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
aml=open("AML Disease Response.csv",'r')
output=open("5a_AMLDiseaseResponse.txt",'w')
amlfh=csv.reader(aml)
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


#Searching in disease_response file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("disease_response.CSV", 'r')
interfh = csv.reader(inter)
AMLDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="RSDAT_RAW":
                RSDAT_RAW=col
            elif i[col] == "RSORRES_MORPH":
                RSORRES_MORPH= col
            elif i[col]=="RSORRES_CYTO":
                RSORRES_CYTO=col
            elif i[col]=="RSORRES_MOLE":
                RSORRES_MOLE=col
            elif i[col]=="RSORRES_FLOW":
                RSORRES_FLOW=col
            elif i[col]=="RSORRES_OTH":
                RSORRES_OTH=col

    else:
        dic=i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[RecordId],i[RSDAT_RAW],i[RSORRES_MORPH],i[RSORRES_CYTO],i[RSORRES_MOLE],i[RSORRES_FLOW],i[RSORRES_OTH]]
            if i[sub] in AMLDict:
                if hh in AMLDict.get(i[sub]):
                    continue
                else:
                    AMLDict[i[sub]].append(hh)
            else:
                AMLDict[i[sub]]=[]
                AMLDict[i[sub]].append(hh)
#
# for m,n in AMLDict.items():
#     print(m,n)
for con in amlfh:
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
            if hhh in AMLDict:
                if len(AMLDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), AMLDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(AMLDict.get(hhh)[0]) + "\n")
                else:
                    for each in AMLDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")

#
