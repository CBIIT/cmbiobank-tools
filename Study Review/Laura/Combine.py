import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
file=open("enrollmentData.csv",'r')
output=open("EnrollmentOutput.csv",'w')
fh=csv.reader(file)
mainlist=[]
invkey={}
aa=[]
def enroll():
    for i in fh:
        if i[0].startswith("project"):
            for col in range(0, len(i)):
                if i[col] == "SubjectId":
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
                    if i[col] == "SiteNum":
                        SiteNum = col
            i.insert(0, "Key")
            i.append("CMTRT-Intervening Therapy")
            i.append("CMCAT-Intervening Therapy")
            aa.append(i)
        else:
            key=i[subId]+"_"+i[sub]+"_"+i[siteid]+"_"+i[Site]+"_"+i[proj]+"_"+i[SiteNum]
            d=[]
            for x in i:
                if x =="":
                    d.append(x.replace("","NA"))
                else:
                    d.append(x)
            d.insert(0,key)
            aa.append(d)


enroll()
for i in aa:
    # print(i)
    output.write(",".join(i) + "\n")
def intervening():
    interveninng=open("CMB_intervening_therapy.CSV",'r')
    inv=csv.reader(interveninng)
    for line in inv:
        if line[0].startswith("projectid"):
            for col in range(0, len(line)):
                if line[col] == "CMCAT":
                    cmcat = col
                elif line[col] == "CMTRT":
                    cmtrt = col
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
                elif line[col] == "RecordActive":
                    RecordActive = col
                elif line[col] == "project":
                    proj = col
                else:
                    if line[col] == "SiteNumber":
                        SiteNum = col
        else:
            if line[RecordActive]=="0":
                continue
            else:
                search=line[subId]+"_"+line[sub]+"_"+line[siteid]+"_"+line[Site]+"_"+line[proj]+"_"+line[SiteNum]
                l=[search,line[cmcat],line[cmtrt]]
                # print(l)
                final=[x.replace('',"NA") if x=='' else x for x in l]
                val_dic=[final[1]+"@CMAT",final[-1]+"@CMTRT"]
                # print(final)
                # invkey.append(final)
                if final[0] in invkey:
                    invkey[final[0]].append(val_dic)
                else:
                    invkey[final[0]]=[]
                    invkey[final[0]].append(val_dic)

intervening()
newSupp={}
for x,y in invkey.items():
    # print(x,y)
    CMTRT_val=[item[1] for item in y]
    CMCAT_val=[item[0] for item in y]
    finalval=[set(CMTRT_val),set(CMCAT_val)]
    newSupp[x]=finalval
out=open("INVout.txt",'w')
for x in aa:
    print(x)
    if x[0] in newSupp:
        print(x[0])
        out.write("\t".join(x) + "\t" + str(newSupp.get(x[0])[0]) + "\t" + str(newSupp.get(x[0])[1]) + "\n")
    else:
        if "Key" in x[0]:
            out.write("\t".join(x) + "\n")
        else:
            out.write("\t".join(x) + "\t" + "NA" + "\t" + "NA" + "\n")

