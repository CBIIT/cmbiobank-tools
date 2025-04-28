import os, csv
from CatalogData import catalog

def specimen_tracking():
    os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
    shipping_enroll=open("CMB_specimen_tracking_enrollment.CSV",'r')
    specimen_trackingOutput=open("specimen_tracking_enroll_Output.txt",'w')
    specimen_trackingOutput.write("SujectID"+"\t"+"ASMTTPT"+"\t"+"TISTYP"+"\t"+"SPECID_DRV"+"\n")

    shippingfh=csv.reader(shipping_enroll)
    specimen_tracking_enroll=[]

    for i in shippingfh:
        if i[0].startswith("projectid"):
            for col in range(0, len(i)):
                if i[col] == "ASMTTPT":
                    asmttpt = col
                elif i[col] == "TISTYP":
                    tistyp = col
                elif i[col] == "SPECID_DRV":
                    specid_drv = col
                elif i[col] == "subjectId":
                    # print(line[i],i)
                    subId = col
                elif i[col] == "Subject":
                    # print(line[i], i)
                    sub = col
                elif i[col] == "siteid":
                    siteid = col
                elif i[col] == "Site":
                    Site = col
                elif i[col] == "RecordActive":
                    RecordActive = col
                elif i[col] == "project":
                    proj = col
                else:
                    if i[col] == "SiteNumber":
                        SiteNum = col
        else:
            if i[RecordActive]=="0":
                continue
            else:
                search = i[proj] + "_" + i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
                k=[search,i[asmttpt],i[tistyp],i[specid_drv]]
                specimen_tracking_enroll.append(k)

    for value, val in catalog.items():
        for doc in specimen_tracking_enroll:
            if value in doc:
                specimen_trackingOutput.write("\t".join(doc)+"\n")
                print(doc)
            else:
                continue




specimen_tracking()

