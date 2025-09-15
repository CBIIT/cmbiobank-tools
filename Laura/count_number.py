import os

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")

file=open("count_number.txt",'r')
fh=file.readlines()
count={}
for i in fh:
    i=i.rstrip().split("\t")
    if i[0] in count:
        if i[1] in count.get(i[0]):
            continue
        else:
            count[i[0]].append(i[1])
    else:
        count[i[0]]=[]
        count[i[0]].append(i[1])

for i,j in count.items():
    print(i,"\t",len(j),"\t",j)