import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
spectrans=open("shippingStatusMoChaOutput_output.txt",'r')
specfh=spectrans.readlines()
spectrac=open("CMB_specimen_tracking_enrollment.CSV",'r')
spectransfh=csv.reader(spectrac)
spectrackList=[]
for i in spectransfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "SPECCAT":
                SPECCAT = col
            elif i[col] == "ASMTTPT":
                ASMTTPT = col
            elif i[col] == "BESPEC_DSL":
                BESPEC_DSL = col
            elif i[col] == "TISTYP":
                TISTYP = col
            elif i[col] == "subjectId":
                # print(line[i],i)
                subId = col
            elif i[col] == "Subject":
                # print(line[i], i)
                sub = col
            elif i[col] == "siteid":
                siteid = col
            elif i[col] == "Site":
                Site = col
            elif i[col] == "project":
                proj = col
            elif i[col] == "SPECID_DRV":
                SPECID = col
            elif i[col] == "RecordActive":
                RecordActive = col
            else:
                if i[col] == "SiteNumber":
                    SiteNum = col
    else:
        search3 = i[proj]+"_"+i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]+"_"+i[SPECID]
        st=[search3,i[ASMTTPT],i[SPECCAT],i[BESPEC_DSL],i[TISTYP]]
        final = [x.replace('', "NA") if x == '' else x for x in st]
        if i[RecordActive]=="0":
            continue
        else:
            spectrackList.append(final)

oncores = open("specimenTracking_enrollment_Output.txt", 'w')

for i in specfh:
    i=i.rstrip().split("\t")
    # print(i[0], "Yesssss")
    newlist = [k[0] for k in spectrackList]
    if i[0] in newlist:
        for y in spectrackList:
            if i[0] == y[0]:
                print(i[0])
                oncores.write("\t".join(i) + "\t" + "\t".join(y[1:]) + "\n")
    else:
        if i[0].startswith("SubjectID"):
            oncores.write("\t".join(i) + "\t" + "Assessment Timepoint" + "\t" + "Specimen category" + "\t" + "Specimen Type" + "\t" + "Type of tissue"  + "\n")
        else:
            oncores.write("\t".join(i) + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA"  + "\n")
