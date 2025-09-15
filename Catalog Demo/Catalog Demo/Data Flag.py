#Data test QC check
import os,csv,xlwt

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
merge=open("Survival-StatusOutput.txt",'r')
workbook=xlwt.Workbook()
disease=workbook.add_sheet("Site",cell_overwrite_ok=True)
disease.write(0,0,"Participant ID")
disease.write(0,1,"Primary Diagnosis (MedDRA Disease Code)")
disease.write(0,2,"Primary Disease Site")

stageSheet=workbook.add_sheet("Stage",cell_overwrite_ok=True)
stageSheet.write(0,0,"Participant ID")
stageSheet.write(0,1,"Primary Diagnosis (MedDRA Disease Code)")
stageSheet.write(0,2,"Primary Disease Site")
stageSheet.write(0,3,"Disease stage (snoMed)")


sheet=workbook.add_sheet("Timepoint", cell_overwrite_ok=True)
sheet.write(0,0,"Participant ID")
sheet.write(0,1,"Collection Timepoint")
sheet.write(0,2,"Calculated Specimen Collection Date")

time=workbook.add_sheet("Biospecimen Type", cell_overwrite_ok=True)
time.write(0,0,"Participant ID")
time.write(0,1,"Collection Timepoint")
time.write(0,2,"Biospecimen Type")
# data=open("DataFlag-Primary Disease Site.txt","w")
# data.write("Participant ID"+"\t"+"Primary Diagnosis (MedDRA Disease Code)"+"\t"+"Primary Disease Site"+"\t"+"Disease stage (snoMed)"+"\n")
mergefh=merge.readlines()

def diseaseSite():
    y=1
    for me in mergefh:
        me=me.rstrip().split("\t")
        if me[0].startswith("Participant ID"):
            for lis in range(0, len(me)):
                if me[lis] == "Participant ID":
                    Participant = lis
                elif me[lis] == "Primary Diagnosis (MedDRA Disease Code)":
                     diagnosis = lis
                elif me[lis] == "Primary Disease Site":
                     site = lis
                elif me[lis] == "Disease stage (snoMed)":
                     stage = lis

        else:
            print(me[diagnosis], me[site])
            if me[diagnosis]=="10010029 - Colorectal Carcinoma":
                aa= ["Ascending Colon", "Cecum", "Colon", "Rectum","Right Colon","Sigmoid Colon","Hepatic Flexure"]
                # dd=["Adenocarcinoma StageIV", "Adenocarcinoma Stage IVA", "Colon Carcinoma Stage IV", "Colorectal Adenocarcinoma Stage IIIB", "Colorectal Adenocarcinoma Stage IIIC", "Colorectal Adenocarcinoma Stage IV", "Colorectal Adenocarcinoma Stage IVA", "Colorectal Adenocarcinoma Stage IVB", "Mucinous Adenocarcinoma Stage IV", "Rectal Carcinoma Stage IV"]
                if me[site] in aa or "Colon" in me[site]:
                    continue
                else:
                    disease.write(y,0,me[Participant])
                    disease.write(y,1,me[diagnosis])
                    disease.write(y,2,me[site])
                    y+=1
                    # data.write((me[Participant])+"\t"+me[diagnosis]+"\t"+me[site]+"\n")

            elif me[diagnosis]=="10029514 - Lung Non-Small Cell Carcinoma":
                if "Lung" in me[site]:
                    continue
                else:
                    disease.write(y, 0, me[Participant])
                    disease.write(y, 1, me[diagnosis])
                    disease.write(y, 2, me[site])
                    y+=1


            elif me[diagnosis]=="10028566 - Plasma Cell Myeloma":
                bb = ["general", "Bone Marrow", "Humerus", "Bone"]
                if me[site] in bb:
                    continue
                else:
                    disease.write(y, 0, me[Participant])
                    disease.write(y, 1, me[diagnosis])
                    disease.write(y, 2, me[site])
                    y+=1

            elif me[diagnosis]=="10036910 - Prostate Carcinoma":
                if "Prostate" in me[site]:
                    continue
                else:
                    disease.write(y, 0, me[Participant])
                    disease.write(y, 1, me[diagnosis])
                    disease.write(y, 2, me[site])
                    y+=1


            elif me[diagnosis]=="10041071 - Lung Small Cell Carcinoma":
                cc = ["Lung", "Hilar"]
                if me[site] in cc or "Lung" in me[site]:
                    continue
                else:
                    disease.write(y, 0, me[Participant])
                    disease.write(y, 1, me[diagnosis])
                    disease.write(y, 2, me[site])
                    y+=1


            elif me[diagnosis]=="10066354 - Gastroesophageal Junction Adenocarcinoma":
                if "Stomach" in me[site]:
                    continue
                else:
                    disease.write(y, 0, me[Participant])
                    disease.write(y, 1, me[diagnosis])
                    disease.write(y, 2, me[site])
                    y+=1


            elif me[diagnosis]=="10000884-Acute Myeloid Leukemia Not Otherwise Specified":
                kk=["Bone Marrow"]
                if me[site] in kk:
                    continue
                else:
                    disease.write(y, 0, me[Participant])
                    disease.write(y, 1, me[diagnosis])
                    disease.write(y, 2, me[site])
                    y +=1
