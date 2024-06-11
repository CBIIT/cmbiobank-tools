import os,csv,re

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-1/RAVE")
Envio = open("CMB_social_and_environmental_factors.CSV", 'r')
final = open("Final.txt", 'w')
Enviofh = csv.reader(Envio)
SocialDict={}
for i in Enviofh:
    if i[0].startswith("projectid"):
        for col in range(0,len(i)):
            if i[col]=="Subject":
                sub=col
            elif i[col]=="SMOKING_SUNCF":
                SMOKING_SUNCF=col
            elif i[col]=="SMOKE_SUSTAGE":
                SMOKE_SUSTAGE=col
            elif i[col] == "SMOKE_SUENAGE":
                SMOKE_SUENAGE = col
            elif i[col] == "SMOK_PK_YR_NUM":
                SMOK_PK_YR_NUM = col
            elif i[col] == "SMOKE_SUDOSE":
                SMOKE_SUDOSE = col
            elif i[col] == "SMOKE_SUDUR":
                SMOKE_SUDUR = col
            elif i[col] == "SECHAND_SUOCCUR":
                SECHAND_SUOCCUR = col
            elif i[col] == "SU_SUSCAT_SPD_SECHAND":
                SU_SUSCAT_SPD_SECHAND = col
            elif i[col] == "ALCOHOL_SUNCF":
                ALCOHOL_SUNCF = col
            elif i[col] == "ALCOHOL_SUDUR":
                ALCOHOL_SUDUR = col
            elif i[col] == "EROCCUR":
                EROCCUR = col
            elif i[col] == "EMPJOB_SCORRES":
                EMPJOB_SCORRES = col
            elif i[col] == "INCMLVL_SCORRES":
                INCMLVL_SCORRES = col
            elif i[col] == "ERTERM01":
                ERTERM01 = col
            elif i[col] == "ERTERM02":
                ERTERM02 = col
            elif i[col] == "ERTERM03":
                ERTERM03 = col
            elif i[col] == "ERTERM04":
                ERTERM04 = col
            elif i[col] == "ERTERM05":
                ERTERM05 = col
            elif i[col] == "RecordActive":
                RecordActive = col
            elif i[col] == "EDULVL_SCORRES":
                EDULVL_SCORRES = col

    else:
        if i[RecordActive]=='0':
            continue
        else:
            hh=[i[sub],i[SMOKING_SUNCF],i[SMOKE_SUSTAGE],i[SMOKE_SUENAGE],i[SMOK_PK_YR_NUM],i[SMOKE_SUDOSE],i[SMOKE_SUDUR],i[SECHAND_SUOCCUR],i[SU_SUSCAT_SPD_SECHAND],i[ALCOHOL_SUNCF],i[ALCOHOL_SUDUR],i[EROCCUR],i[ERTERM01],i[ERTERM02],i[ERTERM03],i[ERTERM04],i[ERTERM05],i[EMPJOB_SCORRES],i[INCMLVL_SCORRES],i[EDULVL_SCORRES]]
            regex = re.compile('[Äôs]')
            if (regex.search(str(hh)) == None):
                print("String is accepted")

            else:
                rep=[]
                for sec in hh:
                        sec.replace('Äôs','s')
                        rep.append(sec)

                final.write("\t".join(rep)+"\n")

                # print("String resolved.")
