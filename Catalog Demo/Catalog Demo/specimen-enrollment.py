import os,csv

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
spec=open("specimen_transmittal_id_output.txt",'r')
output=open("Specid_enroll.txt",'w')
output.write("SubjectID"+"\t"+"BEDAT"+"\t"+"SPECCAT"+"\t"+"BECLMETH_SPD"+"\t"+"SPECID"+"\t"+"BESPEC_DRV"+"\t"+"ASMTTPT_DRV"+"\t"+"TISTYP"+"\t"+"BSTEST"+"\t"+"SubSpecimen-ID"+"\t"+"Public Subject ID"+"\t"+"Public_Subspecimen_id"+"\t"+"Public specimen ID"+"\t"+"Enrollment date"+"\n")
specfh=spec.readlines()
file=open("CMB_enrollment.CSV",'r')
fh=file.readlines()
data={}

for line in fh:
    line = line.rstrip().split(",")
    if line[0].startswith("projectid"):
        for i in range(0, len(line)):
            if line[i] == "DSSTDAT_ENROLLMENT_RAW":
                # print(line[i],i)
                DSSTDAT_ENROLLMENT = i
            elif line[i] == "Subject":
                sub = i
    else:
        data[line[sub]]=line[DSSTDAT_ENROLLMENT]
        # print(data)

for sp in specfh:
    sp=sp.rstrip().split("\t")
    print(sp)
    if "Subject" in sp:
        for col in range(0,len(sp)):
            if sp[col]=="Subject":
                subjid=col
                print(subjid)
    else:
        # print(data)
        if sp[subjid] in data:
            output.write("\t".join(sp)+"\t"+data.get(sp[subjid])+"\n")
            print("\t".join(sp)+"\t"+data.get(sp[subjid])+"\n")




