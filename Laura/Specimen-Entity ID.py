import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
entity=open("entity_ids_20210809.csv",'r')
entityfh=csv.reader(entity)

specEn=open("specimenEnrollmentdate-output.txt",'r')
enrollSpecimen=specEn.readlines()
enrollDateList={}

for i in entityfh:
    if i[0]=="NA":
        continue
    else:
        if i[0].startswith("ctep_id"):
            for col in range(0, len(i)):
                if i[col] == "ctep_id":
                    ctep_id = col
                elif i[col] == "rave_spec_id":
                    rave = col
                elif i[col] == "pub_id":
                    pub_id = col
                elif i[col] == "pub_spec_id":
                    pub_spec_id = col
                elif i[col] == "pub_subspec_id":
                    pub_subspec_id = col
                else:
                    if i[col] == "bcr_subspec_id":
                     subspec = col

        else:
            search3 = i[ctep_id]+"_"+i[rave]+"_"+i[subspec]
            if search3 in enrollDateList:
                print("ERRRRRRORRRRRR")
            else:
                enrollDateList[search3]=[]
                k=[i[pub_id],i[pub_spec_id],i[pub_subspec_id]]
                enrollDateList[search3].append(k)

# for l,m in enrollDateList.items():
#     print(l,m)

fullList=[]
output=open("specimen-enity.txt","w")
for y in enrollSpecimen:
    y=y.rstrip().split("\t")
    # print(y)
    if y[0].startswith("SubjectID"):
        for col in range(0, len(i)):
            if y[col] == "SubjectID":
                SubjectID = col
            elif y[col] == "Specimen ID":
                 Specimen_ID = col
            else:
                if y[col] == "Sub Specimen ID":
                    Sub_Specimen_ID = col
        output.write("\t".join(y) + "\t" + "Public ID" + "\t" + "Public Specimen ID" + "\t" + "Public Sub-Specimen ID" + "\n")


    else:
        search4 = y[SubjectID] + "_" + y[Specimen_ID]+"_"+y[Sub_Specimen_ID]
        print(search4)
        ff=[search4,y]
        fullList.append(ff)

        if search4 in enrollDateList:
            output.write("\t".join(y)+"\t"+"\t".join(enrollDateList.get(search4)[0])+"\n")
        else:
                output.write("\t".join(y) + "\t" + "NA"+ "\t" + "NA"+ "\t" + "NA" + "\n")










