import os, csv

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
# inven=open("Inventory_Output.txt",'r')
entity=open("entity_ids.20220411.1.txt",'r')
# invenfh=inven.readlines()
entityfh=entity.readlines()
enDic={}
pubID={}
subspec={}

for en in entityfh:
    en=en.rstrip().split("\t")
    if en[0]=="" or en[2]=="":
        continue
    else:
        k=en[0]+"_"+en[2]
        if k in enDic:
            if en[6]==enDic.get(k):
                continue
            else:
                print(k,"EROOOOORRRRRR")
        else:
            enDic[en[0]+"_"+en[2]]=en[6]
            pubID[en[0]]=en[4]
            subspec[en[0]+"_"+en[1]]=en[5]
            enDic[en[0] + "_" + en[2]]=en[4]



for i, j in enDic.items():
    print(i,j)






