#replacing the orginal names with RXNorm Database names after spell check

import io,os,nltk,re

os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
wordlist=open("satndarNamesNonT.txt",'r',encoding="ISO-8859-1")
file=open("FilteredNontargeted-therapy.txt","r")
output=open("StandarNamesNon-Targeted.txt",'w')
fh=file.readlines()
names=wordlist.readlines()
dic={}

for i in names:
    i=i.rstrip().split("\t")
    if i[0] in  dic:
        # print(i[0])
        print("Repeated value found")
    else:
        dic[i[0].replace(" ","")]=i[1]

for x in fh:
    x=x.rstrip().split("\t")
    temp=[]
    z=x[1].split(",")
    # print(z)
    for val in z:
        rep=val.replace('"',"").replace(" ","")
        # print(rep)
        if rep=="NA" or rep=="Non-Targeted Therapy":
            continue
        else:
            if rep in dic:
                temp.append(dic.get(rep))
            else:
              print(rep,"Drug not found")
    output.write("\t".join(x[0:1])+"\t"+str(temp)+"\t"+"\t".join(x[2:])+"\n")



