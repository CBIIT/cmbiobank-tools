import os,csv


os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")

def bio():
    entity=open("entity_ids.20231204.csv",'r')
    biopsyPath=open("Biopsy-Path_Subspecimen.csv",'r')
    output=open("6a_Biopsy Pathology V & V.txt",'w')
    output.write("SUBJECT_ID"+"\t"+"SAMPLE_ID"+"\t"+"SUBSPECIMEN_ID"+"\t"+"P-ID"+"\t"+"S-ID"+"\t"+"SUB-ID"+"\t"+"LOGLINE_NUMBER"+"\t"+"ANATOMICAL_LOCATION"+"\t"+"START_DATE"+"\t"+"DIAGNOSIS"+"\t"+"DATE__OF_PATHOLOGY_ REVIEW"+"\t"+
                 "DATE_OF_PATHOLOGIST_SIGNATURE"+"\t"+"DIAGNOSIS_VERIFICATION"+"\t"+"PATHOLOGY_REVIEW_RESULT"+"\t"+"ESTIMATED_TUMOR_CONTENT"+"\t"+"SAMPLE_SUITABLE_FOR_ANALYSIS"+"\t"+"ENRICHMENT_INSTRUCTIONS"+"\t"+"ESTIMATED_TUMOR_CONTENT_AFTER_ENRICHMENT"+"\t"+"SAMPLE_SUITABLE_FOR_ANALYSIS_ENRICHMENT"+"\n")
    biopsyPathfh=csv.reader(biopsyPath)
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


    #Searching in CMB Biopsy Pathology file file to get the data
    os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
    inter = open("biopsy_pathology_verification_and_assessment.CSV", 'r')
    interfh = csv.reader(inter)
    BiopsyPathVer={}
    for i in interfh:
        if i[0].startswith("project"):
            for col in range(0,len(i)):
                if i[col]=="Subject":
                    sub=col
                elif i[col]=="RecordActive":
                    RecordActive=col
                elif i[col]=="RecordId":
                    RecordPosition=col
                elif i[col] == "MIREFID":
                    MIREFID = col
                elif i[col] == "MILOC":
                    MILOC = col
                elif i[col] == "PRSTDAT_RAW":
                    PRSTDAT = col
                elif i[col] == "MHTERM_DIAGNOSIS":
                    MHTERM_DIAGNOSIS = col
                elif i[col] == "MIDAT_RAW":
                    MIDAT = col
                elif i[col] == "SIGNDAT_X1_RAW":
                    SIGNDAT_X1 = col
                elif i[col] == "DXVERIF":
                    DXVERIF = col
                elif i[col] == "MIORRES_BPSY":
                    MIORRES_BPSY = col
                elif i[col] == "MIORRES_TUCONT_X1":
                    MIORRES_TUCONT_X1 = col
                elif i[col] == "SPLADQFL_X1":
                    SPLADQFL_X1 = col
                elif i[col] == "ENRICH":
                    ENRICH = col
                elif i[col] == "MIORRES_TUCONT_X2":
                    MIORRES_TUCONT_X2 = col
                elif i[col] == "SPLADQFL_X2":
                    SPLADQFL_X2 = col
                elif i[col] == "BSREFID_DRV":
                    BSREFID_DRV = col


        else:
            vv = i[sub].split("-")
            if i[RecordActive]=='0' or vv[1]>'0250':
                continue
            else:
                tal = i[sub] + "_" + i[MIREFID]+"_"+i[BSREFID_DRV]
                hh = [i[RecordPosition], i[MILOC], i[PRSTDAT], i[MHTERM_DIAGNOSIS], i[MIDAT], i[SIGNDAT_X1], i[DXVERIF],i[MIORRES_BPSY],i[MIORRES_TUCONT_X1],i[SPLADQFL_X1],i[ENRICH],i[MIORRES_TUCONT_X2],i[SPLADQFL_X2]]
                if hh==[]:
                    continue
                else:
                    if tal in BiopsyPathVer:
                        if hh in BiopsyPathVer.get(tal):
                            continue
                        else:
                            # print ("YESSSSSSSSSSS",tal)
                            BiopsyPathVer[tal].append(hh)
                    else:
                        BiopsyPathVer[tal] = []
                        BiopsyPathVer[tal].append(hh)
    # print(len(BiopsyPathVer))
    # for m,n in BiopsyPathVer.items():
    #     print(m,n)
    for con in biopsyPathfh:
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
                if hhh in BiopsyPathVer:
                    if len(BiopsyPathVer.get(hhh)) == 1:
                        # print (t, enrollDic.get(t), BiopsyPathVer.get(hhh),           'pppp')
                        output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "\t".join(BiopsyPathVer.get(hhh)[0]) + "\n")
                    else:
                        for each in BiopsyPathVer.get(hhh):
                            output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "\t".join(each) + "\n")
            else:
                output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "\t".join(each) + "\n")

                # else:
                #     output.write("\t".join(t.split("_")) + "\t" + "\t".join(hhh.split("_")) + "\t" + "-" + "\t" + "-" + "\t"+ "-" + "\t" + "-" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")

bio()
# comment the above def to run the below def also delete the non public ID's and add end of line to the file

def match():
    file=open("6a_Biopsy Pathology V & V.txt",'r')
    filefh=file.readlines()
    data=open("6a_Biopsy Pathology V-V.csv","r")
    datafh=data.readlines()
    pathout=open("pathalogyFinal.txt","w")
    lookupkey={}



    for val in filefh:
        val=val.rstrip().split("\t")
        if val[3]=="-":
            continue
        else:
            storeAc=val[0]+"_"+val[1]
            if storeAc in lookupkey:
                lookupkey[storeAc].append(val[2:])
            else:
                lookupkey[storeAc]=[]
                lookupkey[storeAc].append(val[2:])

    for rec in datafh:
        rec = rec.rstrip().split(",")
        if "SUBJECT_ID" in rec[0]:
            pathout.write("\t".join(rec)+"\n")
        else:
            find = rec[0] + "_" + rec[1]
            if find in lookupkey:
                print(find,"\t",len(lookupkey.get(find)))
                if len(lookupkey.get(find))>1:
                    for each in lookupkey.get(find):
                        pathout.write(rec[0]+"\t"+rec[1]+"\t"+"\t".join(each)+"\n")
                else:
                    # print(lookupkey.get(find))
                    pathout.write(rec[0]+"\t"+rec[1]+"\t"+"\t".join(lookupkey.get(find)[0])+"\n")
            else:
                pathout.write("\t".join(rec)+"\n")

# match()

