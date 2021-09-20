import os,csv
from dateutil import parser

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
file=open("CMB_enrollment.CSV",'r')
file2=open("enrollmentData.csv",'w')
file2.write("project"+","+"SubjectId"+","+"Subject"+","+"siteid"+","+"Site"+","+"SiteNum"+","+"Age"+","+"Enrollment Date"+","+"Ethnicity"+","+"Sex"+","+
            "Gender"+","+"Race1"+","+"Race2"+","+"Race3"+","+"Race4"+","+"Race5"+","+"Race6"+","+"Race7"+","+"Disease Code"+","+"Enrolling Site CTEP ID "+"\n")
fh=file.readlines()

def enroll():
    for line in fh:
        line=line.rstrip().split(",")
        if line[0].startswith("projectid"):
            for i in range(0,len(line)):
                if line[i]=="project":
                    # print(line[i],i)
                    project=i
                elif line[i]=="subjectId":
                    # print(line[i],i)
                    subId=i
                elif line[i] == "Subject":
                     # print(line[i], i)
                     sub=i
                elif line[i] == "siteid":
                     siteid=i
                elif line[i] == "Site":
                     Site=i
                elif line[i] == "AGE":
                     age=i
                elif line[i] == "DSSTDAT_ENROLLMENT":
                     enrolldate=i
                elif line[i] == "ETHNIC":
                    ethnic = i
                elif line[i] == "SEX":
                    sex = i
                elif line[i] == "GENDER":
                    gender = i
                elif line[i] == "RACE_01":
                    race1 = i
                elif line[i] == "RACE_02":
                    race2 = i
                elif line[i] == "RACE_03":
                    race3 = i
                elif line[i] == "RACE_04":
                    race4 = i
                elif line[i] == "RACE_05":
                    race5 = i
                elif line[i] == "RACE_06":
                    race6 = i
                elif line[i] == "RACE_07":
                    race7 = i
                elif line[i] == "CTEP_SDC_MED_V10_CD":
                    ctep_sdc = i
                elif line[i] == "CTEPID":
                    CTEPID = i
                else:
                    if line[i] == "SiteNumber":
                        # print(line[i], i)
                        SiteNum = i
        else:
            aa=[line[project],line[subId],line[sub],line[siteid],line[Site],line[SiteNum],line[age],line[enrolldate],line[ethnic],line[sex],\
              line[gender],line[race1],line[race2],line[race3],line[race4],line[race5],line[race6],line[race7],line[ctep_sdc],line[CTEPID],line[Site]]
            print(aa)

            file2.write(",".join(aa)+"\n")

enroll()