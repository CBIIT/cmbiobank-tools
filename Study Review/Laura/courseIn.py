import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
socio=open("INVout.txt",'r')
# sociofh=csv.reader(socio)
sociofh=socio.readlines()
courseIni=open("course_initiation.CSV",'r')
coursefh=csv.reader(courseIni)
conList={}
for i in coursefh:
        if i[0].startswith("projectid"):
            for col in range(0, len(i)):
                if i[col] == "ECTARGET":
                    ECTARGET = col
                elif i[col] == "ECDRGCLS":
                    ECDRGCLS = col
                elif i[col] == "TX_CYCLE_NUM":
                    cycle = col
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
                elif i[col] == "RecordActive":
                    RecordActive = col
                else:
                    if i[col] == "SiteNumber":
                        SiteNum = col
        else:
            if i[RecordActive]=="0":
                continue
            else:
                search3 = i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[proj] + "_" + i[SiteNum]
                ll=[search3,i[ECTARGET],i[ECDRGCLS],i[cycle]]
                final = [x.replace('', "NA") if x == '' else x for x in ll]
                val_final=[final[1]+"@ECTARGET",final[2]+"@ECDRGCLS",final[3]+"@cycle"]
                if final[0] in conList:
                    conList[final[0]].append(val_final)
                else:
                    conList[final[0]]=[]
                    conList[final[0]].append(val_final)

            # conList.append(final)

oncores = open("CourseOutput.txt", 'w')
neValue={}
for x,y in conList.items():
    ECTARGET=[item[0] for item in y]
    ECDRGCLS=[item[1] for item in y]
    cycle=[item[2] for item in y]
    unique=[set(ECTARGET),set(ECDRGCLS),set(cycle)]
    neValue[x]=unique

for mem in sociofh:
    mem=mem.rstrip().split("\t")
    print(mem[0])
    if mem[0] in neValue:
        oncores.write("\t".join(mem) + "\t" + str(neValue.get(mem[0])[0]) + "\t" + str(neValue.get(mem[0])[1])+ "\t" + str(neValue.get(mem[0])[2]) + "\n")
    else:
        if "Key" in mem[0]:
            oncores.write("\t".join(mem) +"\t"+"Therapy Targets"+"\t"+"Drug Class"+"\t"+"Targeted Therapy #"+ "\n")
        else:
            oncores.write("\t".join(mem) + "\t" + "NA" + "\t" + "NA"+ "\t" + "NA" + "\n")
# for i in sociofh:
#     newlist = [k[0] for k in conList]
#     if i[0] in newlist:
#         for y in conList:
#             if i[0] == y[0]:
#                 oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
#     else:
#         if i[0].startswith("Key"):
#             oncores.write(",".join(i) + "," + "Therapy Targets" + "," + "Drug Class"+","+"Targeted Therapy #"+ "\n")
#         else:
#             print(i)
#             oncores.write(",".join(i) + "," + "NA" + "," + "NA"+","+"NA"+"\n")