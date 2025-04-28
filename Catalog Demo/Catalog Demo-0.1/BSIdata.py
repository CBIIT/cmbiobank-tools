import os
from BSI_entityID import enDic
from BSI_entityID import pubID
from BSI_entityID import subspec

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
inven=open("Moonshot Report 11.08.2021.txt",'r',encoding='unicode_escape')
inven_Output=open("Inventory_Output.txt",'w')
inven_Output.write("Subject ID"+"\t"+"Specimen ID"+"\t"+"Parent ID"+"\t"+"Material Type"+"\t"+"Anatomic Site"+"\t"+"Fixation Date"+"\t"+"Collection Date"+"\t"+"Collection Event Name"+"\t"+"QC % Necrosis (Moonshot)"+"\t"+"Purification"+"\n")
invenfh=inven.readlines()
invenList=[]
for i in invenfh:
    # i.encode('utf-8').strip()
    i=i.rstrip().split("\t")
    if i[0]=="Subject ID":
        for col in range(0, len(i)):
            if i[col] == "Subject ID":
                Subject_ID = col
                print(Subject_ID,"Subject ID")
            elif i[col] == "Parent ID":
                Parent_ID = col
                print(Parent_ID,"ParentID")
            # elif i[col] == "BSI ID":
            #     BSI_ID = col
            #     print(BSI_ID,"BSI ID")
            elif i[col] == "Material Type":
                MaterialType = col
                print(MaterialType,"Material Type")
            elif i[col] == "Anatomic Site":
                AnatomicSite = col
                print(AnatomicSite,"Anatomic Site")
            elif i[col] == "Collection Date/Time":
                CollectionDate = col
                print(CollectionDate,"CollDate")
            elif i[col] == "Fixation End Date/Time":
                FixationDate = col
                print(FixationDate,"FixDate")
            # elif i[col] == "Concentration by Qubit (ng/µL)":
            #     con_Qubit = col
            #     print(con_Qubit,"conQ")
            # elif i[col] == "Concentration by Nanodrop (ng/µL)":
            #     con_nanodrop = col
            #     print(con_nanodrop,"con Nano")
            elif i[col] == "Collection Event Name":
                Collection= col
                print(Collection,"Collection Name")
            # elif i[col] == "DV200":
            #     DV200 = col
            #     print(DV200,"Dv200")
            # elif i[col] == "DIN":
            #     DIN = col
            #     print(DIN,"DIN")
            # elif i[col] == "RIN":
            #     RIN = col
            #     print(RIN,"RIN")

            # elif i[col] == "Cell Count (x10^6)":
            #     cell_count = col
            #     print(cell_count,"Cell Count")

            elif i[col] == "Vial Status":
                Vial_Status = col
                print(Vial_Status,"Vial status")

            # elif i[col] == "Vial Comments":
            #     Vial_Comments = col
            #     print(Vial_Comments,"vial comments")

            elif i[col] == "Purification":
                Purification = col
                print(Purification,"vial comments")

            elif i[col] == "Original Id":
                Original_Id = col
                print(Original_Id,"orginal ID")

            else:
                if i[col] == "QC % Necrosis (Moonshot)":
                    qc_nec = col
                    print(qc_nec,"QC")
    else:
        if i[Vial_Status]=="Out" or i[Vial_Status]=="Reserved" or i[Vial_Status]=="Empty":
            continue
        else:
            search=[i[Subject_ID],i[Original_Id],i[Parent_ID],i[MaterialType],i[AnatomicSite],i[FixationDate],i[CollectionDate],i[Collection],i[qc_nec],i[Purification]]
            if search in invenList:
                continue
            else:
                invenList.append(search)

            num=i[Subject_ID]+"_"+i[Parent_ID]
            # num1=i[Subject_ID]+"_"+i[BSI_ID]
            num2=i[Subject_ID]+"_"+i[Original_Id]

for element in invenList:
    inven_Output.write("\t".join(element)+"\n")

        # if num1 in enDic:
        #     print(str(enDic.get(num)),num,"Yessss")
        #     inven_Output.write(i[Subject_ID] + "\t"+str(pubID.get(i[Subject_ID])) + "\t"+i[Original_Id]+"\t"+str(subspec.get(num2))+"\t" + i[Parent_ID] + "\t" + str(enDic.get(num)) + "\t" + i[BSI_ID] + "\t" +str(enDic.get(num1))+
        #     "\t" + i[MaterialType]+"\t"+i[AnatomicSite] + "\t" + i[Collection]+ "\t" + i[CollectionDate] + "\t" + i[FixationDate] + "\t" +
        #     i[con_Qubit] + "\t" + i[con_nanodrop] + "\t" + i[DV200] + "\t" +i[DIN]+"\t"+ i[RIN] +"\t" + i[cell_count]+ "\t" +i[Vial_Comments] + "\t" + i[qc_nec] + "\n")
        # else:
        #     print(num1)







