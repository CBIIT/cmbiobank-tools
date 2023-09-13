import os
# code to add the targeted therapy to the Therapy code file
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/Version 2/RAVE")
ther=open("targeted_therapy_administration.txt",'r')
outputfinal=open("FinalList.txt",'w')
outputfinal.write("Subject"+"\t"+"RecordPosition"+"\t"+"RecordId"+"\t"+"Disease Type"+"\t"+"TX_CYCLE_NUM"+"\t"+"Enrollment Date"+"\t"+"CMSTDAT"+"\t"+"CMENDAT"+"\t"+"CMTRT_DSL"+"\t"+"CMDOSTOT"+"\t"+"CMDOSU"+"\t"+"CMDOSFRM"+"\t"+"CMDOSFRQ"+"\t"+"CMROUTE"+"\t"+"CMCDUR"+"\t"+"CMCDURU"+"\t"+"End of Line"+"\n")


therapydict={}
startdict={}
enddict={}
c=0
for i in ther:
    ii=i.rstrip().split("\t")
    if ii[0].startswith("projectid"):
        for line in range(0,len(ii)):
            if ii[line]=="Subject":
                sub=line
            elif ii[line]=="CMTRT_DSL":
                therapy=line
            elif ii[line]=="RecordPosition":
                recPo=line
            elif ii[line]=="TX_CYCLE_NUM":
                cycle=line
            elif ii[line]=="CMDOSFRQ":
                frq=line
            elif ii[line]=="RecordId":
                recid=line
            elif ii[line]=="CMDOSTOT":
                dos=line
            elif ii[line]=="CMDOSU":
                unit=line
            elif ii[line]=="CMDOSFRM":
                frm=line
            elif ii[line]=="CMROUTE":
                rout=line
            elif ii[line]=="CMCDUR":
                dur=line
            elif ii[line]=="CMCDURU":
                cmc=line
            elif ii[line]=="CMSTDAT_RAW":
                therapy_start=line
            elif ii[line]=="CMENDAT_RAW":
                therapy_end=line
            else:
                if ii[line]=="RecordActive":
                    rec=line
    else:
        c+=1
        if ii[rec]=="0":
            continue
        else:
            start=0
            end=0
            if ii[therapy_start]=="":
                start="NA"
            else:
                start=ii[therapy_start]
            if ii[therapy]=="":
                tera="NA"
            else:
                tera=ii[therapy]
            if ii[therapy_end]=="":
                end="NA"
            else:
                end=ii[therapy_end]
            if ii[dos]=="":
                dosage="NA"
            else:
                dosage=ii[dos]

            item=ii[sub]+"_"+start+"_"+end+"_"+tera+"_"+dosage

            if item in therapydict:
                continue
            else:
                therapydict[item]=ii
                outputfinal.write(ii[sub]+"\t"+ii[recPo]+"\t"+ii[recid]+"\t"+"NA"+"\t"+ii[cycle]+"\t"+"NA"+"\t"+start+"\t"+end+"\t"+tera+"\t"+dosage+"\t"+ii[unit]+"\t"+ii[frm]+"\t"+ii[frq]+"\t"+ii[rout]+"\t"+ii[dur]+"\t"+ii[cmc]+"\n")


# print(c,len(therapydict))
# for x,y in therapydict.items():
#     print(x)
# open the Therapy code data file match the key values and append the data to this file
data= open("Targeted Therapy part1.txt",'r')
datafh=data.readlines()
lookupkey={}

for each in datafh:
    each=each.rstrip().split("\t")
    if each[0].startswith("Subject"):
        for col in range(0,len(each)):
            if each[col]=="Subject":
                sub1=col
            elif each[col]=="CMTRT_DSL":
                ttcmrt=col
            elif each[col]=="RecordPosition":
                ttrec=col
            elif each[col]=="TX_CYCLE_NUM":
                ttnum=col
            elif each[col]=="Enrollment Date":
                enroll=col
            elif each[col]=="CMDOSTOT":
                ttdos=col
            elif each[col]=="CMDOSU":
                ttdosu=col
            elif each[col]=="CMDOSFRM":
                ttfrm=col
            elif each[col]=="CMDOSFRQ":
                ttfrq=col
            elif each[col]=="CMROUTE":
                ttrou=col
            elif each[col]=="CMCDUR":
                ttduru=col
            elif each[col]=="CMCDUR":
                ttduru=col
            elif each[col]=="CMCDURU":
                ttcmc=col
            elif each[col]=="CMSTDAT":
                ttstart=col
            elif each[col]=="End of Line":
                eod=col

            else:
                if each[col]=="CMENDAT":
                    ttend=col
    else:
        if each[ttcmrt] == "":
            newtherapy = "NA"
        else:
            newtherapy = each[ttcmrt]
        if each[ttstart] == "":
            newstart = "NA"
        else:
            newstart = each[ttstart]
        if each[ttend] == "":
            newend = "NA"
        else:
            newend = each[ttend]
        if each[ttdos] == "":
            newdos = "NA"
        else:
            newdos = each[ttdos]


        search=each[sub1]+"_"+newstart+"_"+newend+"_"+newtherapy+"_"+newdos
        # print(search)
#         term=each[sub1]
#         lookupkey[term]=0
        if search in therapydict:
            continue
        else:
            outputfinal.write("\t".join(each)+"\n")
            # print(search, each[eod])
#             checklist=[]
#             if each[ttcmrt]=="":
#                 # print(therapydict.get(term))
#                 checklist.extend(therapydict.get(term))
#             else:
#                 checklist.append(each[ttcmrt])
#                 checklist.extend(therapydict.get(term))
#
#             #for adding start dates
#             datestartlist=[]
#             if each[ttstart]=="":
#                 # print(therapydict.get(term))
#                 datestartlist.extend(startdict.get(term))
#             else:
#                 datestartlist.append(each[ttstart])
#                 datestartlist.extend(startdict.get(term))
#
#             # for adding end dates
#             datesEndlist = []
#             if each[ttend] == "":
#                 # print(therapydict.get(term))
#                 datesEndlist.extend(enddict.get(term))
#             else:
#                 datesEndlist.append(each[ttend])
#                 datesEndlist.extend(enddict.get(term))
#             outputfinal.write("\t".join(each[:2])+"\t"+str(checklist)+"\t"+str(datestartlist)+"\t"+str(datesEndlist)+"\t"+"\t".join(each[5:])+"\n")
#
#         else:
#             outputfinal.write("\t".join(each[0:])+"\n")
# for x,y in therapydict.items():
#     if x in lookupkey:
#         continue
#     else:
#         outputfinal.write(x+"\t"+""+"\t"+str(therapydict.get(x))+"\t"+str(startdict.get(x))+"\t"+str(enddict.get(x))+"\n")














