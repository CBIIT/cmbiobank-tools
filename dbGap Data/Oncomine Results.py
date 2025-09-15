import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
oncoresult=open("6a_Oncomine Results.csv",'r')
output=open("6a_Oncomine Results-output.txt",'w')
oncoresultfh=csv.reader(oncoresult)
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
                elif "pub_spec_id" in x[val]:
                    pub_spec_id=val
                elif "rave_spec_id" in x[val]:
                    rave_spec_id=val


        else:
            item=x[pubID]+"_"+x[pub_spec_id]
            itemVal=x[ID]+"_"+x[rave_spec_id]
            # print(itemVal,item)
            if item in enrollDic:
                if itemVal == enrollDic.get(item):
                    continue
                else:
                    print("ERRRRROORRRRRRRRRR present in dictonary", item,itemVal)
            else:
                enrollDic[item]=itemVal
                # print(item,itemVal)


#Searching in CMB_specimen_tracking_enrollment file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
inter = open("oncomine_result.CSV", 'r')
interfh = csv.reader(inter)
spec=open("specimen_transmittal.CSV",'r')
specfh=csv.reader(spec)
SpecimenTrack={}

####Opening Specimen tranmittal file to get the SPECID
SpecTrans={}
for j in specfh:
    if j[0].startswith("projectid"):
        for kal in range(0,len(j)):
            if j[kal]=="Subject":
                subject=kal
            elif j[kal]=="InstanceName":
                instancename=kal
            elif j[kal]=="SPECID":
                specid=kal

    else:
        Sub_In=j[subject]+"_"+j[instancename]
        if Sub_In in SpecTrans:
            if j[specid] == SpecTrans.get(Sub_In):
                continue
            else:
                print("ERORRRRRRRRRRR value present")
        else:
            SpecTrans[Sub_In]=j[specid]
AddDict={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="PFORRES_SPD":
                PFORRES_SPD=col
            elif i[col] == "PFRESRS":
                PFRESRS = col
            elif i[col] == "PFUPLDAT_RAW":
                PFUPLDAT = col
            elif i[col] == "InstanceName":
                InstanceName = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] > "0125":
            continue
        else:
            oo=[i[PFORRES_SPD],i[PFRESRS],i[PFUPLDAT]]
            oncojoin=i[sub]+"_"+i[InstanceName]
            # print(oncojoin,"NOOOOOOOO")
            if oncojoin in SpecTrans:
                temp=i[sub]+"_"+SpecTrans.get(oncojoin)
                if temp in AddDict:
                    print ("Subject, Specimen ID already present")
                else:
                    # print("JJJJJJJJJ",temp)
                    AddDict[temp]=[i[PFORRES_SPD],i[PFRESRS],i[PFUPLDAT]]

#
# for m,n in AddDict.items():
#     print(m,n,"YESSSS")

for con in oncoresultfh:
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub=cont
            elif "SAMPLE_ID" in con[cont]:
                samp=cont
    else:
        t=con[sub]+"_"+con[samp]
        if t in enrollDic:
            hhh=enrollDic.get(t)
            # print(hhh,type(hhh))
            if hhh in AddDict:
                    output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" +"\t".join(AddDict.get(hhh)) + "\n")
            else:
                output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "-"+"\t" + "-"+"\t" + "-" + "\n")


