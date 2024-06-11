import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
bo=open("Bone Marrow.csv",'r')
output=open("5a_BoneMarrow.txt",'w')
bonefh=csv.reader(bo)
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
inter = open("bone_marrow.CSV", 'r')
interfh = csv.reader(inter)
boneDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col]=="LBDAT_RAW":
                LBDAT_RAW=col
            elif i[col] == "LBTIM":
                LBTIM= col
            elif i[col]=="LBORRES_BLSTMBCE":
                LBORRES_BLSTMBCE=col
            elif i[col]=="LBORRES_PROMYCE":
                LBORRES_PROMYCE=col
            elif i[col]=="LBORRES_NEUTMY":
                LBORRES_NEUTMY=col
            elif i[col]=="LBORRES_EOSMYL":
                LBORRES_EOSMYL=col
            elif i[col]=="LBORRES_BASOMYL":
                LBORRES_BASOMYL=col
            elif i[col]=="LBORRES_METAMYCE":
                LBORRES_METAMYCE=col
            elif i[col]=="LBORRES_POLYNE":
                LBORRES_POLYNE=col
            elif i[col]=="LBORRES_POLYEOS":
                LBORRES_POLYEOS=col
            elif i[col]=="LBORRES_POLYBASO":
                LBORRES_POLYBASO=col
            elif i[col]=="LBORRES_LYMCE":
                LBORRES_LYMCE=col
            elif i[col]=="LBORRES_PLSMCECE":
                LBORRES_PLSMCECE=col
            elif i[col]=="LBORRES_MONOCE":
                LBORRES_MONOCE=col
            elif i[col]=="LBORRES_RETI":
                LBORRES_RETI=col
            elif i[col]=="LBORRES_KRCYMGCE":
                LBORRES_KRCYMGCE=col
            elif i[col]=="LBORRES_BLSTRBCE":
                LBORRES_BLSTRBCE=col
            elif i[col]=="LBORRES_BLSTNMCE":
                LBORRES_BLSTNMCE=col
            elif i[col]=="LBORRES_FAB":
                LBORRES_FAB=col

    else:
        dic=i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[RecordId],i[LBDAT_RAW],i[LBTIM],i[LBORRES_BLSTMBCE],i[LBORRES_PROMYCE],i[LBORRES_NEUTMY],i[LBORRES_EOSMYL],i[LBORRES_BASOMYL],i[LBORRES_METAMYCE],i[LBORRES_POLYNE],i[LBORRES_POLYEOS],i[LBORRES_POLYBASO],i[LBORRES_LYMCE],i[LBORRES_PLSMCECE],i[LBORRES_MONOCE],i[LBORRES_RETI],i[LBORRES_KRCYMGCE],i[LBORRES_BLSTRBCE],i[LBORRES_BLSTNMCE],i[LBORRES_FAB]]
            if i[sub] in boneDict:
                if hh in boneDict.get(i[sub]):
                    continue
                else:
                    boneDict[i[sub]].append(hh)
            else:
                boneDict[i[sub]]=[]
                boneDict[i[sub]].append(hh)
#
# for m,n in AMLDict.items():
#     print(m,n)
for con in bonefh:
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
            if hhh in boneDict:
                if len(boneDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), boneDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(boneDict.get(hhh)[0]) + "\n")
                else:
                    for each in boneDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")


