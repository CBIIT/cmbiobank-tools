import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
file1=open("nontargetRD.txt","r")
RemoveDup=open("Remove Duplicates-NT.txt","w")
Fout=file1.readlines()



for i in Fout:
    i=i.rstrip().split(",")

    if len(i)>1:
        k=[set(i)]
        RemoveDup.write((str(k))+"\n")
        print(k)
    else:
        RemoveDup.write("\t".join(i)+"\n")
        print(i)
