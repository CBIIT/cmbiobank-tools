import os,csv
from CatalogData import catalog

#script will read the prior treatment form

def prior_treatment():
    os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
    file=open("CMB_prior__treatment_summary.CSV",'r')
    prio_treatment_Out=open("prior_treatment_Output.txt",'w')
    fh=csv.reader(file)
    prior_dic=[]

    for i in fh:
        if i[0].startswith("projectid"):
            for col in range(0, len(i)):
                if i[col] == "CMTRT_PRIORTRT":
                    cmtrt_prio = col
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
                elif i[col] == "project":
                    proj = col
                else:
                    if i[col] == "SiteNumber":
                        SiteNum = col
        else:
            search= i[proj] + "_" + i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
            k=[search,i[cmtrt_prio]]
            prior_dic.append(k)
    for a, b in catalog.items():
        for d in prior_dic:
            if a in d:
                prio_treatment_Out.write("\t".join(d)+"\n")
                print(d)
        else:
            continue

prior_treatment()