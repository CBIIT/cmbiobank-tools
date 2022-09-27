import os,csv
from dateutil import parser
from datetime import date

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
file=open("enrollment.CSV",'r')
flag=open("dataFlag Disease Site","w")
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
    biofile=open("biopsy_pathology_verification_and_assessment.CSV",'r')
    BioOutput=open("BiopsyPat.txt",'w')
    Biofh=csv.reader(biofile)
    EnrollOutput=open("enrolloutput.txt",'r')
    BioRead=EnrollOutput.readlines()
    biopsy=[]
    bio_dic={}
    for line in BioRead:
        line=line.split("\t")
        biopsy.append(line)
    for soc in Biofh:
        if soc[0].startswith("projectid"):
            for col in range(0, len(soc)):
                if soc[col] == "MILOC":
                    MILOC = col
                elif soc[col] == "subjectId":
                    # print(line[i],i)
                    subId = col
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
                bio_dic[search4]=[soc[MILOC]]
    for l in biopsy:
        nl = [x.replace("\n", "") for x in l]
        # print(nl)
        if l[0] in bio_dic:
            BioOutput.write("\t".join(nl)+"\t"+"\t".join(bio_dic.get(l[0]))+"\n")
        else:
            if nl[0].startswith("SubjectID"):
                BioOutput.write("\t".join(nl) + "\t" + "Anatomic Collection Site"+"\n")
            else:
                BioOutput.write("\t".join(nl) + "\t" + " "+"\n")

def intervening():
    interveningfile = open("intervening_therapy.CSV", 'r')
    InterData = open("InterveningData.txt", 'w')
    Invfh = csv.reader(interveningfile)
    BiopsyOutput = open("enrolloutput.txt", 'r')
    Interveningfh = BiopsyOutput.readlines()
    onco = []
    inv_dic = {}
    for line in Interveningfh:
        line = line.split("\t")
        onco.append(line)
    for soc in Invfh:
        if soc[0].startswith("projectid"):
            for col in range(0, len(soc)):
                if soc[col] == "BESTRESP":
                    BESTRESP = col
                # elif soc[col] == "CMCAT":
                #     CMCAT = col
                elif soc[col] == "subjectId":
                    subId = col
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
            if soc[RecordActive] == "0":
                continue
            else:
                search4 = soc[proj] + "_" + soc[subId] + "_" + soc[sub] + "_" + soc[siteid] + "_" + soc[Site] + "_" + \
                          soc[SiteNum]
                inv_dic[search4] = [soc[BESTRESP]]
    for l in onco:
        nl = [x.replace("\n", "") for x in l]
        # print(nl)
        if l[0] in inv_dic:
            InterData.write("\t".join(nl) + "\t" + "\t".join(inv_dic.get(l[0])) + "\n")
        else:
            if nl[0].startswith("SubjectID"):
                InterData.write("\t".join(nl) + "\t" + "Treatment Response" + "\n")
            else:
                InterData.write("\t".join(nl) + "\t" + " " + "\n")

def oncomine():
    oncofile=open("oncomine_result.CSV",'r')
    oncofile_output=open("oncooutput.txt",'w')
    intervenfile=open("InterveningData.txt",'r')
    indic=[]
    onco={}
    interfh=intervenfile.readlines()

    for x in interfh:
        print(x)
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
                    y=num[PFORRES_SPD].replace("Pass","Available")
                    search3=num[proj]+"_"+num[subId]+"_"+num[sub]+"_"+num[siteid]+"_"+num[Site]+"_"+num[SiteNum]
                    # print(search3)
                    onco[search3]=y
    for n in indic:
        # print(n)
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
                        oncofile_output.write("\t".join(ele)+"\t"+"Biomarker Results"+"\n")
                    else:
                        oncofile_output.write("\t".join(ele)+"\t"+" "+"\n")
