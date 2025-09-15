#This file maps the unique records of the specimen file to the pathology file to get pathology feild information.

import os,csv
os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
file=open("CMB_biopsy_pathology_verification_and_assessment.CSV",'r')
fh=file.readlines()
file2=open("specimen_transmittal_output.csv",'r')
fh2=file2.readlines()
pat=[]
trans=[]

for val in fh2:
    val=val.rstrip().split(",")
    if val[0].startswith("key"):
        for i in range(0, len(val)):
            if val[i] == "SPECID":
                # print(line[i],i)
                SPECID = i
            elif val[i] == "BSREFID":
                # print(line[i],i)
                BSREFID = i
        val.insert(0,"key1")
        trans.append(val)
    else:
        key1=val[0]+"_"+val[SPECID]+"_"+val[BSREFID]
        val.insert(0,key1)
        trans.append(val)

for line in fh:
    line = line.rstrip().split(",")
    if line[0].startswith("projectid"):
        for i in range(0, len(line)):
            if line[i] == "project":
                # print(line[i],i)
                project = i
            elif line[i] == "subjectId":
                # print(line[i],i)
                subId = i
            elif line[i] == "Subject":
                # print(line[i], i)
                sub = i
            elif line[i] == "siteid":
                siteid = i
            elif line[i] == "Site":
                Site = i
            elif line[i] == "MIREFID":
                MIREFID = i
            elif line[i] == "SPLADQFL_X1":
                SPLADQFL_X1 = i
            elif line[i] == "ENRICH":
                ENRICH = i
            elif line[i] == "SPLADQFL_X2":
                SPLADQFL_X2 = i
            elif line[i] == "BSREFID_DRV":
                BSREFID_DRV = i
            elif line[i] == "COVAL":
                coval = i
            else:
                if line[i] == "SiteNumber":
                    # print(line[i], i)
                    SiteNum = i
    else:
        # print(line[project],line[subId],line[sub],line[siteid],line[Site],line[SiteNum])
        search = line[project] + "_" + line[subId] + "_" + line[sub] + "_" + line[siteid] + "_" + line[Site] + "_" + line[SiteNum]+"_"+line[MIREFID]+"_"+line[BSREFID_DRV]
        search1=[search,line[SPLADQFL_X1],line[ENRICH],line[SPLADQFL_X2],line[coval]]
        final = [x.replace('', "NA") if x == '' else x for x in search1]
        sub_final=final[1:]
        # pat.append(final)
        # if final[0] in pat:
        #     if pat.get(final[0])==sub_final:
        #         continue
        #     else:
        #         print("ERRRRRRRRRRRRROOOORRRRRRRRR")
        #         print(final[0],sub_final)
        #         pat[final[0]]=sub_final
        # else:
        #     pat[final[0]] = sub_final

Specimen_bio=open("Specimen_biopsy_pat_output.csv",'w')


# for i in trans:
#     newlist = [k[0] for k in pat]
#     # print(newlist)
#     if i[0] in newlist:
#         for y in pat:
#             if i[0]== y[0]:
#                 Specimen_bio.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
#     else:
#         if 'key'in i:
#             Specimen_bio.write(",".join(i) + "," + "SPLADQFL_X1" + "," + "ENRICH" + "," + "SPLADQFL_X2" + "," + "coval"  + "\n")
#         else:
#             Specimen_bio.write(",".join(i) + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA"  + "\n")





