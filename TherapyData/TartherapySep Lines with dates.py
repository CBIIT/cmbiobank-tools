import os
os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
ther=open("StandarNamesTargeted.txt",'r')
outputfinal=open("TargetedTherapySeperated with dates.txt",'w')
outputfinal.write("Participant ID"+"\t"+"Enrollment Date"+"\t"+"Targeted Therapy"+"\t"+"Start Date"+"\t"+"End Date"+"\n")

for i in ther:
    i=i.rstrip().split("\t")
    if "," in i[2]:
        aa=i[2].split(",")
        bb=i[3].split(",")
        cc=i[4].split(",")

        for val in range(0,len(aa)):
            print("\t".join(i[:2])+"\t"+aa[val]+"\t"+bb[val]+"\t"+cc[val]+"\n")
    #         outputfinal.write("\t".join(i[:2])+"\t"+val.replace('"','').replace(" ","")+"\n")
    # else:
    #     outputfinal.write("\t".join(i)+"\n")

