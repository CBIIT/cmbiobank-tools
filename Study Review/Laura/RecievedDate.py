import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
file1=open("specimenEnrollmentdate-output.txt","r")
Fout=file1.readlines()
file=open("CMB_receiving_status.csv",'r')
fh=csv.reader(file)
receiving={}


for i in fh:
    if "projectid" in i[0]:
        for col in range(0,len(i)):
            if i[col]=="SITEID_X2":
                SITEID=col
            elif i[col]=="SUBSPCM":
                SUBSPCM=col
            elif i[col]=="BEENDAT_RAW":
                BESTDAT_RAW=col
            else:
                if i[col]=="RecordActive":
                    RecordActive=col
    else:
        if i[RecordActive]=="0" or i[SUBSPCM]=="":
            continue
        else:
            if "Andel" in i[SITEID]:
                if i[SUBSPCM] in receiving:
                    print("error")
                else:
                    receiving[i[SUBSPCM]]=i[BESTDAT_RAW]
output=open("outputRecievedDate.txt",'w')
for x in Fout:
    x=x.rstrip().split("\t")
    if "Participant ID" in x[0]:
        for every in range(0,len(x)):
            if x[every]=="Sub Specimen ID":
                ID=every
        output.write("\t".join(x) + "\t" + "Received at VARI" + "\n")
    else:
        if x[ID] in receiving:
            output.write("\t".join(x)+"\t"+receiving.get(x[ID])+"\n")
        else:
            output.write("\t".join(x)+"\t"+"NA"+"\n")

for k,l in receiving.items():
    print(k,l)


