import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
inv=open("outputreceiving.txt",'r')
invfh=inv.readlines()
ship=open("shipping_status.CSV",'r')
shipfh=csv.reader(ship)
shipList={}

for i in shipfh:
    if i[0].startswith("projectid"):
        for col in range(0, len(i)):
            if i[col] == "BESTDAT_RAW":
                BESTDAT = col
            elif i[col] == "BEPARTY":
                BEPARTY = col
            elif i[col] == "SPECID_DRV":
                SPECID = col
            elif i[col] == "SUBSPCM":
                SUBSPCM = col
            elif i[col] == "RecordActive":
                RecordActive = col
    else:
        if i[RecordActive]=="0":
            continue
        else:
            if i[BEPARTY]=="CLIA - Fredrick MoCha Lab":
                k=i[SPECID]+"_"+i[SUBSPCM].replace(", ","_").replace(",  ","_").replace("; ","_").replace(" , ","_").replace(",","_")
                if k in shipList:
                    print("EEEEEERRRRRRROOORRRRRRRR")
                else:
                    shipList[k]=i[BESTDAT]

for h, j in shipList.items():
    print(h,j)
oncores=open("shippingStatusMoChaOutput_output.txt",'w')
for y in invfh:
    y = y.rstrip().split("\t")
    if y[0].startswith("SubjectID"):
        for col1 in range(0, len(y)):
            if y[col1] == "Specimen ID":
                OSPECID = col1
            elif y[col1] == "Sub Specimen ID":
                DNASub = col1
            else:
                if y[col1] == "Associated RNA Sub Specimen":
                    RNAsub = col1
        oncores.write("\t".join(y)+"\t"+"Shipped to MoCha"+"\n")
    else:
        ook = y[OSPECID] + "_" + y[DNASub] + "_" + y[RNAsub]
        if ook in shipList:
            # print(ook)

            oncores.write("\t".join(y)+"\t"+shipList.get(ook)+"\n")
        else:
            print(ook)

            oncores.write("\t".join(y)+"\t"+"NA"+"\n")







    # newlist = [k[0] for k in shipList]
    # if i[0] in newlist:
    #     for y in shipList:
    #         # print(y[2])
    #         if i[0]==y[0]:
    #             if y[2]=="CLIA - Fredrick MoCha Lab":
    #                     oncores.write(",".join(i)+","+"-"+","+y[1]+","+"-"+"\n")
    #             elif "Van Andel Research" in y[2]:
    #                     oncores.write(",".join(i)+","+y[1]+","+"-"+","+"-"+"\n")
    #             elif y[2]=="PDMR Laboratory":
    #                     oncores.write(",".join(i)+","+"-"+","+"-"+","+y[1]+"\n")
    # else:
    #     if i[0].startswith("SubjectID"):
    #         oncores.write(",".join(i)+","+"Shipped Date(destination)-VARI"+","+"Shipped Date(destination)-MoCha"+","+"Shipped Date(destination)-PDMR"+"\n")
    #     else:
    #         oncores.write(",".join(i)+","+"NA"+","+"NA"+","+"NA"+"\n")













