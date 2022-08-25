# open non targeted therapy data and add the values from 102 patient
import os

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
nonTargeted=open("prior__therapy_supplement.txt",'r')
nonTargetFinal=open("nontargeted_data.txt",'w')
nonTargetFinal.write("Subject"+"\t"+"Enrollment Date"+"\t"+"Targeted Therapy"+"\t"+"Targeted Therapy Start Date"+"\t"+"Targeted Therapy End Date"+"\t"+"Non Targeted Therapy"+"\t"+"Non Targeted Start Date"+"\t"+"Non Targeted End Date"+"\t"+"End of Line"+"\n")

nonval=nonTargeted.readlines()
newkey = {}
nontarget_start = {}
nontarget_end = {}
for mus in nonval:
    mus=mus.rstrip().split("\t")
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
            else:
                if mus[sec]=="CMSTDAT_RAW":
                    date_start=sec
    else:
        if mus[active]=="0":
            continue
        else:
            match=mus[subject]
            ff=mus[6]
            dash=ff.split("-")
            if dash[1]>='0102':
                # print(mus[cmtrt])
                if match in newkey:
                    newkey[match].append(mus[cmtrt])
                    nontarget_start[match].append(mus[date_start])
                    nontarget_end[match].append(mus[date_end])
                else:
                    newkey[match]=[]
                    nontarget_start[match]=[]
                    nontarget_end[match]=[]
                    newkey[match].append(mus[cmtrt])
                    nontarget_start[match].append(mus[date_start])
                    nontarget_end[match].append(mus[date_end])

#
# for x,y in newkey.items():
    # print(x,y)
previousTarget=open("FinalList.txt",'r')
pre=previousTarget.readlines()
tarDict={}
for line in pre:
    line=line.rstrip().split("\t")
    if line[0].startswith("Subject"):
        for nos in range(0,len(line)):
            if line[nos]=="Subject":
                sub=nos
            elif line[nos]=="Non Targeted Therapy":
                nontar_val=nos
            elif line[nos]=="Non Targeted Start Date":
                nontar_start=nos
            else:
                if line[nos]=="Non Targeted End Date":
                    nontar_end=nos

    else:
        tarDict[line[sub]]=0
        if line[sub].rstrip().split("-")[1]>='0102':
            # print(line[sub])
            if line[sub].rstrip() in newkey:
                nonTargetFinal.write("\t".join(line[0:5])+"\t"+str(newkey.get(line[sub]))+"\t"+str(nontarget_start.get(line[sub]))+"\t"+str(nontarget_end.get(line[sub]))+"\n")
            else:
                nonTargetFinal.write("\t".join(line) + "\n")
        else:
            nonTargetFinal.write("\t".join(line)+"\n")

for m,n in newkey.items():
    if m in tarDict:
        continue
    else:
        nonTargetFinal.write(m+"\t"+""+"\t"+""+"\t"+""+"\t"+""+"\t"+str(n)+"\t"+str(nontarget_start.get(m))+"\t"+str(nontarget_end.get(m))+"\n")
        print(m,n)




