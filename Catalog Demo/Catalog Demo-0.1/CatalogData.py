import os,csv
from dateutil import parser

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
file=open("CMB_enrollment.CSV",'r')
fh=file.readlines()
catalog={}
bio={}
interv={}

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
                elif line[i] == "DSSTDAT_ENROLLMENT_RAW":
                     enrolldate=i
                elif line[i] == "BRTHDAT_RAW":
                     dob=i
                elif line[i] == "MHDSXCD":
                    Dcode = i
                elif line[i] == "ETHNIC":
                    ethnic = i
                elif line[i] == "SEX":
                    sex = i
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
                elif line[i] == "RecordActive":
                    RecordActive = i
                elif line[i] == "MHLOC":
                    MHLOC = i
                else:
                    if line[i] == "SiteNumber":
                        # print(line[i], i)
                        SiteNum = i
        else:
            if line[RecordActive]=="0":
                continue
            else:
                # print(line[project],line[subId],line[sub],line[siteid],line[Site],line[SiteNum])
                search=line[project]+"_"+line[subId]+"_"+line[sub]+"_"+line[siteid]+"_"+line[Site]+"_"+line[SiteNum]
                if search in catalog:
                    print("!!!!!!!!!!Warning key found multiple times!!!!!!!!!!")
                else:
                    catalog[search]=[]
                    k=parser.parse(line[dob])
                    m=parser.parse(line[enrolldate])
                    a=k-m
                    cal=(str(a).split(" ")[0])
                    add=[line[age],line[dob],line[enrolldate],cal,line[Dcode],line[ethnic],line[sex],line[race1],line[race2],line[race3],line[race4],line[race5],line[race6],line[race7],line[MHLOC]]
                    catalog[search].extend(add)


def biopsy_pat():
    bfile=open("CMB_biopsy_pathology_verification_and_assessment.csv",'r')
    output1 = open("biopsyOut.txt", 'w')
    output1.write("project"+"\t"+"SubjectId"+"\t"+"Subject"+"\t"+"SiteId"+"\t"+"Site"+"\t"+"SiteNumber"+"\t"+"MILOC"+"\t"+"MIORRES_TUCONT_X1"+"\t"+"MIORRES_TUCONT_X2"+"\n")
    fhb=csv.reader(bfile)
    pathology={}
    for dat in fhb:
        # dat=dat.rstrip().split(",")
        if dat[0].startswith("projectid"):
            for x in range(0,len(dat)):
                if dat[x]=="MILOC":
                    miloc= x
                elif dat[x] =="MIORRES_TUCONT_X1":
                    tumcon1=x
                elif dat[x]=="subjectId":
                    # print(line[i],i)
                    subId=x
                elif dat[x] == "Subject":
                     # print(line[i], i)
                     sub=x
                elif dat[x] == "siteid":
                     siteid=x
                elif dat[x] == "Site":
                     Site=x
                elif dat[x] =="project":
                     proj=x
                elif dat[x] =="RecordActive":
                     RecordActive=x
                elif dat[x]=="SiteNumber":
                     SiteNum=x
                else:
                    if dat[x] =="MIORRES_TUCONT_X2":
                        tumcon2=x
        else:
            if dat[RecordActive]=="0":
                continue
            else:
                # print(line[project],line[subId],line[sub],line[siteid],line[Site],line[SiteNum])
                search1=dat[proj]+"_"+dat[subId]+"_"+dat[sub]+"_"+dat[siteid]+"_"+dat[Site]+"_"+dat[SiteNum]
                val1=dat[miloc]+"_"+dat[tumcon1]+"_"+dat[tumcon2]
                # val1=dat[miloc],dat[tumcon1],dat[tumcon2]

                if search1 in pathology:
                    if val1==pathology.get(search1):
                        continue
                    else:
                        pathology[search1].append(val1)
                        print("ERRRROOOOORRRRRRRRRR")
                        print(search1,val1)
                        # output1.write(dat[proj]+"\t"+dat[subId]+"\t"+dat[sub]+"\t"+dat[siteid]+"\t"+dat[Site]+"\t"+dat[SiteNum]+"\t"+dat[miloc]+"\t"
                        #               +dat[tumcon1]+"\t"+dat[tumcon2]+"\n")
                else:
                    pathology[search1]=[]
                    pathology[search1].append(val1)
            for i,j in pathology.items():
                output1.write("\t".join(i.split("_"))+"\t"+j+"\n")
                    # print(i,j)

            # print(dat[proj]+"\t"+dat[subId]+"\t"+dat[sub]+"\t"+dat[siteid]+"\t"+dat[Site]+"\t"+dat[SiteNum]+"\t"+dat[miloc]+"\t"+
            #               tumcon1,tumcon2,dat[tumcon1]+"\t"+dat[tumcon2])
            # print(len(dat),"\t",dat)
            # print(dat[tumcon1],tumcon1,dat[tumcon2],tumcon2)
            # if search1 in catalog:
            #     k=[dat[miloc],dat[tumcon1],dat[tumcon2]]
            #     catalog[search1].append(k)
            #
            # else:
            #     print(search1+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!search1 not present")
