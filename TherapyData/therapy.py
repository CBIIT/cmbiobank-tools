import os,csv
import numpy as np
from dateutil import parser


os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
ther=open("nontargeted_data.txt",'r')
output=open("TherapyData1.txt",'w')
output.write("Subject"+"\t"+"Enrollment Date"+"\t"+"Targeted Therapy"+"\t"+"Targeted Therapy Start Date"+"\t"+"Targeted Therapy End Date"+"\t"+"Calculated Targeted End Date"+"\t"+"Non Targeted Therapy"+"\t"+"Non Targeted Start Date"+"\t"+"Non Targeted End Date"+"\t"+"End of Line"+"\t"+"Calculated Non targeted End Date"+"\n")

def cal_comma_target(a,b):
    # print(a,b)
    cal_val = a.split(",")
    cal_list=[]
    for each in cal_val:
        if "NA" in each:
            cal_list.append("Flag")
        else:
            # print(parser.parse(each.replace('"',""))-parser.parse(line[enrollment]))
            allvalue=parser.parse(each.replace('"',""))-parser.parse(b)
            if "-" in str(allvalue):
                cal_list.append("prior"+str(allvalue).replace(" days, 0:00:00",""))
            else:
                cal_list.append(str(allvalue).replace(" days, 0:00:00","").replace("0:00:00","0"))
    return cal_list
