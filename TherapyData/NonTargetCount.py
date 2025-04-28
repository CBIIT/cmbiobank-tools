import os
os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
ther=open("nontargetCount.txt",'r')
outputfinal=open("NonTargetedTherapyCount.txt",'w')
outputfinal.write("Disease Code"+"\t"+"Drug"+"\t"+"Count"+"\n")

Therapy={}

for i in ther:
    i=i.rstrip().split("\t")
    if "," in i[1]:
        val=i[1].split(",")
        for y in val:
            text=i[0]+"_"+y.replace('"','').replace(" ","")
            if text in Therapy:
                Therapy[text].append("1")
            else:
                Therapy[text]=[]
                Therapy[text].append("1")
    else:
        search=i[0]+"_"+i[1]
        if search in Therapy:
            Therapy[search].append("1")
        else:
            Therapy[search] = []
            Therapy[search].append("1")


for m,n in Therapy.items():
    outputfinal.write("\t".join(m.split("_"))+"\t"+str(len(n))+"\n")
    print(m,n,len(n))



