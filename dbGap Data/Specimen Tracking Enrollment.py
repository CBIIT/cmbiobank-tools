import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/RAVE")
entity=open("entity_ids.20230227.csv",'r')
specimentrac=open("6a_Specimen Tracking Enrollment.csv",'r')
output=open("6a_Specimen Tracking Enrollment-output.txt",'w')
specimentrackfh=csv.reader(specimentrac)
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
inter = open("specimen_tracking_enrollment.CSV", 'r')
interfh = csv.reader(inter)
SpecimenTrack={}
for i in interfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="SPECID_DRV":
                SPECID_DRV=col
            elif i[col] == "DXGRP":
                DXGRP = col
            elif i[col] == "SNOMED_X2":
                SNOMED_X2 = col
            elif i[col] == "ASMTTPT":
                ASMTTPT = col
            elif i[col] == "SPECCAT":
                SPECCAT = col
            elif i[col] == "BESPEC_DSL":
                BESPEC_DSL = col
            elif i[col] == "BEREFID":
                BEREFID = col
            elif i[col] == "TISTYP":
                TISTYP = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] >"0125":
            continue
        else:
            tal=i[sub]+"_"+i[SPECID_DRV]
            hh=[i[DXGRP],i[SNOMED_X2],i[ASMTTPT],i[SPECCAT],i[BESPEC_DSL],i[BEREFID],i[TISTYP]]
            if tal in SpecimenTrack:
                if hh in SpecimenTrack.get(tal):
                    continue
                else:
                    SpecimenTrack[tal].append(hh)
            else:
                SpecimenTrack[tal]=[]
                SpecimenTrack[tal].append(hh)
#
# for m,n in DeathSummary.items():
#     print(m,n)
for con in specimentrackfh:
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub1=cont
            elif "SAMPLE_ID" in con[cont]:
                samp=cont
    else:
        t=con[sub1]+"_"+con[samp]
        if t in enrollDic:
            hhh=enrollDic.get(t)
            # print(hhh,type(hhh))
            if hhh in SpecimenTrack:
                if len(SpecimenTrack.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), DeathSummary.get(hhh),           'pppp')
                    output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "\t".join(SpecimenTrack.get(hhh)[0]) + "\n")
                else:
                    for each in SpecimenTrack.get(hhh):
                        output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "\t".join(each) + "\n")
            else:
                output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "-"+"\t" + "-"+"\t" + "-"+"\t" + "-"+ "\n")


