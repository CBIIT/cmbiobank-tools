import os,csv

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE/DME_Download/VCF")
os.system("mkdir -p VCF_Report")
pp=open("Patient Eligibility.csv",'r')
fh=csv.reader(pp)
vv=[]

for i in fh:
    if "SUBJECT_ID" in i:
        continue
    else:
        vv.append(i[0])

for file in os.listdir():
    if "(" in file:
        filerename=file.replace("(","\(").replace(")","\)")
        fileh = file.rstrip().split("_")
        fileh[0] = fileh[0][:-3]
        if fileh[0] in vv:
            print(file)
            os.system('cp /Users/mohandasa2/Desktop/dbGap\ Data/Submission-V3/RAVE/DME_Download/VCF/' + filerename + ' /Users/mohandasa2/Desktop/dbGap\ Data/Submission-V3/RAVE/DME_Download/VCF/VCF_Report/')
    else:
        fileh=file.rstrip().split("_")
        fileh[0]=fileh[0][:-3]
        if fileh[0] in vv:
            print(file)
            os.system('cp /Users/mohandasa2/Desktop/dbGap\ Data/Submission-V3/RAVE/DME_Download/VCF/'+ file+ ' /Users/mohandasa2/Desktop/dbGap\ Data/Submission-V3/RAVE/DME_Download/VCF/VCF_Report/')
    #
    #     print(file[0])