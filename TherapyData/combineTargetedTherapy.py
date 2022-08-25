import os
# code to add the targeted therapy to the Therapy code file
os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
ther=open("targeted_therapy_administration.csv",'r')
outputfinal=open("FinalList.txt",'w')
outputfinal.write("Subject"+"\t"+"Enrollment Date"+"\t"+"Targeted Therapy"+"\t"+"Targeted Therapy Start Date"+"\t"+"Targeted Therapy End Date"+"\t"+"Non Targeted Therapy"+"\t"+"Non Targeted Start Date"+"\t"+"Non Targeted End Date"+"\t"+"End of Line"+"\n")


therapydict={}
startdict={}
enddict={}

for i in ther:
    ii=i.rstrip().split(",")
    if ii[0].startswith("projectid"):
        for line in range(0,len(ii)):
            if ii[line]=="Subject":
                sub=line
            elif ii[line]=="CMTRT_DSL":
                therapy=line
            elif ii[line]=="CMSTDAT_RAW":
                therapy_start=line
            elif ii[line]=="CMENDAT_RAW":
                therapy_end=line
            else:
                if ii[line]=="RecordActive":
                    rec=line
    else:
        if ii[rec]=="0"or ii[therapy]=="":
            continue
        else:
            start=0
            end=0
            item=ii[sub]
            if ii[therapy_start]=="":
                start="NA"
            else:
                start=ii[therapy_start]
            if ii[therapy_end]=="":
                end="NA"
            else:
                end=ii[therapy_end]

            if item in therapydict:
                therapydict[item].append(ii[therapy])
                startdict[item].append(start)
                enddict[item].append(end)

            else:
                therapydict[item]=[]
                startdict[item]=[]
                enddict[item]=[]
                therapydict[item].append(ii[therapy])
                startdict[item].append(start)
                enddict[item].append(end)

# for x,y in startdict.items():
#     print(x,y)
#open the Therapy code data file match the key values and append the data to this file
data= open("Therapy code.txt",'r')
datafh=data.readlines()
lookupkey={}

for each in datafh:
    each=each.rstrip().split("\t")
    if each[0].startswith("Subject"):
        for col in range(0,len(each)):
            if each[col]=="Subject":
                sub1=col
            elif each[col]=="Targeted Therapy":
                tar_therapy=col
            elif each[col]=="Targeted Therapy Start date":
                tar_therapy_start=col

            else:
                if each[col]=="Targeted Therapy End Date":
                    tar_therapy_end=col
    else:
        term=each[sub1]
        lookupkey[term]=0
        if term in therapydict:
            checklist=[]
            if each[tar_therapy]=="":
                # print(therapydict.get(term))
                checklist.extend(therapydict.get(term))
            else:
                checklist.append(each[tar_therapy])
                checklist.extend(therapydict.get(term))

            #for adding start dates
            datestartlist=[]
            if each[tar_therapy_start]=="":
                # print(therapydict.get(term))
                datestartlist.extend(startdict.get(term))
            else:
                datestartlist.append(each[tar_therapy_start])
                datestartlist.extend(startdict.get(term))

            # for adding end dates
            datesEndlist = []
            if each[tar_therapy_end] == "":
                # print(therapydict.get(term))
                datesEndlist.extend(enddict.get(term))
            else:
                datesEndlist.append(each[tar_therapy_end])
                datesEndlist.extend(enddict.get(term))
            outputfinal.write("\t".join(each[:2])+"\t"+str(checklist)+"\t"+str(datestartlist)+"\t"+str(datesEndlist)+"\t"+"\t".join(each[5:])+"\n")

        else:
            outputfinal.write("\t".join(each[0:])+"\n")
for x,y in therapydict.items():
    if x in lookupkey:
        continue
    else:
        outputfinal.write(x+"\t"+""+"\t"+str(therapydict.get(x))+"\t"+str(startdict.get(x))+"\t"+str(enddict.get(x))+"\n")














