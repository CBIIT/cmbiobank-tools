import os, csv

def dbgap_id():
    os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
    output=open("specimen_transmittal_id_output.txt",'w')
    output.write("SubjectID"+"\t"+"BEDAT"+"\t"+"SPECCAT"+"\t"+"BECLMETH_SPD"+"\t"+"SPECID"+"\t"+"BESPEC_DRV"+"\t"+"ASMTTPT_DRV"+"\t"+"TISTYP"+"\t"+"Public Subject ID"+"\t"+"Public specimen ID"+"\n")
    #Write the OUTPUT HEADER HERE TO THE OUTPUT FILE#####################
    file = open("entity_ids.20220830.csv",'r')
    fh = csv.reader(file)
    finder = []
    enroll=[]
    entityDic={}
    spectrans=open("specimen_transmittal_output.txt",'r')
    spectrans_fh=spectrans.readlines()
    for line in spectrans_fh:
        # print(line)
        line=line.split("\t")
        if line[0]=="SubjectID":
            for column in range(0,len(line)):
                if line[column]=='SPECID':
                    specid=column
                # else:
                #     if line[column].rstrip()=='Sub Specimen ID':
                #         # print(column)
                #         subspecid=column
        else:
            new=line[0].split("_")
            # print(line[subspecid])
            # if line[subspecid]=="":
            k = [new[2], line[specid]]
            # print(k)
            k.extend(line)
            # print(k)
            if k in enroll:
                continue
            else:
                enroll.append(k)



    for ii in fh:
        if "ctep_id" in ii[0]:
            for vall in range(0,len(ii)):
                if 'ctep_id' in ii[vall]:
                    ctep_id=vall
                elif ii[vall]=="rave_spec_id":
                    rave_id=vall
                elif ii[vall]=="pub_spec_id":
                    pub_id=vall
                elif ii[vall]=="pub_id":
                    pub=vall
                # elif ii[vall]=="bcr_subspec_id":
                #     bcr_subspec_id=vall
                # else:
                #     if ii[vall]=="pub_subspec_id":
                #         pub_sub=vall
        else:
            # find=[ii[ctep_id],ii[rave_id],ii[bcr_subspec_id],ii[pub_id],ii[pub_sub],ii[pub]]
            find=[ii[ctep_id],ii[rave_id],ii[pub_id],ii[pub]]
            if find in finder:
                continue
            else:
                finder.append(find)

            # print(ii[ctep_id],ii[rave_id],ii[pub_id],ii[pub_sub])
    for m in enroll:
        # print(m)
        for v in finder:
            if v[-1]=='NA':
                continue
            else:
                if m[0]==v[0] and m[1]==v[1]:
                        outlist = [val.replace("\n", "") for val in m]
                        print(outlist)
                        #changing the specimen type
                        Stype=outlist[-3].replace("Fresh Tissue in Media to VARI","Formalin Fixed Tissue").replace("Formalin Fixed Core Biopsy","Formalin Fixed Tissue").replace("Fresh Tissue in Media to VARI","Formalin Fixed Tissue").replace("Streck Blood to VARI","Streck Blood to VARI").replace("Fresh Tissue in Media","Formalin Fixed Tissue").replace("Streck Blood to VARI","Streck Blood")
                        outlist.insert(-3,Stype)
                        outlist.pop(-3)
                        output.write("\t".join(outlist[2:]) + "\t" + v[-1] + "\t" + v[-2] + "\t" + "\n")
                        # output.write(m+"\t"+l+"\t"+ v[-1] + "\t" + v[-2] + "\n")

            # else:
                    #     if m[2].rstrip()==v[2]:
                    #         outlist = [val.replace("\n", "") for val in m]
                    #         print(outlist)
                            # print(ii[pub_id],ii[pub_sub])
                            # output.write("\t".join(outlist[3:])+"\t"+v[-1]+"\t"+v[-2]+"\t"+v[-3]+"\n")
                            # print("\t".join(outlist[2:])+"\t"+ii[pub_id]+"\t"+ii[pub_sub])

dbgap_id()