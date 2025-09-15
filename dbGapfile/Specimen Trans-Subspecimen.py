#This code will get the sub specimen to the Specimen Transmittal DS file

import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
entity=open("entity_ids.20231204.csv",'r')
specimentrans=open("6a_Specimen Transmittal.csv",'r')
# output=open("6a_Specimen Transmittal-output.txt",'w')
specimentransfh=csv.reader(specimentrans)
entityfh=csv.reader(entity)
enrollDic={}

for x in entityfh:
    # print(x)
    if x[5]=="":
        continue
    else:
        if "ctep_id" in x[0]:
            for val in range(0,len(x)):
                # print(x[val])
                if x[val]=="pub_id":
                    pubID=val
                elif "ctep_id" in x[val]:
                    ID=val
                elif "pub_spec_id" in x[val]:
                    pub_spec_id=val
                elif "pub_subspec_id" in x[val]:
                    pub_subspec_id=val
                elif "bcr_subspec_id" in x[val]:
                    bcr_subspec_id=val
                elif "rave_spec_id" in x[val]:
                    rave_spec_id=val


        else:
            item=x[pubID]+"_"+x[pub_spec_id]
            itemVal=x[pub_subspec_id]
            # print(itemVal,item)
            if item in enrollDic:
                if itemVal in enrollDic.get(item):
                    continue
                else:
                    enrollDic[item].append(itemVal)
            else:
                enrollDic[item]=[]
                enrollDic[item].append(itemVal)

output=open("specimentransmittal_Subspecimen.csv",'w')
for m,n in enrollDic.items():
    for j in n:
        print(m.split("_"),j)
        output.write(",".join(m.split("_"))+","+j+"\n")

    # print (m,n)