def intervening():
    file3=open("CMB_intervening_therapy.CSV",'r')
    output_interv=open("InterveningOut.txt",'w')
    output_interv.write("SubjectID" + "\t" + "AGE"+"\t"+"BirthDate"+"\t"+"Enrollment Date"+"\t"+"Calculated Birth Date" + "\t" + "Disease Code" + "\t" + "Ethnicity" + "\t" + "SEX" + "\t" + "Gender" + "\t" + "Race1" + "\t"
                        + "Race2"+ "\t" + "Race3"+ "\t" + "Race4"+ "\t" + "Race5"+ "\t" + "Race6"+ "\t" + "Race7"  + "\t" +"Primary Disease Site"+"\t"+ "Therapy Category" + "\t" +
              "Response Assessment"+"\t"+"Intervening Therapies"+"\t"+"Oncomine Results Available"+"\n")
    inte=[]
    fileread=csv.reader(file3)
    for item in fileread:
        if item[0].startswith("projectid"):
            for col in range(0,len(item)):
                if item[col]=="BESTRESP":
                    bresp=col
                elif item[col]=="CMCAT":
                    cmcat= col
                elif item[col]=="CMTRT":
                    cmtrt= col
                elif item[col]=="subjectId":
                    # print(line[i],i)
                    subId=col
                elif item[col] == "Subject":
                     # print(line[i], i)
                     sub=col
                elif item[col] == "siteid":
                     siteid=col
                elif item[col] == "Site":
                     Site=col
                elif item[col] == "RecordActive":
                     RecordActive=col
                elif item[col] =="project":
                     proj=col
                else:
                    if item[col]=="SiteNumber":
                     SiteNum=col
        else:
            if item[RecordActive]=="0":
                continue
            else:
                search2=item[proj]+"_"+item[subId]+"_"+item[sub]+"_"+item[siteid]+"_"+item[Site]+"_"+item[SiteNum]
                l=[search2,item[cmcat],item[bresp],item[cmtrt]]
                inte.append(l)
    # print(inte)
    for i,j in catalog.items():
        newlist=[x[0] for x in inte]
        if i in newlist:
            for y in inte:
                if i in y[0]:
                    output_interv.write(i+"\t"+"\t".join(j)+"\t"+"\t".join(y[1:])+"\n")
        else:
            output_interv.write(i+"\t"+"\t".join(j)+"\t"+" "+"\t"+" "+"\t"+" "+"\n")