workbook.save('dataFlag.xls')



# Primary diagnosis and Disease Stage

def diseaseStage():
    d=1
    for me in mergefh:
        me = me.rstrip().split("\t")
        if me[0].startswith("Participant ID"):
            for lis in range(0, len(me)):
                if me[lis] == "Participant ID":
                    Participant = lis
                elif me[lis] == "Primary Diagnosis (MedDRA Disease Code)":
                    diagnosis = lis
                elif me[lis] == "Primary Disease Site":
                    site = lis
                elif me[lis] == "Disease stage (snoMed)":
                    stage = lis

        else:
            if me[diagnosis] == "10010029 - Colorectal Carcinoma":
                dd=["Adenocarcinoma StageIV", "Adenocarcinoma Stage IVA", "Colon Carcinoma Stage IV", "Colorectal Adenocarcinoma Stage IIIB", "Colorectal Adenocarcinoma Stage IIIC", "Colorectal Adenocarcinoma Stage IV", "Colorectal Adenocarcinoma Stage IVA", "Colorectal Adenocarcinoma Stage IVB", "Mucinous Adenocarcinoma Stage IV", "Rectal Carcinoma Stage IV"]
                if me[stage] in dd:
                    continue
                else:
                    stageSheet.write(d,0,me[Participant])
                    stageSheet.write(d,1,me[diagnosis])
                    stageSheet.write(d,2,me[site])
                    stageSheet.write(d,3,me[stage])
                    d+=1

            elif me[diagnosis]=="10028566 - Plasma Cell Myeloma":
                ee = ["Plasma Cell Myeloma StageIII", "Multiple myeloma StageIII"]
                if me[stage] in ee:
                    continue
                else:
                    stageSheet.write(d, 0, me[Participant])
                    stageSheet.write(d, 1, me[diagnosis])
                    stageSheet.write(d, 2, me[site])
                    stageSheet.write(d, 3, me[stage])
                    d+=1

            elif me[diagnosis]=="10029514 - Lung Non-Small Cell Carcinoma":
                ff = ["Non-Small Cell Lung Carcinoma StageIIIA", "Non-Small Cell Lung Carcinoma StageIVB", "Non-Small Cell Lung Carcinoma StageIVC", "Non-Small Cell Lung Carcinoma StageV", "Lung adenocarcinoma StageIIIB"]
                if me[stage] in ff:
                    continue
                else:
                    stageSheet.write(d, 0, me[Participant])
                    stageSheet.write(d, 1, me[diagnosis])
                    stageSheet.write(d, 2, me[site])
                    stageSheet.write(d, 3, me[stage])
                    d+=1

            elif me[diagnosis]=="10036910 - Prostate Carcinoma":
                gg = ["Prostate Adenocarcinoma StageIV", "Adenocarcinoma StageIV"]
                if me[stage] in gg:
                    continue
                else:
                    stageSheet.write(d, 0, me[Participant])
                    stageSheet.write(d, 1, me[diagnosis])
                    stageSheet.write(d, 2, me[site])
                    stageSheet.write(d, 3, me[stage])
                    d+=1

            elif me[diagnosis]=="10041071 - Lung Small Cell Carcinoma":
                hh = ["Small Cell Carcinoma StageIV", "Small Cell Lung Carcinoma StageIV"]
                if me[stage] in hh:
                    continue
                else:
                    stageSheet.write(d, 0, me[Participant])
                    stageSheet.write(d, 1, me[diagnosis])
                    stageSheet.write(d, 2, me[site])
                    stageSheet.write(d, 3, me[stage])
                    d+=1

            elif me[diagnosis]=="10053571 - Melanoma":
                if "Melanoma" in me[stage]:
                    continue
                else:
                    stageSheet.write(d, 0, me[Participant])
                    stageSheet.write(d, 1, me[diagnosis])
                    stageSheet.write(d, 2, me[site])
                    stageSheet.write(d, 3, me[stage])
                    d+=1

            elif me[diagnosis]=="10066354 - Gastroesophageal Junction Adenocarcinoma":
                if "Gastric" in me[stage]:
                    continue
                else:
                    stageSheet.write(d, 0, me[Participant])
                    stageSheet.write(d, 1, me[diagnosis])
                    stageSheet.write(d, 2, me[site])
                    stageSheet.write(d, 3, me[stage])
                    d+=1

            elif me[diagnosis]=="10000884-Acute Myeloid Leukemia Not Otherwise Specified":
                jj=["z"]
                if me[stage] in jj:
                    continue
                else:
                    # print(me[Participant],me[diagnosis],me[stage])
                    stageSheet.write(d, 0, me[Participant])
                    stageSheet.write(d, 1, me[diagnosis])
                    stageSheet.write(d, 2, me[site])
                    stageSheet.write(d, 3, me[stage])
                    d+=1
