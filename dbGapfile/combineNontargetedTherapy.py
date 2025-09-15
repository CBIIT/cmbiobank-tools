# open non targeted therapy data and add the values from 102 patient
import os
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE")
nonTargeted=open("prior__therapy_supplement.txt",'r')
nonTargetFinal=open("nontargeted_data.txt",'w')
nonTargetFinal.write("SUBJECT_ID"+"\t"+"CAT_THERAPY"+"\t"+"Enrollment Date"+"\t"+"THERAPY_START_DATE_DOSE"+"\t"+"Therapy"+"\t"+"THERAPY_END_DATE_LAST_DOSE"+"\t"+"THERAPY_END_DATE_REGIMEN"+"\t"+"FREQUENCY"+"\t"+"INTENDED_DOSE_REGIMEN"+"\t"+"DOSE"+"\t"+"DOSE_UNIT"+"\t"+"BEST_OVERALL_RESPONSE"+"\t"+"LOGLINE_NUM"+"\t"+"End of Line"+"\n")

nonval=nonTargeted.readlines()
newkey = {}
nontarget_start = {}
nontarget_end = {}

for mus in nonval:
    mus=mus.rstrip().split('\t')
    if mus[0].startswith("projectid"):
        for sec in range(0,len(mus)):
            if mus[sec]=="Subject":
                subject=sec
            elif mus[sec]=="RecordActive":
                active=sec
            elif mus[sec]=="CMTRT":
                cmtrt=sec
            elif mus[sec]=="CMENDAT_RAW":
                date_end=sec
            elif mus[sec]=="CMDOSRGM":
                ree=sec
            elif mus[sec]=="CMCAT":
                cmcat=sec
            elif mus[sec]=="RecordPosition":
                rec=sec
            elif mus[sec]=="RGMENDAT_RAW":
                rgm=sec
            elif mus[sec]=="CMDOSFRQ":
                frq=sec
            elif mus[sec]=="CMDSTXT":
                dos=sec
            elif mus[sec]=="CMDOSU":
                dosU=sec
            elif mus[sec]=="BESTRESP":
                resp=sec
            else:
                if mus[sec]=="CMSTDAT_RAW":
                    date_start=sec
    else:
        if mus[active] == "0":
            continue
        else:
            match = mus[subject]
            ff = mus[6]
            dash = ff.split("-")
            if dash[1] >= '0250':
                # print(mus[subject]+"\t"+mus[cmcat]+"\t"+"Enrollment date"+"\t"+mus[date_start]+"\t"+mus[cmtrt]+"\t"+mus[date_end]+"\t"+mus[rgm]+"\t"+mus[frq]+"\t"+"NA"+"\t"+mus[dos]+"\t"+mus[dosU]+"\t"+mus[resp]+"\t"+mus[rec]+"\n")
                nonTargetFinal.write(mus[subject]+"\t"+mus[cmcat]+"\t"+"Enrollment date"+"\t"+mus[date_start]+"\t"+mus[cmtrt]+"\t"+mus[date_end]+"\t"+mus[rgm]+"\t"+mus[frq]+"\t"+mus[ree]+"\t"+mus[dos]+"\t"+mus[dosU]+"\t"+mus[resp]+"\t"+mus[rec]+"\t"+"aa"+"\n")


previousTarget=open("Non-Targeted Therapy.txt",'r')
pre=previousTarget.readlines()
tarDict={}
for line in pre:
    line=line.rstrip().split("\t")
    if line[0].startswith("Subject"):
        for nos in range(0,len(line)):
            if line[nos]=="Subject":
                sub=nos
            elif line[nos]=="CAT_THERAPY":
                catN=nos
            elif line[nos]=="Enrollment Date":
                enroll=nos
            elif line[nos]=="THERAPY_START_DATE_DOSE":
                start=nos
            elif line[nos]=="THERAPY":
                therapy=nos
            elif line[nos]=="INTENDED_DOSE_REGIMEN":
                int=nos
            elif line[nos]=="THERAPY_END_DATE_LAST_DOSE":
                last=nos
            elif line[nos]=="THERAPY_END_DATE_REGIMEN":
                lastReg=nos
            elif line[nos]=="FREQUENCY":
                frqN=nos
            elif line[nos]=="DOSE":
                dosN=nos
            elif line[nos]=="DOSE_UNIT":
                dosuN=nos
            elif line[nos]=="BESTRESBEST_OVERALL_RESPONSEP":
                respN=nos
            elif line[nos]=="End of Line":
                end=nos
            elif line[nos]=="Disease Term (MedDRA)":
                dis=nos
            else:
                if line[nos]=="LOGLINE_NUM":
                    log=nos
    else:
        print(line[sub]+"\t"+line[dis]+"\t"+line[catN]+"\t"+line[enroll]+"\t"+line[start]+"\t"+line[therapy]+"\t"+line[last]+"\t"+line[lastReg]+"\t"+line[frqN]+"\t"+"NA"+"\t"+line[dosN]+"\t"+line[dosuN]+"\t"+line[respN]+"\t"+line[log]+"\t"+line[end]+"\n")
        nonTargetFinal.write(line[sub]+"\t"+line[catN]+"\t"+line[enroll]+"\t"+line[start]+"\t"+line[therapy]+"\t"+line[last]+"\t"+line[lastReg]+"\t"+line[frqN]+"\t"+line[int]+"\t"+line[dosN]+"\t"+line[dosuN]+"\t"+line[respN]+"\t"+line[log]+"\t"+line[end]+"\n")