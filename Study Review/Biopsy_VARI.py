import os,csv
os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")

bio=open("biopsy_pathology_verification_and_assessment.CSV",'r')
biofh=csv.reader(bio)
c=0
dup={}
out=open("Biopsy_VARI_records.txt",'w')
for line in biofh:
    if line[0].startswith("projectid"):
        for col in range(0, len(line)):
            # print(line[col])
            if "BSREFID_DRV" ==line[col]:
                BSREFID_DRV=col
            elif line[col] == "subjectId":
                # print(line[i],i)
                subId = col
            elif line[col] == "Subject":
                # print(line[i], i)
                sub = col
            elif line[col] == "siteid":
                siteid = col
            elif line[col] == "Site":
                Site = col
            elif line[col] == "project":
                proj = col
            elif line[col] == "RecordActive":
                RecordActive = col
            elif line[col] == "MIREFID":
                MIREFID = col
            elif line[col] == "MIDAT_RAW":
                MIDAT_RAW = col
            else:
                if line[col] == "SiteNumber":
                    SiteNum = col
    else:
        if line[RecordActive]=='0':
            continue
        else:
            if line[BSREFID_DRV].endswith("0000"):
                search = line[proj] + "_" + line[subId] + "_" + line[sub] + "_" + line[siteid] + "_" + line[Site] + "_" + line[SiteNum] + "_" + line[MIREFID]
                if line[BSREFID_DRV] in dup:
                    continue
                else:
                    dup[line[BSREFID_DRV]]=[search,line[MIREFID],line[MIDAT_RAW]]
                c+=1
                # print(line[BSREFID_DRV], c)
for i,j in dup.items():
    print(i,j)
    out.write(j[0]+ "\t"+ j[1]+"\t"+"NA"+"\t"+i+"\t"+"NA"+"\t"+"NA"+"\t"+j[2]+"\n")
