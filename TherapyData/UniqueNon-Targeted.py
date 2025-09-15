import os
os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
ther=open("StandarNamesNon-Targeted.txt",'r')
outputfinal=open("Non-TargetedTherapyUnique.txt",'w')

for i in ther:
    i=i.rstrip().split("\t")
    aa=i[1].replace('"','')

    unique_values = list(set(aa.split(", ")))
    outputfinal.write("\t".join(i[:1])+"\t"+str(unique_values)+"\t"+"\t".join(i[2:])+"\n")
    print(unique_values)

