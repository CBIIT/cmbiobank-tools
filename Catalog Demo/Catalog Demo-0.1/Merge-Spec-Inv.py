import os

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
con = open("Megered Patient-Spec Data.txt", 'r')
confh = con.readlines()
Inv=open("Inventory_Output.txt",'r')
Invfh=Inv.readlines()
outputPatSpec = open("Merged Data.txt", 'w')

Patient = {}

for i in confh:
    i=i.rstrip().split("\t")
    if i[0].startswith("Participant ID"):
        for col in range(0, len(i)):
            if i[col] == "Participant ID":
                Participant_ID = col
            elif i[col] == "SPECID":
                SPECID = col

    else:
        search=i[Participant_ID]+"_"+i[SPECID]
        if search in Patient:
            print("ERRRRROORRRRRRRRR")
        else:
            Patient[search]=i[1:]

for x in Invfh:
    x=x.rstrip().split("\t")

for m,n in Patient.items():
    print(m)
    for x in Invfh:
        x = x.rstrip().split("\t")
        search2=x[0]+"_"+x[1]
        if m == search2:
            print(m+"\t"+"\t".join(n)+"\t"+"\t".join(x[1:])+"\n")
            outputPatSpec.write(m+"\t"+"\t".join(n)+"\t"+"\t".join(x[1:])+"\n")

