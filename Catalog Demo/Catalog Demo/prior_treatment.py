import os,csv
from CatalogData import catalog

#script will read the prior treatment form

def prior_treatment():
    os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
    file=open("prior__treatment_summary.CSV",'r')
    prio_treatment_Out=open("prior_treatment_Output.txt",'w')
    fh=csv.reader(file)
    prior_dic=[]
    Dict={}

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
                elif i[col] == "CMOCCUR":
                    CMOCCUR = col
                elif i[col] == "Site":
                    Site = col
                elif i[col] == "project":
                    proj = col
                else:
                    if i[col] == "SiteNumber":
                        SiteNum = col
        else:
            if i[CMOCCUR]=="Yes":
                search= i[proj] + "_" + i[subId] + "_" + i[sub] + "_" + i[siteid] + "_" + i[Site] + "_" + i[SiteNum]
                k = [search, i[cmtrt_prio]]
                prior_dic.append(k)
                if search in Dict:
                    Dict[search].append(i[cmtrt_prio])
                else:
                    Dict[search]=[]
                    Dict[search].append(i[cmtrt_prio])
    for k,l in Dict.items():
        prio_treatment_Out.write(k+"\t"+";".join(l)+"\n")
        print(k,";".join(l))

    # for g in prior_dic:
    #     # print(g)
    #     if g[0] in Dict:
    #         prio_treatment_Out.write("\t".join(g)+"\t"+str(Dict.get(g[0]+"\n")))
    #         # print(g)

    #
    # for a, b in catalog.items():
    #     for d in prior_dic:
    #         print(d)
    #         if a in d:
    #             prio_treatment_Out.write("\t".join(d)+"\n")
    #         else:
    #             continue

prior_treatment()