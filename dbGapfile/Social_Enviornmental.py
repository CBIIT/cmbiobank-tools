import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
socio=open("Social & Environmental Factors.csv",'r')
output=open("5a_SocialAndEnvironmentalFactors.txt",'w')
sociofh=csv.reader(socio)
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


#Searching in CMB Social and Environmental Factors  file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
Envio = open("social_and_environmental_factors.CSV", 'r')
Enviofh = csv.reader(Envio)
SocialDict={}
for i in Enviofh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="SMOKING_SUNCF":
                SMOKING_SUNCF=col
            elif i[col]=="SMOKE_SUSTAGE":
                SMOKE_SUSTAGE=col
            elif i[col] == "SMOKE_SUENAGE":
                SMOKE_SUENAGE = col
            elif i[col] == "SMOK_PK_YR_NUM":
                SMOK_PK_YR_NUM = col
            elif i[col] == "SMOKE_SUDOSE":
                SMOKE_SUDOSE = col
            elif i[col] == "SMOKE_SUDUR":
                SMOKE_SUDUR = col
            elif i[col] == "SECHAND_SUOCCUR":
                SECHAND_SUOCCUR = col
            elif i[col] == "SU_SUSCAT_SPD_SECHAND":
                SU_SUSCAT_SPD_SECHAND = col
            elif i[col] == "ALCOHOL_SUNCF":
                ALCOHOL_SUNCF = col
            elif i[col] == "ALCOHOL_SUDUR":
                ALCOHOL_SUDUR = col
            elif i[col] == "EROCCUR":
                EROCCUR = col
            elif i[col] == "EMPJOB_SCORRES":
                EMPJOB_SCORRES = col
            elif i[col] == "INCMLVL_SCORRES":
                INCMLVL_SCORRES = col
            elif i[col] == "ERTERM01":
                ERTERM01 = col
            elif i[col] == "ERTERM02":
                ERTERM02 = col
            elif i[col] == "ERTERM03":
                ERTERM03 = col
            elif i[col] == "ERTERM04":
                ERTERM04 = col
            elif i[col] == "ERTERM05":
                ERTERM05 = col
            elif i[col] == "RecordActive":
                RecordActive = col
            elif i[col] == "EDULVL_SCORRES":
                EDULVL_SCORRES = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[SMOKING_SUNCF],i[SMOKE_SUSTAGE],i[SMOKE_SUENAGE],i[SMOK_PK_YR_NUM],i[SMOKE_SUDOSE],i[SMOKE_SUDUR],i[SECHAND_SUOCCUR],i[SU_SUSCAT_SPD_SECHAND],i[ALCOHOL_SUNCF],i[ALCOHOL_SUDUR],i[EROCCUR],i[ERTERM01],i[ERTERM02],i[ERTERM03],i[ERTERM04],i[ERTERM05],i[EMPJOB_SCORRES],i[INCMLVL_SCORRES],i[EDULVL_SCORRES]]
            if i[sub] in SocialDict:
                if hh in SocialDict.get(i[sub]):
                    continue
                else:
                    SocialDict[i[sub]].append(hh)
            else:
                SocialDict[i[sub]]=[]
                SocialDict[i[sub]].append(hh)

# for m,n in SocialDict.items():
#     print(m,n)
for con in sociofh:
    # print(con)
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        # print("HEEYYYYY")
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub=cont
    else:
        t=con[sub]
        if t in enrollDic:
            hhh=enrollDic.get(t)
            # print(hhh,type(hhh))
            if hhh in SocialDict:
                if len(SocialDict.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), SocialDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(SocialDict.get(hhh)[0]) + "\n")
                else:
                    for each in SocialDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")
        else:
            output.write(t + "\t" + hhh + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")



