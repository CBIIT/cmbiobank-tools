import os
os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
ther=open("StandarNamesTargeted.txt",'r')
outputfinal=open("TargetedTherapyUnique.txt",'w')

for i in ther:
    i=i.rstrip().split("\t")
    aa=i[2].replace('"','')

    unique_values = list(set(aa.split(", ")))
    outputfinal.write("\t".join(i[:2])+"\t"+str(unique_values)+"\t"+"\t".join(i[3:])+"\n")
    print(unique_values)

