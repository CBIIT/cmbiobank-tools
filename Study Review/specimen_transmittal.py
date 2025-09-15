import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
blood=open("BloodCollection_Output.csv",'r')
bloodfh=csv.reader(blood)

spec=open("CMB_specimen_transmittal.CSV",'r')
specfh=csv.reader(spec)
specList=[]
for i in specfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "USUBJID_DRV":
                USUBJID_DRV = col
            elif i[col] == "SPECID":
                SPECID = col
            elif i[col] == "MHLOC_DRV":
                MHLOC_DRV = col
            elif i[col] == "DXGRP":
                DXGRP = col
            elif i[col] == "ASMTTPT_DRV":
                ASMTTPT_DRV = col
            elif i[col] == "BEDAT":
                BEDAT = col
            elif i[col] == "BETIM":
                BETIM = col
            elif i[col] == "SPECCAT":
                SPECCAT = col
            elif i[col] == "BESPEC_DRV":
                BESPEC_DRV = col
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
            elif i[col] == "NUMSPEC":
                NUMSPEC = col
            elif i[col] == "ORNUMSPC":
                ORNUMSPC = col
            elif i[col] == "BESTDAT_X1":
                BESTDAT_X1 = col
            elif i[col] == "BESTTIM_X1":
                BESTTIM_X1 = col
            elif i[col] == "BEENDAT_X1":
                BEENDAT_X1 = col
            elif i[col] == "BEENTIM_X1":
                BEENTIM_X1 = col
            elif i[col] == "SPECSRC":
                SPECSRC = col
            elif i[col] == "BSNAM":
                BSNAM = col
            elif i[col] == "BSTEST":
                BSTEST = col
            elif i[col] == "BSSTDAT":
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
            elif i[col] == "SPECID_DBGAP":
                SPECID_DBGAP = col
            elif i[col] == "SUBSPCM_DBGAP":
                SUBSPCM_DBGAP = col
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
        search3 = i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[proj] + "_" + i[SiteNum]
        sp=[search3,i[USUBJID_DRV],i[SPECID],i[MHLOC_DRV],i[DXGRP],i[ASMTTPT_DRV],i[BEDAT],i[BETIM],i[SPECCAT],i[BESPEC_DRV],i[MEDTYPE],
                    i[CLMTHIND],i[TUBETYPE],i[BESLPR],i[NUMCHSD],i[NUMSPEC],i[ORNUMSPC],i[BESTDAT_X1],i[BESTTIM_X1],i[BEENDAT_X1],i[BEENTIM_X1],
                    i[SPECSRC],i[BSNAM],i[BSSTDAT],i[BSSTTIM],i[BECLMETH_SPD],i[BECLMETH_SPD_X1],i[BSREFID],i[BSPDMRYN],
                    i[BSORRES],i[BSORRESU],i[SPECID_DBGAP],i[SUBSPCM_DBGAP]]
        final = [x.replace('', "NA") if x == '' else x for x in sp]
        specList.append(final)

oncores = open("specimenTrans_Output.csv", 'w')

for i in bloodfh:
    newlist = [k[0] for k in specList]
    if i[0] in newlist:
        for y in specList:
            if i[0] == y[0]:
                oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
    else:
        if i[0].startswith("key"):
            oncores.write(",".join(i) + "," + "USUBJID_DRV"+"," + "SPECID"+"," + "MHLOC_DRV"+"," + "DXGRP"+"," + "ASMTTPT_DRV"+
                          "," + "BEDAT"+"," + "BETIM"+"," + "SPECCAT"+"," + "BESPEC_DRV"+"," + "MEDTYPE"+"," + "CLMTHIND"+"," + "TUBETYPE"+
                          "," + "BESLPR"+"," + "NUMCHSD"+"," + "NUMSPEC"+"," + "ORNUMSPC"+"," + "BESTDAT_X1"+"," + "BESTTIM_X1"+"," + "BEENDAT_X1"+","
                          + "BEENTIM_X1"+"," + "SPECSRC"+"," + "BSNAM"+"," + "BSSTDAT"+"," + "BSSTTIM"+"," + "BECLMETH_SPD"+"," +
                          "BECLMETH_SPD_X1"+"," + "BSREFID"+"," + "BSPDMRYN"+"," + "BSORRES"+"," + "BSORRESU"+"," + "SPECID_DBGAP"+"," + "SUBSPCM_DBGAP"+"\n")
        else:
            oncores.write(",".join(i) + "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"
                          + "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"
                          + "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"
                          + "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "," + "NA"+ "\n")