def oncomine():
    oncofile=open("CMB_oncomine_result.CSV",'r')
    oncofile_output=open("oncooutput.txt",'w')
    intervenfile=open("InterveningOut.txt",'r')
    indic=[]
    onco={}
    interfh=intervenfile.readlines()

    for x in interfh:
        x=x.split("\t")
        indic.append(x)

    fhonco=csv.reader(oncofile)
    for num in fhonco:
        if num[0].startswith("projectid"):
            for col in range(0, len(num)):
                if num[col] == "PFORRES_SPD":
                    PFORRES_SPD = col
                elif num[col] == "subjectId":
                    # print(line[i],i)
                    subId = col
                elif num[col] == "Subject":
                    # print(line[i], i)
                    sub = col
                elif num[col] == "siteid":
                    siteid = col
                elif num[col] == "Site":
                    Site = col
                elif num[col] == "RecordActive":
                    RecordActive = col
                elif num[col] == "project":
                    proj = col
                else:
                    if num[col] == "SiteNumber":
                        SiteNum = col
        else:
            if num[RecordActive]=="0":
                continue
            else:
                if num[PFORRES_SPD]=="Pass":
                    search3=num[proj]+"_"+num[subId]+"_"+num[sub]+"_"+num[siteid]+"_"+num[Site]+"_"+num[SiteNum]
                    # print(search3)
                    onco[search3]=num[PFORRES_SPD]
    for n in indic:
        print(n)
        if "\n" in n:
            n.remove('\n')
            n.append(" ")
            # print(n)
            if n[0] in onco:
                # print(ele[0])
                n.append(onco.get(n[0]))
                oncofile_output.write("\t".join(n) + "\n")
            else:
                if "SubjectID" in n[0]:
                    oncofile_output.write("\t".join(n) + "\n")
                else:
                    oncofile_output.write("\t".join(n) + "\t" + " " + "\n")
        else:
            # print(n)
            ele=list(map(lambda s: s.strip(), n))
            # print(ele)
            if ele[0] in onco:
                ele.append(onco.get(ele[0]))
                print(ele,"YeSSSSSSS")
                oncofile_output.write("\t".join(ele)+"\n")
            else:
                    if "SubjectID" in ele[0]:
                        oncofile_output.write("\t".join(ele)+"\n")
                    else:
                        oncofile_output.write("\t".join(ele)+"\t"+" "+"\n")
def social():
    socfile=open("CMB_social_and_environmental_factors.CSV",'r')
    socEnv=open("SocialEnv.txt",'w')
    socfh=csv.reader(socfile)
    oncoOutput=open("oncooutput.txt",'r')
    oncoOutfh=oncoOutput.readlines()
    onco=[]
    soc_dic={}
    for line in oncoOutfh:
        line=line.split("\t")
        onco.append(line)
    for soc in socfh:
        if soc[0].startswith("projectid"):
            for col in range(0, len(soc)):
                if soc[col] == "SMOKING_SUNCF":
                    smokSun = col
                elif soc[col] == "subjectId":
                    # print(line[i],i)
                    subId = col
                elif soc[col] == "SMOK_PK_YR_NUM":
                    # print(line[i],i)
                    smokeYr = col
                elif soc[col] == "SMOKE_SUDUR":
                    # print(line[i],i)
                    smokeDur = col
                elif soc[col] == "ALCOHOL_SUNCF":
                    # print(line[i],i)
                    alcohol = col
                elif soc[col] == "EROCCUR":
                    # print(line[i],i)
                    erOccur = col
                elif soc[col] == "Subject":
                    # print(line[i], i)
                    sub = col
                elif soc[col] == "siteid":
                    siteid = col
                elif soc[col] == "Site":
                    Site = col
                elif soc[col] == "RecordActive":
                    RecordActive = col
                elif soc[col] == "project":
                    proj = col
                else:
                    if soc[col] == "SiteNumber":
                        SiteNum = col
        else:
            if soc[RecordActive]=="0":
                continue
            else:
                search4=soc[proj]+"_"+soc[subId]+"_"+soc[sub]+"_"+soc[siteid]+"_"+soc[Site]+"_"+soc[SiteNum]
                soc_dic[search4]=[soc[smokSun],soc[smokeYr],soc[smokeDur],soc[alcohol],soc[erOccur]]
    for l in onco:
        nl = [x.replace("\n", "") for x in l]
        # print(nl)
        if l[0] in soc_dic:
            socEnv.write("\t".join(nl)+"\t"+"\t".join(soc_dic.get(l[0]))+"\n")
        else:
            if nl[0].startswith("SubjectID"):
                socEnv.write("\t".join(nl) + "\t" + "SMOKING_SUNCF"+"\t"+"SMOK_PK_YR_NUM" + "\t" + "SMOKE_SUDUR"+"\t"+"ALCOHOL_SUNCF"+"\t"+"EROCCUR"+"\n")
            else:
                socEnv.write("\t".join(nl) + "\t" + " "+"\t" + " " +"\t" + " "+"\t" + " "+"\t" + " " +"\n")

