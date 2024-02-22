import os,csv
from collections import OrderedDict

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
test=open("specimenTracking_enrollment_Output.csv",'r')
testfh=csv.reader(test)

dbgap=open("entity_ids.20210516.csv",'r')
dbgapfh=csv.reader(dbgap)
dbgapList=[]
entity={}

for i in dbgapfh:
    if i[0].startswith("ctep_id"):
        for col in range(0, len(i)):
            if i[col] == "pub_spec_id":
                pub_spec_id = col
            else:
                if i[col] == "rave_spec_id":
                    rave_spec_id = col
    else:
        # print(i[rave_spec_id],i[pub_spec_id])
        if i[rave_spec_id] not in entity:
            entity[i[rave_spec_id]]=[]
            entity[i[rave_spec_id]].append(i[pub_spec_id])
        else:
                entity[i[rave_spec_id]].append(i[pub_spec_id])
# for m,n in entity.items():
#     print(m,set(n))

oncores = open("data_Output.csv", 'w')

for i in testfh:
    print(i)
    if i[89] in entity:
        oncores.write(",".join(i)+","+",".join(list(OrderedDict.fromkeys(entity.get(i[89]))))+"\n")
    else:
        oncores.write(",".join(i)+","+"NA"+"\n")


    # print(i[89])
    # if i[0] in newlist:
    #     for y in dbgapList:
    #         if i[0] == y[0]:
    #             oncores.write(",".join(i) + "," + ",".join(y[1:]) + "\n")
    # else:
    #     if i[0].startswith("key"):
    #         oncores.write(",".join(i) + "," + "pub_spec_id" +"\n")
    #     else:
    #         oncores.write(",".join(i) + "," + "NA" + "\n")
