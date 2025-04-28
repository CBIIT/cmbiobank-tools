import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
bfile=open("CMB_biopsy_pathology_verification_and_assessment.csv",'r')
output1 = open("PathologyOut.txt", 'w')
output1.write("Subject"+"\t"+"MILOC"+"\t"+"MIORRES_TUCONT_X1"+"\t"+"MHTERM_DIAGNOSIS"+"\t"+"ENRICH_STD"+"\t"+"COVAL"+"\t"+"MIORRES_TUCONT_X2_STD"+"\n")
fhb=csv.reader(bfile)
for dat in fhb:
    # dat=dat.rstrip().split(",")
    if dat[0].startswith("projectid"):
        for x in range(0,len(dat)):
            if dat[x]=="MILOC_STD":
                miloc= x
            elif dat[x] =="MIORRES_TUCONT_X1_STD":
                tumcon1=x
            elif dat[x]=="MHTERM_DIAGNOSIS":
                # print(line[i],i)
                MHTERM_DIAGNOSIS=x
            elif dat[x] == "Subject":
                 # print(line[i], i)
                 sub=x
            elif dat[x] == "ENRICH_STD":
                 ENRICH_STD=x
            elif dat[x]=="COVAL":
                 COVAL=x
            else:
                if dat[x] =="MIORRES_TUCONT_X2_STD":
                    tumcon2=x
    else:
        output1.write(dat[sub]+"\t"+dat[miloc]+"\t"+dat[tumcon1]+"\t"+dat[MHTERM_DIAGNOSIS]+"\t"+dat[ENRICH_STD]+"\t"+dat[COVAL]+dat[tumcon2]+"\n")