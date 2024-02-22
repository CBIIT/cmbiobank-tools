import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
hematology=open("Hematology DS.csv",'r')
output=open("Hematology-output.txt",'w')
hematologyfh=csv.reader(hematology)
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


#Searching in CMB Hematology file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("hematology.CSV", 'r')
interfh = csv.reader(inter)
hematologyDict={}
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
                LBDAT=col
            elif i[col] == "LBTIM":
                LBTIM = col
            elif i[col] == "LB_LBORRES_HGB":
                LB_LBORRES_HGB = col
            elif i[col] == "LB_LBORRES_HCT":
                LB_LBORRES_HCT = col
            elif i[col] == "LB_LBORRES_WBC":
                LB_LBORRES_WBC = col
            elif i[col] == "LBORRES_NEUTLE":
                LBORRES_NEUTLE = col
            elif i[col] == "LBORRES_LYMLE":
                LBORRES_LYMLE = col
            elif i[col] == "LBORRES_BASOLE":
                LBORRES_BASOLE = col
            elif i[col] == "LBORRES_MONOLE":
                LBORRES_MONOLE = col
            elif i[col] == "LBORRES_EOSLE":
                LBORRES_EOSLE = col
            elif i[col] == "LBORRES_NEUTBNE":
                LBORRES_NEUTBNE = col
            elif i[col] == "LBORRES_BLASTLE":
                LBORRES_BLASTLE = col
            elif i[col] == "LB_LBORRES_PLAT":
                LB_LBORRES_PLAT = col
            elif i[col] == "LB_LBORRES_NEUT":
                LB_LBORRES_NEUT = col
            elif i[col] == "LBORRES_LYMATLE":
                LBORRES_LYMATLE = col
            elif i[col] == "LB_LBORRES_RBC":
                LB_LBORRES_RBC = col
            elif i[col] == "LBORRES_RETIRBC":
                LBORRES_RETIRBC = col
            elif i[col] == "LB_LBORRES_ESR":
                LB_LBORRES_ESR = col
            elif i[col] == "LB_LBORRES_PT":
                LB_LBORRES_PT = col
            elif i[col] == "LBORRES_APTT":
                LBORRES_APTT = col
            elif i[col] == "LB_LBORRES_INR":
                LB_LBORRES_INR = col
            elif i[col] == "LB_LBORRES_LYM":
                LB_LBORRES_LYM = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1]>'0125':
            continue
        else:
            hh=[i[RecordId],i[LBDAT],i[LBTIM],i[LB_LBORRES_HGB],i[LB_LBORRES_HCT],i[LB_LBORRES_WBC],i[LBORRES_NEUTLE],i[LBORRES_LYMLE],i[LBORRES_BASOLE],i[LBORRES_MONOLE],i[LBORRES_EOSLE],i[LBORRES_NEUTBNE],i[LBORRES_BLASTLE],i[LB_LBORRES_PLAT],i[LB_LBORRES_NEUT],i[LBORRES_LYMATLE],i[LB_LBORRES_RBC],i[LBORRES_RETIRBC],i[LB_LBORRES_ESR],i[LB_LBORRES_PT],i[LBORRES_APTT],i[LB_LBORRES_INR],i[LB_LBORRES_LYM]]
            if i[sub] in hematologyDict:
                if hh in hematologyDict.get(i[sub]):
                    continue
                else:
                    hematologyDict[i[sub]].append(hh)
            else:
                hematologyDict[i[sub]]=[]
                hematologyDict[i[sub]].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in hematologyfh:
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
            if hhh in hematologyDict:
                if len(hematologyDict.get(hhh)) == 1:
                    print (t, enrollDic.get(t), hematologyDict.get(hhh),           'pppp')
                    output.write(t + "\t" + hhh + "\t" + "\t".join(hematologyDict.get(hhh)[0]) + "\n")
                else:
                    for each in hematologyDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t"+ "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t"+ "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t"+ "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t"  +"\n")
        else:
            output.write(t + "\t" + hhh + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "\n")




