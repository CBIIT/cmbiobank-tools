import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data")
<<<<<<< Updated upstream
entity=open("entity_ids.20211206.csv",'r')
=======
entity=open("entity_ids.20211010.csv",'r')
>>>>>>> Stashed changes
output=open("SubjectConsent-output.csv",'w')
consent=open("2a_SubjectConsent_DS.csv",'r')
consentfh=csv.reader(consent)
entityfh=csv.reader(entity)
enrollDic={}

for x in entityfh:
    # print(x)
    if x[0]=="NA":
        continue
    else:
        if "ctep_id" in x[0]:
            for val in range(0,len(x)):
                # print(x[val])
                if x[val]=="pub_id":
                    pubID=val
                elif "ctep_id" in x[val]:
                        ID=val
        else:
            item=x[pubID]
            itemVal=x[ID]
            # print(itemVal,item)
            if item in enrollDic:
                if itemVal in enrollDic.get(item):
                    continue
                else:
                    enrollDic[item].append(itemVal)
            else:
                enrollDic[item]=[]
                enrollDic[item].append(itemVal)

#
# for m,n in enrollDic.items():
#     print(m,n)


#Searching in CMB enrollment file to get the SEX
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/RAVE")
enroll = open("CMB_enrollment.CSV", 'r')
enrollfh = csv.reader(enroll)
EnrollmentSex={}
for i in enrollfh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="SEX":
                sex=col

    else:
        if i[sub] in EnrollmentSex:
            if i[sex] in EnrollmentSex.get(i[sub]):
                continue
            else:
                EnrollmentSex[i[sub]].append(i[sex])
        else:
            EnrollmentSex[i[sub]]=[]
            EnrollmentSex[i[sub]].append(i[sex])
for con in consentfh:
    entityDic={}
    if "SUBJECT_ID" in con[0]:
        for cont in range(0,len(con)):
            if "SUBJECT_ID" in con[cont]:
                sub=cont
<<<<<<< Updated upstream
            elif "CONSENT" in con[cont]:
                consent=cont
    else:
        t=con[sub]

=======
    else:
        t=con[sub]
>>>>>>> Stashed changes
        if t in enrollDic:
            cid=enrollDic.get(t)
            # print(t, len(enrollDic.get(t)))
            if len(cid)==1:
                if cid[0] in EnrollmentSex:
<<<<<<< Updated upstream
                    # print (t,con[consent],cid[0],EnrollmentSex.get(cid[0])[0])
                    output.write(t+","+con[consent]+","+EnrollmentSex.get(cid[0])[0]+"\n")
=======
                    print (t,cid[0],EnrollmentSex.get(cid[0])[0])
                    output.write(t+","+EnrollmentSex.get(cid[0])[0]+"\n")
>>>>>>> Stashed changes
            else:
                print ("ERRRRROORRRRRRRRRRRRRRRRRRR")







