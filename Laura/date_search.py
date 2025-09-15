import os

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")

file=open("result.txt",'r')
fileh=file.readlines()

k=open("result-1.txt",'r')
kh=k.readlines()
K_dic={}

for line in kh:
    line=line.rstrip().split("\t")
    # print(line)
    mykey=line[0]+"_"+line[1]
    if mykey in K_dic:
        print(mykey,"error")
    else:
        K_dic[mykey]=line[-1]

for i in fileh:
    i=i.rstrip().split("\t")
    if i[0]+"_"+i[1] in K_dic:
        print("\t".join(i),"\t",K_dic.get(i[0]+"_"+i[1]))


# for i in fileh:
#     print(i)