def social():
    socfile=open("social_and_environmental_factors.CSV",'r')
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
                smoke=soc[smokSun].replace("Current reformed smoker for more than 15 years","Quit > 15 yrs. ago").replace("Current smoker","Current").replace("Current reformed smoker for less than or equal to 15 years","Quit < 15 yrs. ago").replace("Lifelong non-smoker","Never").replace("Smoking history not documented","Not provided")
                alco=soc[alcohol].replace("Consumed alcohol in the past, but currently a non-drinker","Former").replace("Alcohol consumption equal to or less than 2 drinks per day for men and 1 drink or less per day for women","Moderate").replace("Alcohol consumption more  than 2 drinks per day for men and more than 1 drink per day for women","Heavy (note that Heavy is not correct term,)").replace("Lifelong non-drinker","Nondrinker").replace("Alcohol consumption history not available","Not Provided")
                soc_dic[search4]=[smoke,soc[smokeYr],soc[smokeDur],alco,soc[erOccur]]
    for l in onco:
        nl = [x.replace("\n", "") for x in l]
        # print(nl)
        if l[0] in soc_dic:
            socEnv.write("\t".join(nl)+"\t"+"\t".join(soc_dic.get(l[0]))+"\n")
        else:
            if nl[0].startswith("SubjectID"):
                socEnv.write("\t".join(nl) + "\t" + "Smoking History"+"\t"+"Smoking Pack Years" + "\t" + "Years Smoked"+"\t"+"Alcohol Consumption"+"\t"+"Carcinogen Exposure"+"\n")
            else:
                socEnv.write("\t".join(nl) + "\t" + " "+"\t" + " " +"\t" + " "+"\t" + " "+"\t" + " " +"\n")

def courseIni():
    courseIni=open("course_initiation.CSV",'r')
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
    histo=open("histology_and_disease.CSV",'r')
    course_int=open("SocialEnv.txt",'r')
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
      outlist = [val.replace("\n", "") for val in y]
      if outlist[0].startswith("SubjectID"):
          histo_output.write("\t".join(outlist) + "\t" + "Tumor Grade" + "\t" + "Disease stage (snoMed)" + "\t" + "Initial Diagnosis date" + "\n")
          continue
      else:
          # Age at Enrollement
          objBirth=parser.parse(outlist[2])
          objEnroll=parser.parse(outlist[3])
          ageD=(objEnroll-objBirth)
          val=ageD/365.25
          obj=(str(val).split(","))
          diaAge=obj[0].replace("days"," ")
          #SnoMed code
          medra=outlist[5].replace("10010029","10010029 - Colorectal Carcinoma").replace("10028566","10028566 - Plasma Cell Myeloma").replace("10029514","10029514 - Lung Non-Small Cell Carcinoma").replace("10036910","10036910 - Prostate Carcinoma").replace("10041071","10041071 - Lung Small Cell Carcinoma").replace("10053571","10053571 - Melanoma").replace("10066354","10066354 - Gastroesophageal Junction Adenocarcinoma").replace("10000884","10000884-Acute Myeloid Leukemia Not Otherwise Specified")
          stage=outlist[-2].split("=")
          #Disease stage (snoMed)
          Dstage=stage[0]+"Stage"+outlist[-4]
          # outlist.insert(1,diaAge)
          # outlist.pop(3)
          outlist.insert(5,medra)
          outlist.pop(6)
          outlist.insert(-2,Dstage)
          outlist.pop(-5)
          outlist.pop(-2)
          histo_output.write("\t".join(outlist)+"\n")

def concom_prior_med():
    concom=open("concomitant_and_prior_medications.CSV",'r')
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



# enroll()
# biopsy_pat() Do not Run
# intervening()
# oncomine()
# social()
# courseIni() Do not Run
histology()
# concom_prior_med() Do not Run



#Run while running the enrollment defination
# output=open("enrolloutput.txt",'w')
# output.write("SubjectID"+"\t"+"Age at Enrollment"+"\t"+"BirthDate"+"\t"+"Enrollment Date"+"\t"+"Calculated Birth Date"+"\t"+"Primary Diagnosis (MedDRA Disease Code)"+"\t"+"Ethnicity"+"\t"+"SEX"+"\t"+"Race1"+"\t"+"Race2"+"\t"+"Race3"
#              +"\t"+"Race4"+"\t"+"Race5"+"\t"+"Race6"+"\t"+"Race7"+"\t"+"Primary Disease Site"+"\n")
#
# #     # print(i,j)
# for i, j in catalog.items():
#     output.write(i+"\t"+"\t".join(j)+"\n")
#     print(i,j)

