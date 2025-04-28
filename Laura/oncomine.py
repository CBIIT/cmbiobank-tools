import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
inv=open("specimenTracking_enrollment_Output.txt",'r')
invfh=inv.readlines()
onco=open("oncomine_result.CSV",'r')
oncofh=csv.reader(onco)
oncolist=[]

for i in oncofh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "PFORRES_SPD":
                PFORRES_SPD = col
            elif i[col] == "PFUPLDAT_RAW":
                pfupldat = col
            elif i[col] == "PFRESRS":
                PFRESRS = col
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
        onl=[search3,i[PFORRES_SPD],i[pfupldat],i[PFRESRS]]
        final = [x.replace('', "NA") if x == '' else x for x in onl]
        if i[RecordActive]=="0":
            continue
        else:
            oncolist.append(final)

oncores=open("oncoOutput.txt",'w')

for i in invfh:
    i=i.rstrip().split("\t")
    # if i[0]=="10323_40745_IL042-0024_1367_John H Stroger Jr Hospital of Cook County_IL042_10323-CE862F01-1":
    newlist = [k[0] for k in oncolist]
    if i[0] in newlist:
        print(i[0])
        for y in oncolist:
            if i[0]==y[0]:
                    if not i[3].endswith("0000"):
                        oncores.write("\t".join(i)+"\t"+"\t".join(y[1:])+"\n")
                    else:
                        oncores.write("\t".join(i) + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\n")
    else:
        if i[0].startswith("SubjectID"):
            oncores.write("\t".join(i)+"\t"+"Processing result "+"\t"+"Date of upload of results to Patient/Provider Portal "+"\t"+"Reason for failure "+"\n")
        else:
            oncores.write("\t".join(i)+"\t"+"NA"+"\t"+"NA"+"\t"+"NA"+"\n")













