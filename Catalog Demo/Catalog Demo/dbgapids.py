import os, csv

def dbgap_id():
    os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
    output=open("specimen_transmittal_id_output.txt",'w')
    output.write("SubjectID"+"\t"+"BEDAT"+"\t"+"SPECCAT"+"\t"+"BECLMETH_SPD"+"\t"+"SPECID"+"\t"+"BESPEC_DRV"+"\t"+"ASMTTPT_DRV"+"\t"+"TISTYP"+"\t"+"BSTEST"+"\t"+"SubSpecimen-ID"+"\t"+"Public Subject ID"+"\t"+"Public_Subspecimen_id"+"\t"+"Public specimen ID"+"\n")
    #Write the OUTPUT HEADER HERE TO THE OUTPUT FILE#####################
    file = open("entity_ids.20210809.csv",'r')
    fh = csv.reader(file)
    finder = []
    enroll=[]
    spectrans=open("specimen_transmittal_output.txt",'r')
    spectrans_fh=spectrans.readlines()
    for line in spectrans_fh:
        line=line.split("\t")
        if line[0]=="SujectID":
            for column in range(0,len(line)):
                if line[column]=='SPECID':
                    specid=column
                else:
                    if line[column].rstrip()=='SubSpecimen-ID':
                        print(column)
                        subspecid=column
        else:
            new=line[0].split("_")
            # print(line[subspecid])
            if line[subspecid].rstrip()=="":
                k = [new[2], line[specid],"NA"]
                print(k)
                k.extend(line)
                enroll.append(k)
            else:
                k=[new[2],line[specid],line[subspecid]]
                k.extend(line)
                enroll.append(k)
    for ii in fh:
        if ii[0].startswith("ctep_id"):
            for vall in range(0,len(ii)):
                if ii[vall]=='ctep_id':
                    ctep_id=vall
                elif ii[vall]=="rave_spec_id":
                    rave_id=vall
                elif ii[vall]=="pub_spec_id":
                    pub_id=vall
                elif ii[vall]=="pub_id":
                    pub=vall
                elif ii[vall]=="bcr_subspec_id":
                    bcr_subspec_id=vall
                else:
                    if ii[vall]=="pub_subspec_id":
                        pub_sub=vall
        else:
            find=[ii[ctep_id],ii[rave_id],ii[bcr_subspec_id],ii[pub_id],ii[pub_sub],ii[pub]]
            # print(ii[ctep_id],ii[rave_id],ii[pub_id],ii[pub_sub])
            finder.append(find)
    for m in enroll:
        for v in finder:
            if v[-1]=='NA' and v[-2]=='NA':
                continue
            else:
                if m[0]==v[0] and m[1]==v[1] and m[2].rstrip()==v[2]:
                        outlist = [val.replace("\n", "") for val in m]
                        output.write("\t".join(outlist[3:]) + "\t" + v[-1] + "\t" + v[-2] + "\t" + v[-3] + "\n")
                    # else:
                    #     if m[2].rstrip()==v[2]:
                    #         outlist = [val.replace("\n", "") for val in m]
                    #         print(outlist)
                            # print(ii[pub_id],ii[pub_sub])
                            # output.write("\t".join(outlist[3:])+"\t"+v[-1]+"\t"+v[-2]+"\t"+v[-3]+"\n")
                            # print("\t".join(outlist[2:])+"\t"+ii[pub_id]+"\t"+ii[pub_sub])

dbgap_id()