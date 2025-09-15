#replacing the orginal names with RXNorm Database names after spell check

import io,os,nltk,re

os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
wordlist=open("satndarNamesT.txt",'r',encoding="ISO-8859-1")
file=open("Filteredtargeted-therapy.txt","r")
output=open("StandarNamesTargeted.txt",'w')
fh=file.readlines()
names=wordlist.readlines()
dic={}

for i in names:
    i=i.rstrip().split("\t")
    if i[0] in  dic:
        print("Repeated value found")
    else:
        dic[i[0].replace(" ","")]=i[1]

for x in fh:
    x=x.rstrip().split("\t")
    temp=[]
    z=x[2].split(",")
    for val in z:
        rep=val.replace('"',"").replace(" ","")
        if rep=="NA" or rep=="TargetedTherapy":
            continue
        else:
            if rep in dic:
                temp.append(dic.get(rep))
            else:
              print(rep,"Drug not found")
    output.write("\t".join(x[0:2])+"\t"+str(temp)+"\t"+"\t".join(x[3:])+"\n")



