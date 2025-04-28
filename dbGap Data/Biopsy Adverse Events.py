import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
BiopsyAdverse=open("Biopsy Adverse Events.csv",'r')
output=open("Biopsy Adverse Events-output.txt",'w')
BiopsyAdversefh=csv.reader(BiopsyAdverse)
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


#Searching in CMB Biopsy Adverse Events file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("biopsy_adverse_events.CSV", 'r')
interfh = csv.reader(inter)
BaselineMedDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="ASMTTPT_SPEC":
                ASMTTPT_SPEC=col
            elif i[col]=="PRSTDAT":
                PRSTDAT=col
            elif i[col]=="SUPPAE_QVAL_CTCAE":
                SUPPAE_QVAL_CTCAE=col
            elif i[col]=="SUPPAE_QVAL_CTCAECD":
                SUPPAE_QVAL_CTCAECD=col
            elif i[col]=="AE_AESTDAT":
                AE_AESTDAT=col
            elif i[col]=="AE_AEENDAT":
                AE_AEENDAT=col
            elif i[col]=="AERFYN":
                AERFYN=col
            elif i[col]=="AEABTXSC":
                AEABTXSC=col
            elif i[col]=="AE_AESHOSP":
                AE_AESHOSP=col
            elif i[col]=="AE_AESLIFE":
                AE_AESLIFE=col
            elif i[col]=="AE_AESDTH":
                AE_AESDTH=col
            elif i[col]=="AE_AESDISAB":
                AE_AESDISAB=col
            elif i[col]=="AE_AESCONG":
                AE_AESCONG=col
            elif i[col]=="SUPPAE_QVAL_AESINTV":
                SUPPAE_QVAL_AESINTV=col
            elif i[col]=="AE_AESMIE":
                AE_AESMIE=col
            elif i[col]=="AETHPY":
                AETHPY=col

    else:
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[ASMTTPT_SPEC],i[PRSTDAT],i[SUPPAE_QVAL_CTCAE],i[SUPPAE_QVAL_CTCAECD],i[AE_AESTDAT],i[AE_AEENDAT],i[AERFYN],i[AEABTXSC],i[AE_AESHOSP],i[AE_AESLIFE],i[AE_AESDTH],i[AE_AESDISAB],i[AE_AESCONG],i[SUPPAE_QVAL_AESINTV],i[AE_AESMIE],i[AETHPY]]
            if i[sub] in BaselineMedDict:
                if hh in BaselineMedDict.get(i[sub]):
                    continue
                else:
                    BaselineMedDict[i[sub]].append(hh)
            else:
                BaselineMedDict[i[sub]]=[]
                BaselineMedDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in BaselineMedfh:
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
            if hhh in BaselineMedDict:
                if len(BaselineMedDict.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), BaselineMedDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(BaselineMedDict.get(hhh)[0]) + "\n")
                else:
                    for each in BaselineMedDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\n")


