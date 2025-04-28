import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
spectrans=open("specimen_transmittal_output_seperate.csv",'r')
specfh=csv.reader(spectrans)

spectrac=open("CMB_specimen_tracking_enrollment.CSV",'r')
spectransfh=csv.reader(spectrac)
spectrackList=[]
for i in spectransfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "DXGRP":
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
            elif i[col] == "BESPID":
                BESPID = col
            elif i[col] == "LBLNUM":
                LBLNUM = col
            elif i[col] == "PATHXFN":
                PATHXFN = col
            elif i[col] == "MOLXFN":
                MOLXFN = col
            elif i[col] == "NEWSPEC_DRV":
                NEWSPEC_DRV = col
            elif i[col] == "NEWHIDDENLABEL_DRV":
                NEWHIDDENLABEL_DRV = col
            elif i[col] == "NEWPL_DRV":
                NEWPL_DRV = col
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
            else:
                if i[col] == "SiteNumber":
                    SiteNum = col
    else:
        search3 = i[proj] + "_" + i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
        st=[search3,i[DXGRP],i[SNOMED_X2],i[ASMTTPT],i[SPECCAT],i[BESPEC_DSL],i[BEREFID],i[TISTYP],i[BESPID],i[LBLNUM],
            i[PATHXFN],i[MOLXFN],i[NEWSPEC_DRV],i[NEWHIDDENLABEL_DRV],i[NEWPL_DRV]]
        final = [x.replace('', "NA") if x == '' else x for x in st]
        spectrackList.append(final)

oncores = open("specimenTracking_enrollment_separate_Output.csv", 'w')

for i in specfh:
    newlist = [k[0] for k in spectrackList]
    if i[0] in newlist:
        for y in spectrackList:
            if i[0] == y[0]:
                oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
    else:
        if i[0].startswith("SujectID"):
            oncores.write(",".join(i) + "," + "DXGRP" + "," + "SNOMED_X2" + "," + "ASMTTPT" + "," + "SPECCAT" + "," + "BESPEC_DSL" +
                          "," + "BEREFID" + "," + "TISTYP" + "," + "BESPID" + "," + "LBLNUM" + "," + "PATHXFN" + "," + "MOLXFN" + "," +
                          "NEWSPEC_DRV" +"," + "NEWHIDDENLABEL_DRV" + "," + "NEWPL_DRV" + "\n")
        else:
            oncores.write(",".join(i) + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA"
                          + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + ","  + "\n")
