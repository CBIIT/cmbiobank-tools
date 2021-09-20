import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
f=open("offStudyOutput.txt",'r')
fh=f.readlines()
patient=open("PatientOutput.txt",'w')
# fh=csv.reader(f)

file=open("entity_ids_20210809.csv",'r')
fileH=csv.reader(file)

Dict_entity={}

for i in fileH:
    if i[0]=="NA":
        continue
    else:
        if i[0] in Dict_entity:
            if Dict_entity.get(i[0])==i[4]:
                continue
            else:
                print(i[0],i[4],"errorrrrr")
        else:
            Dict_entity[i[0]]=i[4]

for i in fh:
    i=i.rstrip().split("\t")
    if i[0]=="Key":
        patient.write("\t".join(i) + "\t" + "Public Subject ID" + "\n")
        for x in range(0,len(i)):
           if i[x]=="Subject":
               sub=x
           else:
               continue
    else:
        # print(i[sub])

        if i[sub] in Dict_entity:
            patient.write("\t".join(i)+"\t"+Dict_entity.get(i[sub])+"\n")
            print("\t".join(i),"\t",Dict_entity.get(i[sub]))