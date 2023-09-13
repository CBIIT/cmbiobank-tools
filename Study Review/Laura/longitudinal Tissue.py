import os,csv

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
cour=open("data-file.txt",'r')
long=open("longitudinal samples.txt",'w')
point=open("input.txt",'r')
ph=point.readlines()

diseasename=0
timepoint=0

dict={}
# category=["Blood","Bone Marrow","Formalin Fixed Paraffin Embedded Tissue","Tissue in Formalin","Fresh Tissue"]

courfh=cour.readlines()
for i in courfh:
    i=i.rstrip().split("\t")
    if i[0].startswith("Participant ID"):
        for col in range(0,len(i)):
            if i[col]=="Disease Term (MedDRA)":
                dis = col
            elif i[col]=="Specimen category":
                cat = col
            elif i[col]=="Assessment Timepoint":
                ass = col
            else:
                if i[col]=="Participant ID":
                    part = col
    else:
        if i[cat]=="Blood":
            continue
        else:
            search = str(i[part]+"_"+i[dis]+"_"+i[ass]+"_"+i[cat])
            if search in dict:
                continue
            else:
                dict[search]=0

# checking the dictionary if its present or else add it to the dictionary
acute={}
def check_dic(a,b,c):
    if b in c:
        c[b].append(a)
    else:
        c[b]=[]
        c[b].append(a)



#To get only archival longitudinal samples for every disease
def archival(ar,bas,on,post,prog):
    count_Ab = 0
    count_AO = 0
    count_APo = 0
    count_Aprog = 0

    if ar!=0:
        for each in ar:
            if each in bas:
                count_Ab+=1
            if each in on:
                count_AO+=1
            if each in post:
                count_APo+=1
            if each in prog:
                    count_Aprog+=1
        print(diseasename,"Archival and Baseline","\t",count_Ab)
        print(diseasename,"Archival and On Treatment","\t",count_AO)
        print(diseasename,"Archival and Post-Treatment (No Progression)","\t",count_APo)
        print(diseasename,"Archival and Progression","\t",count_Aprog)
    else:
        print("Archival and Baseline","\t",0)
        print("Archival and On Treatment","\t",0)
        print("Archival and Post-Treatment (No Progression)","\t",0)
        print("Archival and Progression","\t",0)

# to get baseline longitudinal samples for every disease

def baseline(ar,bas,on,post,prog):
    increBon=0
    increPost=0
    increProg=0

    if bas!=0:
        for ele in set(bas):
                if ele in on:
                    increBon += 1
                if ele in post:
                    increPost +=1
                if ele in prog:
                    increProg +=1

        print(diseasename,"Baseline and On Treatment","\t",increBon)
        print(diseasename,"Baseline and Post-Treatment (No Progression)","\t",increPost)
        print(diseasename,"Baseline and Progression","\t",increProg)
    else:
        print("Baseline and On Treatment","\t",0)
        print("Baseline and Post-Treatment (No Progression)","\t",0)
        print("Baseline and Progression","\t",0)


# to get on-treatment longitudinal samples for every disease

def onTreatment(ar,bas,on,post,prog):

    vabPost=0
    vabProg=0

    if on!=0:
        for val in set(on):
                if val in post:
                    vabPost +=1
                if val in prog:
                    vabProg +=1
        print(diseasename,"On Treatment and Post-Treatment (No Progression)","\t",vabPost)
        print(diseasename,"On Treatment and Progression","\t",vabProg)
    else:
        print("On Treatment and Post-Treatment (No Progression)","\t",0)
        print("On Treatment and Progression","\t",0)

# to get post-treatment longitudinal samples for every disease

def postTreatment(ar,bas,on,post,prog):
    checkProg=0

    if post!=0:
        for ee in set(post):
                if ee in prog:
                    checkProg +=1

        print(diseasename,"Post-Treatment (No Progression) and Progression","\t",checkProg)
    else:
        print("Post-Treatment (No Progression) and Progression","\t",0)

for value in ph:
    value = value.rstrip().split("\t")
    diseasename = value[0]
    timepoint = value[1]
    print(diseasename,timepoint)
    for x,y in dict.items():
        x=x.rstrip().split("_")
        if x[1] in diseasename:
            if x[2]=="Archival":
                check_dic(x[0],x[1]+"_A",acute)
            elif "Baseline" in x[2]:
                check_dic(x[0], x[1] + "_B", acute)
            elif "On Treatment (Fresh)" in x[2]:
                check_dic(x[0],x[1]+"_On",acute)
            elif "Post-Treatment (No progression)" in x[2]:
                check_dic(x[0],x[1] + "_Post",acute)
            elif "Progression (Fresh)" in x[2]:
                check_dic(x[0],x[1] + "_Prog",acute)

#checkinh the lenght of the string to add it to the dictionary else asign timepint to 0
    if diseasename+"_A" in acute:
        ar=acute.get(diseasename+"_A")
    else:
        ar=[]
    if diseasename+"_B" in acute:
        bas=acute.get(diseasename+"_B")
    else:
        bas=[]
    if diseasename+"_On" in acute:
        on=acute.get(diseasename+"_On")
    else:
        on=[]
    if diseasename+"_Post" in acute:
        post=acute.get(diseasename+"_Post")
    else:
        post=[]
    if diseasename+"_Prog" in acute:
        prog=acute.get(diseasename+"_Prog")
    else:
        prog=[]
    if timepoint == "Archival":
        archival(ar, bas, on, post, prog)
    elif timepoint == "Baseline":
        baseline(ar, bas, on, post, prog)
    elif timepoint == "On Treatment":
        onTreatment(ar, bas, on, post, prog)
    elif timepoint == "Post-Treatment":
        postTreatment(ar, bas, on, post, prog)