therfh=ther.readlines()
for line in therfh:
    line=line.rstrip().split("\t")
    if line[0].startswith("Subject"):
        for i in range(0,len(line)):
            if line[i]=="Targeted Therapy End Date":
                target=i
            elif line[i]=="Enrollment Date":
                enrollment=i
            elif line[i]=="Non Targeted End Date":
                 nontarget=i
            elif line[i]=="Subject":
                 sub=i
    else:
        # print(line)
        # where both the cell values are empty
        if line[target]=="" and line[nontarget]=="":
                output.write("\t".join(line[0:5])+"\t"+"No Date"+"\t"+"\t".join(line[5:])+"\t"+"No Date"+"\n")
        # condition where target and non target have NA
        elif line[target] == "NA" and line[nontarget] == "NA":
            output.write("\t".join(line[0:5]) + "\t" + "Flag" + "\t" + "\t".join(line[5:]) + "\t" + "Flag" + "\n")



        # condition where target is single date(not NA, not empty and no comma) and non target is NA
        elif line[nontarget]=="NA" and ',' not in line[target] and 'NA' not in line[target] and line[target]!="":
            # print(line[target],"KKK",line[nontarget],line[enrollment])
            newenroll_calculation=parser.parse(line[enrollment])
            newtarget=parser.parse(line[target])
            newdate_calculation=newtarget-newenroll_calculation
            if "-" in str(newdate_calculation):
                output.write("\t".join(line[0:5]) + "\t" + "prior"+str(newdate_calculation).replace(" days, 0:00:00","") + "\t" + "\t".join(line[5:]) + "\t" + "Flag" + "\n")
            else:
                output.write("\t".join(line[0:5]) + "\t" + str(newdate_calculation).replace(" days, 0:00:00", "").replace("0:00:00","0") + "\t" + "\t".join(line[5:]) + "\t" + "Flag" + "\n")
        # condition where non target is single date(not NA, not empty and no comma) and  target is NA
        elif line[target]=="NA" and "," not in line[nontarget] and "NA" not in line[nontarget] and line[nontarget]!="":
            valEnroll=parser.parse(line[enrollment])
            valNontarget=parser.parse(line[nontarget])
            valcalculated=valNontarget-valEnroll
            if "-" in str(valcalculated):
                output.write("\t".join(line[0:5])+"\t"+"Flag"+"\t"+"\t".join(line[5:])+"\t"+"prior"+str(valcalculated).replace(" days, 0:00:00","")+"\n")
            else:
                output.write("\t".join(line[0:5])+"\t"+"Flag"+"\t"+"\t".join(line[5:])+"\t"+str(newdate_calculation).replace(" days, 0:00:00", "").replace("0:00:00","0")+"\n")

        else:
            #where target is not empty with multiple values and nontarget is empty
            if line[target]!="" and line[nontarget]=="":
                if "," in line[target]:
                    multipleval=line[target].split(",")
                    final=[]
                    for each in multipleval:
                        if "NA" in each:
                            final.append("Flag")
                        else:
                            # print(parser.parse(each.replace('"',""))-parser.parse(line[enrollment]))
                            value=parser.parse(each.replace('"',""))-parser.parse(line[enrollment])
                            if "-" in str(value):
                                final.append("prior"+str(value).replace(" days, 0:00:00",""))
                            else:
                                print(str(value))
                                final.append(str(value).replace(" days, 0:00:00","").replace("0:00:00","0"))
                    output.write("\t".join(line[0:5])+"\t"+str(final)+"\t"+"\t".join(line[5:])+"\t"+"No Date"+"\n")
                        # line.insert(5,final)

                elif "NA" in line[target]:
                    output.write("\t".join(line[0:5]) + "\t" + "Flag"+"\t"+"\t".join(line[5:])+"\t"+"No Date" + "\n")
                    # line.insert(5,"Flag")
                else:
                    enrolldate=parser.parse(line[enrollment])
                    targetadate=parser.parse(line[target])
                    a=targetadate-enrolldate
                    if "-" in str(a):
                        output.write("\t".join(line[0:5]) + "\t" +"prior"+str(a).replace(" days, 0:00:00","")+"\t"+"\t".join(line[5:])+"\t"+"No Date" + "\n")
                    else:
                        output.write("\t".join(line[0:5]) + "\t" +str(a).replace(" days, 0:00:00","").replace("0:00:00","0")+"\t"+"\t".join(line[5:])+"\t"+"No Date" + "\n")

                        #when non targeted therapy end date is not empty and with multiple values and target is empty
            elif line[nontarget] != "" and line[target] == "":
                    if "," in line[nontarget]:
                        nonmultipleval = line[nontarget].split(",")
                        nonfinal = []
                        for noneach in nonmultipleval:
                            if "NA" in noneach:
                                nonfinal.append("Flag")
                            else:
                                # print(parser.parse(each.replace('"',""))-parser.parse(line[enrollment]))
                                print(line[sub])
                                nonvalue = parser.parse(noneach.replace('"', "")) - parser.parse(line[enrollment])

                                if "-" in str(nonvalue):
                                    nonfinal.append("prior"+str(nonvalue).replace(" days, 0:00:00",""))
                                else:
                                    nonfinal.append(str(nonvalue).replace(" days, 0:00:00", "").replace("0:00:00","0"))
                        output.write("\t".join(line[0:5]) + "\t" + "No Date" + "\t" + "\t".join(line[5:]) + "\t" + str(nonfinal) + "\n")
                        # line.insert(5,final)

                    elif "NA" in line[nontarget]:
                        output.write("\t".join(line[0:5]) + "\t" + "No Date" + "\t" + "\t".join(line[5:]) + "\t" + "Flag" + "\n")
                        # line.insert(5,"Flag")
                    else:
                        enrolldate1 = parser.parse(line[enrollment])
                        nontargetadate = parser.parse(line[nontarget])
                        nona = nontargetadate - enrolldate1
                        if "-" in str(nona):
                            output.write("\t".join(line[0:5]) + "\t" + "No Date" + "\t" + "\t".join(line[5:]) + "\t" + "prior"+str(nona).replace(" days, 0:00:00","") + "\n")
                        else:
                            output.write("\t".join(line[0:5]) + "\t" + "No Date" + "\t" + "\t".join(line[5:]) + "\t" +str(nona).replace(" days, 0:00:00", "").replace("0:00:00","0")+ "\n")

            elif "," not in line[target] and "NA" not in line[target] and "," not in line[nontarget] and "NA" not in line[nontarget]:
                    allenrolldate_single = parser.parse(line[enrollment])
                    allnontargetadate_single = parser.parse(line[nontarget])
                    alltarget_single=parser.parse(line[target])
                    nontarget_single = allnontargetadate_single - allenrolldate_single
                    target_date=alltarget_single-allenrolldate_single
                    if "-" in str(nontarget_single):
                        final_single="prior"+str(nontarget_single).replace(" days, 0:00:00","")
                    else:
                        final_single=str(nontarget_single).replace(" days, 0:00:00", "").replace("0:00:00","0")
                    if "-" in str(target_date):
                        final_single_target = "prior"+str(target_date).replace(" days, 0:00:00","")
                    else:
                        final_single_target = str(target_date).replace(" days, 0:00:00", "").replace("0:00:00","0")
                    output.write("\t".join(line[0:5]) + "\t" + final_single_target + "\t" + "\t".join(line[5:]) + "\t" + final_single + "\n")
                # else:
                #     print(line[sub], line[target], line[nontarget])
            else:
                # print(line[sub], line[target], line[nontarget], "KKK")
                if "," in line[target]:
                    xy = cal_comma_target(line[target], line[enrollment])
                    # condition where we have multiple valyes in both target and non target column
                    if "," in line[nontarget]:
                        yy=cal_comma_target(line[nontarget],line[enrollment])
                        output.write("\t".join(line[0:5])+"\t"+str(xy)+"\t"+"\t".join(line[5:])+"\t"+str(yy)+"\n")
                # condition where target having multiple values and  "NA" in non target
                    elif "NA" in line[nontarget]:
                        output.write("\t".join(line[0:5])+"\t"+str(xy)+"\t"+"\t".join(line[5:])+"\t"+"Flag"+"\n")

                # condition where target is having multiple and non target having single date
                    elif "," not in line[nontarget] and "NA" not in line[nontarget]:
                        allenrolldate_comma = parser.parse(line[enrollment])
                        allnontargetadate_comma=parser.parse(line[nontarget])
                        nontarget_val=allnontargetadate_comma-allenrolldate_comma
                        if "-" in str(nontarget_val):
                            output.write("\t".join(line[0:5]) + "\t" +str(xy)+"\t"+"\t".join(line[5:])+"\t"+"prior"+str(nontarget_val).replace(" days, 0:00:00","") + "\n")
                        else:
                            output.write("\t".join(line[0:5]) + "\t" +str(xy)+"\t"+"\t".join(line[5:])+"\t"+str(nontarget_val).replace(" days, 0:00:00","").replace("0:00:00","0") + "\n")
                # condition where target is single date and non target is having multiple values
                else:
                    if "," in line[nontarget]:
                        # print(line[nontarget], line[target])
                        non_comma = cal_comma_target(line[nontarget], line[enrollment])
                        if "," not in line[target] and "NA" not in line[target]:
                            # print(line[target], line[nontarget])

                            new_comma = parser.parse(line[enrollment])
                            newtarget_comma = parser.parse(line[target])
                            new_val = newtarget_comma - new_comma
                            if "-" in str(new_val):
                                output.write("\t".join(line[0:5]) + "\t" + "prior"+str(new_val).replace(" days, 0:00:00","") + "\t" + "\t".join(line[5:]) + "\t" + str(non_comma) + "\n")
                            else:
                                 output.write("\t".join(line[0:5]) + "\t" + str(new_val).replace(" days, 0:00:00", "").replace("0:00:00","0") + "\t" + "\t".join(line[5:]) + "\t" + str(non_comma) + "\n")
                        elif "NA" in line[target]:
                            output.write("\t".join(line[0:5])+"\t"+"Flag"+"\t"+"\t".join(line[5:])+"\t"+str(non_comma)+"\n")

