import os
os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
ther=open("Tartherapy-withSiteand ID.txt",'r')
outputfinal=open("TargetedTherapySeperated.txt",'w')
outputfinal.write("Participant ID"+"\t"+"Site"+"\t"+"Disease Code"+"\t"+"Drug"+"\n")

for i in ther:
    i=i.rstrip().split("\t")
    if "," in i[3]:
        aa=i[3].split(",")
        print(aa)
        for val in aa:
            print("\t".join(i[:3])+"\t"+val)
            outputfinal.write("\t".join(i[:3])+"\t"+val.replace('"','').replace(" ","")+"\n")
    else:
        outputfinal.write("\t".join(i)+"\n")

