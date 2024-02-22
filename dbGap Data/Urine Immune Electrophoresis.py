<<<<<<< Updated upstream
import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
urine=open("Urine Immune Electrophoresis.csv",'r')
output=open("Urine Immune Electrophoresis-output.txt",'w')
urinefh=csv.reader(urine)
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


#Searching in CMB Urine Immune Electrophoresis file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("urine_immune_electrophoresis.CSV", 'r')
interfh = csv.reader(inter)
urineDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="LBDAT_RAW":
                LBDAT=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="LBTIM":
                LBTIM=col
            elif i[col]=="LBORRES_IGA":
                LBORRES_IGA=col
            elif i[col] == "LBORRES_IGD":
                LBORRES_IGD = col
            elif i[col] == "LBORRES_IGE":
                LBORRES_IGE = col
            elif i[col] == "LBORRES_IGG":
                LBORRES_IGG = col
            elif i[col]=="LBORRES_IGM":
                LBORRES_IGM=col
            elif i[col] == "LBORRES_MCPROT":
                LBORRES_MCPROT = col
            elif i[col] == "LBORRES_PCPROT":
                LBORRES_PCPROT = col
            elif i[col] == "LBORRES_KAPPALC":
                LBORRES_KAPPALC = col
            elif i[col] == "LBORRES_LMBDLC":
                LBORRES_LMBDLC = col
            elif i[col] == "LBORRES_BJPROT":
                LBORRES_BJPROT = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] > "0125":
            continue
        else:
            hh=[i[LBDAT],i[LBTIM],i[LBORRES_IGA],i[LBORRES_IGD],i[LBORRES_IGE],i[LBORRES_IGG],i[LBORRES_IGM],i[LBORRES_MCPROT],i[LBORRES_PCPROT],i[LBORRES_KAPPALC],i[LBORRES_LMBDLC],i[LBORRES_BJPROT]]
            if i[sub] in urineDict:
                if hh in urineDict.get(i[sub]):
                    continue
                else:
                    urineDict[i[sub]].append(hh)
            else:
                urineDict[i[sub]]=[]
                urineDict[i[sub]].append(hh)
#
# for m,n in urineDict.items():
#     print(m,n)
for con in urinefh:
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        for cont in range(0, len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub = cont
    else:
        t = con[sub]
        if t in enrollDic:
            hhh = enrollDic.get(t)
            if hhh in urineDict:
                if len(urineDict.get(hhh)) == 1:
                    # print (t,enrollDic.get(t),urineDict.get(hhh))
                    output.write(t + "\t" + hhh + "\t" + "\t".join(urineDict.get(hhh)[0]) + "\n")
                else:
                    for each in urineDict.get(hhh):
                        output.write(t + "\t" + hhh + "\t" + "\t".join(each) + "\n")
            else:
                output.write(t + "\t" + hhh + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")
        else:
            output.write(t + "\t" + hhh + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")


=======
####### NO Data in the columns selected so the code is not written but check the CMB Rave file for this file ##########
>>>>>>> Stashed changes
