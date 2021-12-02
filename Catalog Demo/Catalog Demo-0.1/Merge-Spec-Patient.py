import os

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
spec = open("Patient-Data.txt", 'r')
specfh = spec.readlines()
pat=open("Specid_enroll.txt",'r')
patfh=pat.readlines()
outputPatSpec = open("Merged-Spec-Patient.txt", 'w')

Patient = {}

for i in specfh:
    i=i.rstrip().split("\t")
    if i[0].startswith("Participant ID"):
        for col in range(0, len(i)):
            if i[col] == "Participant ID":
                Participant_ID = col

    else:
        if i[Participant_ID] in Patient:
            print("ERRRRROORRRRRRRRR")
        else:
            Patient[i[Participant_ID]]=i[1:]

for x in patfh:
    x=x.rstrip().split("\t")

for m,n in Patient.items():
    for x in patfh:
        x = x.rstrip().split("\t")
        if m == x[0]:
            print(m+"\t"+"\t".join(n)+"\t"+"\t".join(x[1:])+"\n")
            outputPatSpec.write(m+"\t"+"\t".join(n)+"\t"+"\t".join(x[1:])+"\n")