def courseIni():
    courseIni=open("CMB_course_initiation.CSV",'r')
    coursefh=csv.reader(courseIni)
    socOpen=open("SocialEnv.txt",'r')
    course_output=open("course_ini_output.txt",'w')
    socRe=socOpen.readlines()
    cur =[]
    evn=[]
    for ev in socRe:
        ev=ev.split("\t")
        evn.append(ev)

    for course in coursefh:
        if course[0].startswith("projectid"):
            for col in range(0, len(course)):
                if course[col] == "ECTARGET":
                    target = col
                elif course[col] == "subjectId":
                    # print(line[i],i)
                    subId = col
                elif course[col] == "ECDRGCLS":
                    # print(line[i],i)
                    drugClass = col
                elif course[col] == "Subject":
                    # print(line[i], i)
                    sub = col
                elif course[col] == "siteid":
                    siteid = col
                elif course[col] == "Site":
                    Site = col
                elif course[col] == "RecordActive":
                    RecordActive = col
                elif course[col] == "project":
                    proj = col
                else:
                    if course[col] == "SiteNumber":
                        SiteNum = col
        else:
            if course[RecordActive]=="0":
                continue
            else:
                search5=course[proj]+"_"+course[subId]+"_"+course[sub]+"_"+course[siteid]+"_"+course[Site]+"_"+course[SiteNum]
                s=[search5,course[target],course[drugClass]]
                cur.append(s)
    for item in evn:
        newlist = [x[0] for x in cur]
        if item[0] in newlist:
            for ele in cur:
                if item[0]==ele[0]:
                    # print(item,ele[1:])
                    item.append(ele[-2])
                    item.append(ele[-1])
                    # print(item)
                    final = [x.replace("\n", "") for x in item]
                    course_output.write("\t".join(final)+"\n")
                    item.pop()
                    item.pop()
        else:

            final = [x.replace("\n", "") for x in item]
            if item[0].startswith("SubjectID"):
                course_output.write("\t".join(final) + "\t" + "ECTARGET"+"\t"+"ECDRGCLS" +"\n")
            else:
                course_output.write("\t".join(final)+"\t"+" "+"\t"+ " "+"\n")

def histology():
    histo=open("CMB_histology_and_disease.CSV",'r')
    course_int=open("course_ini_output.txt",'r')
    histo_output=open("histology_output.txt",'w')
    cour=course_int.readlines()
    courlist=[]
    for i in cour:
        i=i.split("\t")
        courlist.append(i)
    histo_list=[]
    histofh=csv.reader(histo)
    for hist in histofh:
        if hist[0].startswith("projectid"):
            for col in range(0, len(hist)):
                if hist[col] == "RSORRES_DZSTAGE_STD":
                    Dstate = col
                elif hist[col] == "subjectId":
                    # print(line[i],i)
                    subId = col
                elif hist[col] == "MIORRES_X1":
                    # print(line[i],i)
                    Tumgrade = col
                elif hist[col] == "MHSTDAT_DX_RAW":
                    # print(line[i],i)
                    dat = col
                elif hist[col] == "SNOMED":
                    # print(line[i],i)
                    SNOMED = col
                elif hist[col] == "Subject":
                    # print(line[i], i)
                    sub = col
                elif hist[col] == "siteid":
                    siteid = col
                elif hist[col] == "Site":
                    Site = col
                elif hist[col] == "RecordActive":
                    RecordActive = col
                elif hist[col] == "project":
                    proj = col
                else:
                    if hist[col] == "SiteNumber":
                        SiteNum = col
        else:
            if hist[RecordActive]=="0":
                continue
            else:
                search5=hist[proj]+"_"+hist[subId]+"_"+hist[sub]+"_"+hist[siteid]+"_"+hist[Site]+"_"+hist[SiteNum]
                l=[search5,hist[Dstate],hist[Tumgrade],hist[SNOMED],hist[dat]]
                # print(l)
                final=["nan" if x =='' else x for x in l]
                # print(final)
                histo_list.append(final)
    for y in courlist:
      for sublist in histo_list:
          if y[0] == sublist[0]:
             if sublist[-2] in y:
                 if sublist[-1] in y:
                     continue
                 else:
                     y.append(sublist[-1])
             else:
              y.append(sublist[-4])
              y.append(sublist[-3])
              y.append(sublist[-2])
              y.append(sublist[-1])
      # print(y)
      outlist = [val.replace("\n", "") for val in y]
      # print(outlist)
      histo_output.write("\t".join(outlist)+"\n")

