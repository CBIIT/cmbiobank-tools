import os, csv

def dbgap_id():
    os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
    output=open("BSI with public ID_output.txt",'w')
    output.write("Subject ID" + "\t" + "Original Id" + "\t" + "Parent ID" + "\t" + "BSI ID" + "\t" + "Derived Biospecimen Type" + "\t" + "Anatomic Site" + "\t" + "Hours in fixative (calculated)" + "\t" + "Collection Date" + "\t" + "QC Tumor Content after Enrichment (Moonshot)" + "\t" + "QC % Necrosis (Moonshot)" + "\t" + "Purification" + "\t" + "QC % Tumor (Moonshot)" + "\t" + "Vial Status" + "\t" + "Cell Count (x10^6)" + "\t" + "RIN" + "\t" + "DV200" + "\t" + "DIN" + "\t" + "Concentration by TapeStation (ng/ÂµL)" + "\t" + "Concentration by Nanodrop (ng/ÂµL)" + "\t" + "Concentration by Qubit (ng/ÂµL)" + "\t" + "Volume" + "\t" + "Volume Unit" + "\t" + "Suspension" + "\n")
    file = open("entity_ids.20220425.2.csv",'r')
    fh = csv.reader(file)
    finder = []
    enroll=[]
    entityDic={}
    spectrans=open("Inventory_Output.txt",'r')
    spectrans_fh=spectrans.readlines()
    for line in spectrans_fh:
        line=line.split("\t")
        if line[0]=="Subject ID":
            for column in range(0,len(line)):
                if line[column]=='Original Id':
                    specid=column
                elif line[column]=='Subject ID':
                    sub=column
                else:
                    if line[column]=='BSI ID':
                        bsi=column

        else:
            k = [line[sub], line[specid],line[bsi]]
            # print(k)
            k.extend(line)
            print(k)
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

                elif ii[vall]=="bcr_subspec_id":
                    bcr_subspec_id=vall
                else:
                    if ii[vall]=="pub_subspec_id":
                        pub_sub=vall
        else:
            find=[ii[ctep_id],ii[rave_id],ii[bcr_subspec_id],ii[pub],ii[pub_id],ii[pub_sub]]
            # print(find)
            if find in finder:
                continue
            else:
                finder.append(find)

    for m in enroll:
        for v in finder:
            # print(v)
            if v[-3]=='NA':
                continue
            else:
                # print(m[0],v[0],m[1],v[1],m[3],v[3])
                if m[0]==v[0] and m[1]==v[1] and m[2]==v[2]:
                        outlist = [val.replace("\n", "") for val in m]
                        print(outlist)

                        output.write("\t".join(outlist[3:]) + "\t" +v[-3]+"\t"+ v[-1] + "\t" + v[-2] + "\t" + "\n")
    #                     # output.write(m+"\t"+l+"\t"+ v[-1] + "\t" + v[-2] + "\n")

            # else:
                    #     if m[2].rstrip()==v[2]:
                    #         outlist = [val.replace("\n", "") for val in m]
                    #         print(outlist)
                            # print(ii[pub_id],ii[pub_sub])
                            # output.write("\t".join(outlist[3:])+"\t"+v[-1]+"\t"+v[-2]+"\t"+v[-3]+"\n")
                            # print("\t".join(outlist[2:])+"\t"+ii[pub_id]+"\t"+ii[pub_sub])

dbgap_id()