workbook.save('dataFlag.xls')


# Collection Timepoint vs. Collection Day
def timepoint():
    r=1
    for me in mergefh:
        me = me.rstrip().split("\t")
        if me[0].startswith("Participant ID"):
            for lis in range(0, len(me)):
                if me[lis] == "Participant ID":
                    Participant = lis
                elif me[lis] == "Collection Timepoint":
                    collection = lis
                elif me[lis] == "Calculated Specimen Collection Date":
                    cal = lis

        else:
            if me[collection] == "ARCHIVAL":
                if "-" in me[cal] :
                    continue
                else:
                    sheet.write(r, 0, me[Participant])
                    sheet.write(r, 1, me[collection])
                    sheet.write(r, 2, me[cal])
                    # print(me[Participant],me[collection],me[cal])

            elif me[collection]== "ON TREATMENT" or me[collection]=="BASELINE" or me[collection]=="PROGRESSION":
                if "-" not in me[cal]:
                    continue
                else:
                    sheet.write(r,0,me[Participant])
                    sheet.write(r,1,me[collection])
                    sheet.write(r,2,me[cal])
            r += 1
            workbook.save('dataFlag.xls')

            # print(me[Participant],me[collection],me[cal])

#checking for Collection Timepoint compared to Biospecimen Type
def collection():
    bioT=1
    for me in mergefh:
        me = me.rstrip().split("\t")
        if me[0].startswith("Participant ID"):
            for lis in range(0, len(me)):
                if me[lis] == "Participant ID":
                    Participant = lis
                elif me[lis] == "Collection Timepoint":
                    collection = lis
                elif me[lis] == "Biospecimen Type":
                    bio = lis

        else:
            if me[collection] == "ARCHIVAL":
                if "Block" in me[bio] or "Slide" in me[bio]:
                    continue
                else:
                    time.write(bioT,0,me[Participant])
                    time.write(bioT,1,me[collection])
                    time.write(bioT,2,me[bio])

            elif me[collection] == "BASELINE" or me[collection]=="PROGRESSION":
                if "Bone" in me[bio] or "Tissue" in me[bio] or "Blood" in me[bio]:
                    continue
                else:
                    time.write(bioT, 0, me[Participant])
                    time.write(bioT, 1, me[collection])
                    time.write(bioT, 2, me[bio])
            elif me[collection]=="ON TREATMENT":
                if me[bio]== "FFPE Block":
                    time.write(bioT, 0, me[Participant])
                    time.write(bioT, 1, me[collection])
                    time.write(bioT, 2, me[bio])
                else:
                    continue

            bioT +=1
            workbook.save('dataFlag.xls')


diseaseSite()
diseaseStage()
timepoint()
collection()