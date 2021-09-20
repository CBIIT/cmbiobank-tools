import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
# socio=open("sociooutput.csv",'r')
# sociofh=csv.reader(socio)
courseIni=open("CMB_course_initiation.CSV",'r')
coursefh=csv.reader(courseIni)
conList=[]
for i in coursefh:
        if i[0].startswith("projectid"):
            for col in range(0, len(i)):
                if i[col] == "ECTARGET":
                    ECTARGET = col
                elif i[col] == "ECDRGCLS":
                    ECDRGCLS = col
                elif i[col] == "MALG_NEO_ANTM_TP":
                    MALG_NEO_ANTM_TP = col
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
            ll=[search3,i[ECTARGET],i[ECDRGCLS],i[MALG_NEO_ANTM_TP]]

            final = [x.replace('', "NA") if x == '' else x for x in ll]
            conList.append(final)

# oncores = open("CourseOutput.csv", 'w')
#
# for i in sociofh:
#     newlist = [k[0] for k in conList]
#     if i[0] in newlist:
#         for y in conList:
#             if i[0] == y[0]:
#                 oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
#     else:
#         if i[0].startswith("key"):
#             oncores.write(",".join(i) + "," + "ECTARGET" + "," + "ECDRGCLS"+ "," + "MALG_NEO_ANTM_TP" + "\n")
#         else:
#             print(i)
#             oncores.write(",".join(i) + "," + "NA" + "," + "NA"+ "," + "NA" + "\n")

for i in conList:
    print("\t".join(i))