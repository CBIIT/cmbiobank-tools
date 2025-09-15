import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
spectrans=open("biopsy_pathOutput.txt",'r')
specfh=spectrans.readlines()

spectrac=open("enrollment.CSV",'r')
enrollSpecimen=csv.reader(spectrac)
enrollDateList={}
for i in enrollSpecimen:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "DSSTDAT_ENROLLMENT_RAW":
                DSSTDAT_ENROLLMENT = col
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
        search3 = i[proj]+"_"+i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
        st=[search3,i[DSSTDAT_ENROLLMENT],i[Site]]
        final = [x.replace('', "NA") if x == '' else x for x in st]
        # enrollDateList.append(final)
        if final[0] in enrollDateList:
            print("errorrrr")
        else:
            enrollDateList[search3]=[]
            enrollDateList[search3].append(final[-1])
            enrollDateList[search3].append(final[-2])

oncores = open("specimenEnrollmentdate-output.txt", 'w')
#
for i in specfh:
    i=i.rstrip().split("\t")
#     # print(type(i))
    i[0]=i[0].rstrip().split("_")
    l=i[0].pop(-1)
    s="_"
#     # print(i[0])
    s=s.join(i[0])
    del i[0]
    i.insert(0,s)
    # newlist = [k[0] for k in enrollDateList]
    if s in enrollDateList:
            oncores.write("\t".join(i) + "\t" + enrollDateList.get(s)[0]+"\t"+enrollDateList.get(s)[1] + "\n")
    else:
        if s.startswith(""):
            oncores.write("\t".join(i) + "\t" + "Enrollment Site" +"\t"+"Enrollment Date"+ "\n")
        else:
            oncores.write("\t".join(i) + "\t" + "NA"  + "\n")