def concom_prior_med():
    concom=open("CMB_concomitant_and_prior_medications.CSV",'r')
    concomOutput=open("cocom_prior_med_Output.txt",'w')
    concomfh=csv.reader(concom)
    histology_output=open("histology_output.txt",'r')
    hhoo=[]
    conprior = {}
    histofh=histology_output.readlines()
    for hh in histofh:
        hh=hh.rstrip().split("\t")
        hhoo.append(hh)
    for x in concomfh:
        if x[0].startswith("projectid"):
            for col in range(0,len(x)):
                if x[col]=="CMTRT":
                    cmtrt=col
                elif x[col]=="subjectId":
                    # print(line[i],i)
                    subId=col
                elif x[col] == "Subject":
                     # print(line[i], i)
                     sub=col
                elif x[col] == "siteid":
                     siteid=col
                elif x[col] == "Site":
                     Site=col
                elif x[col] =="project":
                     proj=col
                else:
                    if x[col]=="SiteNumber":
                     SiteNum=col
        else:
            search6=x[proj]+"_"+x[subId]+"_"+x[sub]+"_"+x[siteid]+"_"+x[Site]+"_"+x[SiteNum]
            if search6 in conprior:
                conprior[search6].append(x[cmtrt])
            else:
                conprior[search6]=[]
                conprior[search6].append(x[cmtrt])
    for i in hhoo:
        # print(i)
        if i[0] in conprior:
            # i.append(conprior.get(i[0]))

            concomOutput.write("\t".join(i)+"\t"+str(conprior.get(i[0]))+"\n")
        else:
            if i[0].startswith("SubjectID"):
                concomOutput.write("\t".join(i)+"\t"+"RSORRES_DZSTAGE_STD"+"\t"+"MIORRES_X1"+"\t"+"CMTRT-concomitant and prior_med"+"\n")
            else:
                concomOutput.write("\t".join(i)+"\t"+" "+"\n")



enroll()
# biopsy_pat()
# intervening()
# oncomine()
# social()
# courseIni()
# histology()
# concom_prior_med()

# output=open("enrolloutput.txt",'w')
# output.write("SubjectID"+"\t"+"Age at Diagnosis"+"\t"+"BirthDate"+"\t"+"Enrollment Date"+"\t"+"Calculated Birth Date"+"\t"+"SnoMed Code"+"\t"+"Ethnicity"+"\t"+"SEX"+"\t"+"Race1"+"\t"+"Race2"+"\t"+"Race3"
#              +"\t"+"Race4"+"\t"+"Race5"+"\t"+"Race6"+"\t"+"Race7"+"\t"+"Primary Disease Site"+"\t"+"Treatment Response"+"\t"+"Therapy Category"+"\n")
#
# #     # print(i,j)
# for i, j in catalog.items():
#     output.write(i+"\t"+"\t".join(j)+"\n")
#     print(i,j)

