import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
specimentrans=open("specimentransmittal_Subspecimen.csv",'r')
output=open("6a_Specimen Transmittal-output.txt",'w')
specimentransfh=csv.reader(specimentrans)
entityfh=csv.reader(entity)
enrollDic={}

for x in entityfh:
    # print(x)
    if x[5]=="":
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
                elif "pub_subspec_id" in x[val]:
                    pub_subspec_id=val
                elif "bcr_subspec_id" in x[val]:
                    bcr_subspec_id=val
                elif "rave_spec_id" in x[val]:
                    rave_spec_id=val


        else:
            item=x[pubID]+"_"+x[pub_spec_id]+"_"+x[pub_subspec_id]
            itemVal=x[ID]+"_"+x[rave_spec_id]+"_"+x[bcr_subspec_id]
            # print(itemVal,item)
            if item in enrollDic:
                if itemVal == enrollDic.get(item):
                    continue
                else:
                    print("ERRRRROORRRRRRRRRR present in dictonary", item,itemVal)
            else:
                enrollDic[item]=itemVal
                # print(item,itemVal)


#Searching in CMB Specimen Transmittal file to get the data
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
inter = open("specimen_transmittal.CSV", 'r')
interfh = csv.reader(inter)
SpecimenTrans={}
for i in interfh:
    if i[0].startswith("project"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="RecordActive":
                RecordActive=col
            elif i[col]=="RecordId":
                RecordId=col
            elif i[col] == "SPECID":
                SPECID = col
            elif i[col] == "DXGRP":
                DXGRP = col
            elif i[col] == "BEDAT_RAW":
                BEDAT = col
            elif i[col] == "BETIM":
                BETIM = col
            elif i[col] == "SPECCAT":
                SPECCAT = col
            elif i[col] == "MEDTYPE":
                MEDTYPE = col
            elif i[col] == "CLMTHIND":
                CLMTHIND = col
            elif i[col] == "TUBETYPE":
                TUBETYPE = col
            elif i[col] == "BESLPR":
                BESLPR = col
            elif i[col] == "NUMCHSD":
                NUMCHSD = col
            elif i[col] == "NUMUCHSD":
                NUMUCHSD = col
            elif i[col] == "NUMALIQ":
                NUMALIQ = col
            elif i[col] == "BESTDAT_X1_RAW":
                BESTDAT_X1 = col
            elif i[col] == "BESTTIM_X1":
                BESTTIM_X1 = col
            elif i[col] == "BEENDAT_X1_RAW":
                BEENDAT_X1 = col
            elif i[col] == "BEENTIM_X1":
                BEENTIM_X1 = col
            elif i[col] == "TISTYP":
                TISTYP = col
            elif i[col] == "BSNAM":
                BSNAM = col
            elif i[col] == "BSTEST":
                BSTEST = col
            elif i[col] == "BSSTDAT_RAW":
                BSSTDAT = col
            elif i[col] == "BSSTTIM":
                BSSTTIM = col
            elif i[col] == "BECLMETH_SPD":
                BECLMETH_SPD = col
            elif i[col] == "BECLMETH_SPD_X1":
                BECLMETH_SPD_X1 = col
            elif i[col] == "BSREFID":
                BSREFID = col
            elif i[col] == "BSPDMRYN":
                BSPDMRYN = col
            elif i[col] == "BSORRES":
                BSORRES = col
            elif i[col] == "BSORRESU":
                BSORRESU = col
            elif i[col] == "BSORRES_PF":
                BSORRES_PF = col
            elif i[col] == "SPECSRC":
                SPECSRC = col

    else:
        vv=i[sub].split("-")
        if i[RecordActive]=='0' or vv[1] >"0250":
            continue
        else:
            tal = i[sub] + "_" + i[SPECID]+"_"+i[BSREFID]
            hh = [i[RecordId], i[DXGRP], i[BSPDMRYN], i[BEDAT], i[BETIM], i[SPECCAT], i[BECLMETH_SPD],i[CLMTHIND],i[BECLMETH_SPD_X1],i[TUBETYPE],i[BESLPR],i[NUMCHSD],i[NUMUCHSD],i[NUMALIQ],i[BESTDAT_X1],i[BESTTIM_X1],i[BEENDAT_X1],i[BEENTIM_X1],i[TISTYP],i[SPECSRC],i[BSNAM],i[BSTEST],i[BSSTDAT],i[BSSTTIM],i[BSORRES],i[BSORRESU],i[BSORRES_PF]]
            if hh==[]:
                continue
            else:
                if tal in SpecimenTrans:
                    if hh in SpecimenTrans.get(tal):
                        continue
                    else:
                        # print ("YESSSSSSSSSSS",tal)
                        SpecimenTrans[tal].append(hh)
                else:
                    SpecimenTrans[tal] = []
                    SpecimenTrans[tal].append(hh)
    #
for m,n in SpecimenTrans.items():
    print(m,n)
for con in specimentransfh:
    if "SUBJECT_ID" in con[0]:
        for cont in range(0, len(con)):
            if "SUBJECT_ID" in con[cont]:
                subject = cont
            elif "SAMPLE_ID" in con[cont]:
                samp = cont
            elif "SUBSPECIMEN_ID" in con[cont]:
                subspec = cont
    else:
        t = con[subject] + "_" + con[samp]+"_"+con[subspec]
        if t in enrollDic:
            hhh = enrollDic.get(t)
            # print(hhh,type(hhh),t)
            if hhh in SpecimenTrans:
                if len(SpecimenTrans.get(hhh)) == 1:
                    # print (t, enrollDic.get(t), DeathSummary.get(hhh),           'pppp')
                    output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "\t".join(
                        SpecimenTrans.get(hhh)[0]) + "\n")
                else:
                    for each in SpecimenTrans.get(hhh):
                        output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "\t".join(each) + "\n")
            # else:
                # output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")

        # else:
        #     if con[subspec]=="":
        #         if t in specimentrans:
        #             print(t,"aaa")
        #             output.write("\t".join(t.split("_")) + "\t" + "\t".join(specimentrans.get(t)) + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")
        #



