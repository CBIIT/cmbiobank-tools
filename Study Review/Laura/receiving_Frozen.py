import os,csv
os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")

bio=open("receiving_status.CSV",'r')
revfh=csv.reader(bio)
c=0
dup={}
out=open("FrozenSample_output.txt",'w')
for line in revfh:
    if line[0].startswith("projectid"):
        for col in range(0, len(line)):
            # print(line[col])
            if "InstanceName" ==line[col]:
                InstanceName=col
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
            elif line[col] == "SITEID_X2":
                SITEID_X2 = col
            elif line[col] == "SUBSPCM":
                SUBSPCM = col
            elif line[col] == "SPECID2_DRV":
                SPECID2_DRV = col
            else:
                if line[col] == "SiteNumber":
                    SiteNum = col
    else:
        if line[RecordActive]=='0':
            continue
        else:
            if "Frozen" in line[InstanceName] or "Slide" in line[InstanceName] or "FFPE" in line[InstanceName]or "Bone Marrow Aspirate" in line[InstanceName]:
                if "Andel" in line[SITEID_X2]:
                    search = line[proj] + "_" + line[subId] + "_" + line[sub] + "_" + line[siteid] + "_" + line[Site] + "_" + line[SiteNum] + "_" + line[SPECID2_DRV]
                    y=search,line[SPECID2_DRV]
                    if line[SUBSPCM] in dup:
                        continue
                    else:
                        dup[line[SUBSPCM]]=y
                    c+=1


            # if line[InstanceName].endswith("0000"):
            #     search = line[proj] + "_" + line[subId] + "_" + line[sub] + "_" + line[siteid] + "_" + line[
            #         Site] + "_" + line[
            #                  SiteNum] + "_" + line[MIREFID]
            #     if line[BSREFID_DRV] in dup:
            #         continue
            #     else:
            #         dup[line[BSREFID_DRV]]=[search,line[MIREFID]]
            #     c+=1
            #     # print(line[BSREFID_DRV], c)
for i,j in dup.items():
    print(i,j)
    out.write(j[0]+"\t"+j[1]+"\t"+i+"\n")
