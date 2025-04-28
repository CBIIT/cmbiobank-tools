import os
from BSI_entityID import enDic
from BSI_entityID import pubID
from BSI_entityID import subspec

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
inven=open("Moonshot Report 4.25.2022.txt",'r',encoding='unicode_escape')
inven_Output=open("Inventory_Output.txt",'w')
inven_Output.write("Subject ID"+"\t"+"Original Id"+"\t"+"Parent ID"+"\t"+"BSI ID"+"\t"+"Derived Biospecimen Type"+"\t"+"Anatomic Site"+"\t"+"Hours in fixative (calculated)"+"\t"+"Collection Date"+"\t"+"QC Tumor Content after Enrichment (Moonshot)"+"\t"+"QC % Necrosis (Moonshot)"+"\t"+"Purification"+"\t"+"QC % Tumor (Moonshot)"+"\t"+"Vial Status"+"\t"+"Cell Count (x10^6)"+"\t"+"RIN"+"\t"+"DV200"+"\t"+"DIN"+"\t"+"Concentration by TapeStation (ng/ÂµL)"+"\t"+"Concentration by Nanodrop (ng/ÂµL)"+"\t"+"Concentration by Qubit (ng/ÂµL)"+"\t"+"Volume"+"\t"+"Volume Unit"+"\t"+"Suspension"+"\n")
invenfh=inven.readlines()
invenList=[]
for i in invenfh:
    # i.encode('utf-8').strip()
    i=i.rstrip().split("\t")
    if i[0]=="Subject ID":
        for col in range(0, len(i)):
            if i[col] == "Subject ID":
                Subject_ID = col
            elif i[col] == "Parent ID":
                Parent_ID = col

            elif i[col] == "Original Id":
                Original_Id = col

            elif i[col] == "BSI ID":
                BSI_ID = col

            elif i[col] == "Material Type":
                MaterialType = col

            elif i[col] == "Anatomic Site":
                AnatomicSite = col

            elif i[col] == "Collection Date/Time":
                CollectionDate = col

            elif i[col] == "Volume":
                Volume = col

            elif i[col] == "Volume Unit":
                Volume_Unit = col

            elif i[col] == "Fixation End Date/Time":
                FixationDate = col

            elif i[col] == "Concentration by Qubit (ng/µL)":
                con_Qubit = col

            elif i[col] == "Concentration by Nanodrop (ng/µL)":
                con_nanodrop = col

            elif i[col] == "Concentration by TapeStation (ng/µL)":
                con_tape = col

            # elif i[col] == "Collection Event Name":
            #     Collection= col

            elif i[col] == "DV200":
                DV200 = col

            elif i[col] == "DIN":
                DIN = col

            elif i[col] == "RIN":
                RIN = col

            elif i[col] == "Cell Count (x10^6)":
                cell_count = col

            elif i[col] == "Vial Status":
                Vial_Status = col

            elif i[col] == "QC % Tumor (Moonshot)":
                qc_tumor= col

            elif i[col] == "QC Tumor Content after Enrichment (Moonshot)":
                tumor_enrich= col

            elif i[col] == "Purification":
                Purification = col

            elif i[col] == "Suspension/Solvent":
                Suspension=col

            else:
                if i[col] == "QC % Necrosis (Moonshot)":
                    qc_nec = col
    else:
        if i[Vial_Status]=="Out" or i[Vial_Status]=="Reserved" or i[Vial_Status]=="Empty" or i[Vial_Status]=="Destroyed/Broken":
            continue
        else:
            search=[i[Subject_ID],i[Original_Id],i[Parent_ID],i[BSI_ID],i[MaterialType],i[AnatomicSite],i[FixationDate],i[CollectionDate],i[tumor_enrich],i[qc_nec],i[Purification],i[qc_tumor],i[Vial_Status],i[cell_count],i[RIN],i[DV200],i[DIN],i[con_tape],i[con_nanodrop],i[con_Qubit],i[Volume],i[Volume_Unit],i[Suspension]]
            if search in invenList:
                continue
            else:
                invenList.append(search)

            num=i[Subject_ID]+"_"+i[Parent_ID]
            # num1=i[Subject_ID]+"_"+i[BSI_ID]
            num2=i[Subject_ID]+"_"+i[Original_Id]

for element in invenList:
    # material type for embedded block to FFPE block
    if not element[0].startswith("Subject ID"):
        ffpe = element[4].replace("Embedded Block", "FFPE Block")
        element.insert(4, ffpe)
        element.pop(5)
        if element[5] == "Bone Marrow":
            pur = element[10].replace("CD138 Sort Negative Fraction", "CD138 '-' BM").replace("CD138 Sort Positive Fraction", "CD138 + BM")
            element.insert(10, pur)
            element.pop(11)
        elif element[5]=="Whole Blood":
            pur1=element[10].replace("CD138 Sort Negative Fraction","CD138 '-' Blood").replace("CD138 Sort Positive Fraction","CD138 + Blood")
            element.insert(10, pur1)
            element.pop(11)
        elif element[4]=="Curl":
            cur=element[4].replace("Curl","Tissue Curl")
            element.insert(4,cur)
            element.pop(5)



        inven_Output.write("\t".join(element) + "\n")

    else:
        continue

        # if num1 in enDic:
        #     print(str(enDic.get(num)),num,"Yessss")
        #     inven_Output.write(i[Subject_ID] + "\t"+str(pubID.get(i[Subject_ID])) + "\t"+i[Original_Id]+"\t"+str(subspec.get(num2))+"\t" + i[Parent_ID] + "\t" + str(enDic.get(num)) + "\t" + i[BSI_ID] + "\t" +str(enDic.get(num1))+
        #     "\t" + i[MaterialType]+"\t"+i[AnatomicSite] + "\t" + i[Collection]+ "\t" + i[CollectionDate] + "\t" + i[FixationDate] + "\t" +
        #     i[con_Qubit] + "\t" + i[con_nanodrop] + "\t" + i[DV200] + "\t" +i[DIN]+"\t"+ i[RIN] +"\t" + i[cell_count]+ "\t" +i[Vial_Comments] + "\t" + i[qc_nec] + "\n")
        # else:
        #     print(num1)







