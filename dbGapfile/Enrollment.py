import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
enrollment=open("Enrollment DS.csv",'r')
output=open("Enrollment-output.txt",'w')
enrollfh=csv.reader(enrollment)
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


#Searching in CMB Enrollment file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("enrollment.CSV", 'r')
interfh = csv.reader(inter)
EnrollmentDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="SEX":
                SEX=col
            elif i[col]=="GENDER":
                GENDER=col
            elif i[col] == "RACE":
                RACE= col
            elif i[col]=="ETHNIC":
                ETHNIC=col
            elif i[col]=="BRTHDAT_RAW":
                BRTHDAT=col
            elif i[col]=="AGE":
                AGE=col
            elif i[col]=="WEIGHT_VSORRES":
                WEIGHT_VSORRES=col
            elif i[col]=="WEIGHT_VSORRES_UN":
                WEIGHT_units=col
            elif i[col]=="HEIGHT_VSORRES_UN":
                HEIGHT_units=col
            elif i[col]=="HEIGHT_VSORRES":
                HEIGHT_VSORRES=col
            elif i[col]=="BSA_VSORRES":
                BSA_VSORRES=col
            elif i[col]=="MHDSXCD":
                MHDSXCD=col
            elif i[col]=="CTEP_SDC_MED_V10_CD":
                CTEP_SDC_MED_V10_CD=col
            elif i[col]=="MHLOC":
                MHLOC=col
            elif i[col]=="CPRFSTAT":
                CPRFSTAT=col
            elif i[col]=="ICPAPYN":
                ICPAPYN=col
            elif i[col]=="DSSTDAT_IC_RAW":
                DSSTDAT_IC=col


    else:
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[SEX],i[GENDER],i[RACE]," ",i[ETHNIC],i[BRTHDAT],i[AGE],i[WEIGHT_VSORRES],i[WEIGHT_units],i[HEIGHT_VSORRES],i[HEIGHT_units],i[BSA_VSORRES],i[MHDSXCD],i[CTEP_SDC_MED_V10_CD],i[MHLOC],i[CPRFSTAT],i[DSSTDAT_IC],i[ICPAPYN]]
            if i[sub] in EnrollmentDict:
                if hh in EnrollmentDict.get(i[sub]):
                    continue
                else:
                    EnrollmentDict[i[sub]].append(hh)
            else:
                EnrollmentDict[i[sub]]=[]
                EnrollmentDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in enrollfh:
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
            if hhh in EnrollmentDict:
                if len(EnrollmentDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), EnrollmentDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(EnrollmentDict.get(hhh)[0]) + "\n")
                else:
                    for each in EnrollmentDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")
        else:
            output.write(t + "\t" + hhh + "\n")




