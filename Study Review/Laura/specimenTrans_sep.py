import os,csv

dbgapid = []
spec = []

def spec_trans():
    os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
    filespecimen=open("CMB_specimen_transmittal.CSV",'r')
    MoChaFile=open("MoCha CLIA - 2021-09-10.csv",'r',encoding="ISO-8859-1")
    spec_transOutput=open("specimen_transmittal_output_seperate.txt",'w')
    spec_transOutput.write("SubjectID"+"\t"+"Specimen ID"+"\t"+"Blood Sample Quality"+"\t" + "Sub Specimen ID"+"\t" +"Associated RNA Sub Specimen"+"\t"+"Biospecimen Test Name"+"\t"+"VARI QC Start Date"+"\n")
    filefh=csv.reader(filespecimen)
    MoChafh=csv.reader(MoChaFile)
    clia={}
    RNAlist=[]

    for line in MoChafh:
        if line[0].startswith("Subject"):
            for ecol in range(0,len(line)):
                if line[ecol]=="BSI ID (DNA)":
                    DNA=ecol
                elif line[ecol]=="BSI ID (cDNA from RNA)":
                    RNA=ecol
        else:
            if line[DNA].startswith("CMB"):
                if line[DNA] in clia:
                    if line[RNA]==clia.get(line[DNA]):
                        continue
                    else:
                        print("ERRRRRRRROOORRRRRRRRRR")
                else:
                    clia[line[DNA]]=line[RNA]
                    if line[RNA].startswith("CMB"):
                        if line[RNA] in RNAlist:
                            continue
                        else:
                            RNAlist.append(line[RNA])

    trans_Date={}
    trans_Test={}
    trasn_meta={}
    for i in filefh:
        if i[0].startswith("projectid"):
            for col in range(0, len(i)):
                if i[col] == "SPECID":
                    SPECID = col
                elif i[col] == "BSTEST":
                    BSTEST = col
                elif i[col] == "BSSTDAT_RAW":
                    BSSTDAT = col
                elif i[col] == "BSREFID":
                    BSREFID = col
                elif i[col] == "BSORRES":
                    BSORRES = col
                elif i[col] == "BSORRESU":
                    BSORRESU = col
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
                elif i[col] == "BSNAM":
                    BSNAM = col
                elif i[col] == "BSPDMRYN":
                    BSPDMRYN = col
                elif i[col] == "BSORRES_PF":
                    BSORRES_PF = col
                elif i[col] == "RecordActive":
                    RecordActive = col
                else:
                    if i[col] == "SiteNumber":
                        SiteNum = col
        else:
            search = i[proj] + "_" + i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]+"_"+i[SPECID]
            # if "10323-7265GHK1-3" in i[SPECID]:
            y=[search,i[SPECID],i[BSORRES_PF]]
            if i[RecordActive]=="0":
                continue
            else:
                if i[BSTEST] in ["Blood Sample", "DNA Concentration","RNA Concentration"] and i[BSREFID]:
                    # print(search)
                    if i[BSREFID] in trans_Date:
                        # print(search,"1")
                        trans_Test[i[BSREFID]].append(i[BSTEST])
                        trans_Date[i[BSREFID]].append(i[BSSTDAT])
                    else:
                        # print(search,"2",i[BSREFID],y)
                        trasn_meta[i[BSREFID]]=y
                        trans_Date[i[BSREFID]]=[]
                        trans_Test[i[BSREFID]]=[]
                        trans_Test[i[BSREFID]].append(i[BSTEST])
                        trans_Date[i[BSREFID]].append(i[BSSTDAT])
    for x,y in trasn_meta.items():
        print(x,y)
        if x in clia:
            spec_transOutput.write("\t".join(y)+"\t"+x+"\t"+clia.get(x)+"\t"+str(set(trans_Test.get(x)))+"\t"+ str(set(trans_Date.get(x)))+"\n")
        elif x in RNAlist:
            continue
        else:
            spec_transOutput.write("\t".join(y)+"\t"+x+"\t"+ "NA"+"\t"+str(set(trans_Test.get(x)))+"\t"+ str(set(trans_Date.get(x)))+"\n")
    for k,l in trans_Date.items():
        print(k,l)





spec_trans()
