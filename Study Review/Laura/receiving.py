import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
file1=open("specimen_transmittal_output_seperate.txt","r")
Fout=file1.readlines()
file=open("receiving_status.csv",'r')
fh=csv.reader(file)
receiving={}
samp={}


for i in fh:
    if "projectid" in i[0]:
        for col in range(0,len(i)):
            if i[col]=="SITEID_X2":
                SITEID=col
            elif i[col]=="SUBSPCM":
                SUBSPCM=col
            elif i[col]=="BESTDAT_RAW":
                BESTDAT_RAW=col
            elif i[col]=="SPCADQYN":
                SPCADQYN=col
            elif i[col]=="INADREAS":
                INADREAS=col
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
                    if i[INADREAS]=="":
                        data = [i[BESTDAT_RAW], i[SPCADQYN], "NA"]
                    else:
                        data=[i[BESTDAT_RAW],i[SPCADQYN],i[INADREAS]]
                    receiving[i[SUBSPCM]]=data
output=open("outputreceiving.txt",'w')
for x in Fout:
    x=x.rstrip().split("\t")
    if "SubjectID" in x[0]:
        for every in range(0,len(x)):
            if x[every]=="Sub Specimen ID":
                ID=every
<<<<<<< Updated upstream
        output.write("\t".join(x) + "\t" + "Shipped to VARI" +"\t"+"Specimen adequacy when received at VARI"+"\t"+"Reason for inadequacy"+ "\n")
=======
        output.write("\t".join(x) + "\t" + "Shipped to VARI" +"\t"+"Specimen inadequacy when received at VARI"+"\t"+"Reason for inadequacy"+ "\n")
>>>>>>> Stashed changes
    else:
            if x[ID] in receiving:
                output.write("\t".join(x)+"\t"+"\t".join(receiving.get(x[ID]))+"\n")
            else:
                output.write("\t".join(x)+"\t"+"NA"+"\t"+"NA"+"\t"+"NA"+"\n")

for k,l in receiving.items():
    print(k,l)


