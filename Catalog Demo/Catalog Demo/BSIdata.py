import os
from BSI_entityID import enDic
from BSI_entityID import pubID
from BSI_entityID import subspec

os.chdir("/Users/mohandasa2/Desktop/CatalogData/RAVE")
inven=open("Moonshot Report 8.9.2021.txt",'r',encoding='unicode_escape')
inven_Output=open("Inventory_Output.txt",'w')
inven_Output.write("Subject ID"+"\t"+"Public ID"+"\t"+"Specimen ID"+"\t"+"Public Specimen ID"+"\t"+"Parent ID"+"\t"+"Public Parent subspecimen ID"+"\t"+"BSI ID"+"\t"+"SubSpec ID"+"\t"+"Material Type"+"\t"+"Fixative"+"\t"+"Volume"+"\t"+"Volume Unit"+"\t"+
                   "Concentration by Qubit (ng/µL)"+"\t"+"Concentration by Nanodrop (ng/µL)"+"\t"+"DV200"+"\t"+"DIN"+"\t"+"RIN"+"\t"+"Cell Count (x10^6)"+"\t"+"QC % Necrosis (Moonshot)"+"\n")
invenfh=inven.readlines()
invenList=[]
for i in invenfh:
    # i.encode('utf-8').strip()
    i=i.rstrip().split("\t")
    if i[0]=="Subject ID":
        for col in range(0, len(i)):
            if i[col] == "Subject ID":
                Subject_ID = col
                # print(Subject_ID)
            elif i[col] == "Parent ID":
                Parent_ID = col
            elif i[col] == "BSI ID":
                BSI_ID = col
            elif i[col] == "Material Type":
                Material_Type = col
            elif i[col] == "Fixative":
                Fixative = col
            elif i[col] == "Volume":
                Volume = col
            elif i[col] == "Volume Unit":
                Volume_Unit = col
            elif i[col] == "Concentration by Qubit (ng/µL)":
                con_Qubit = col
            elif i[col] == "Concentration by Nanodrop (ng/µL)":
                con_nanodrop = col
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
            elif i[col] == "Original Id":
                Original_Id = col
            else:
                if i[col] == "QC % Necrosis (Moonshot)":
                    qc_nec = col
    else:
        if i[Vial_Status]=="Out" or i[Vial_Status]=="Reserved":
            continue
        else:

            num=i[Subject_ID]+"_"+i[Parent_ID]
            num1=i[Subject_ID]+"_"+i[BSI_ID]
            num2=i[Subject_ID]+"_"+i[Original_Id]
        # if num in enDic:
        #     print("yes")
        #     print(i[Subject_ID] + "\t" + i[Parent_ID] + "\t"+enDic.get(num)+"\t" + i[BSI_ID] + "\t" + i[Material_Type] + "\t" + i[Fixative] + "\t" + \
        #          i[Volume]+ "\t" + i[Volume_Unit] + "\t" + i[con_Qubit]+"\t"+ i[con_nanodrop] + "\t" + i[DV200]+"\t"+i[DIN]+"\t"+ i[RIN] +
        #       "\t" + i[cell_count]+ "\t" + i[qc_nec]+"\n")
        #
        #
        # if i[0] in pubID:
        #     num
        #     print(pubID.get(i[0]))
        #     # print(i[Subject_ID] +pubID.get(num)+ "\t" + i[Parent_ID] + "\t" + enDic.get(num) + "\t" + i[BSI_ID] + "\t" + i[
        #     #     Material_Type] + "\t" + i[Fixative] + "\t" + \
        #     #       i[Volume] + "\t" + i[Volume_Unit] + "\t" + i[con_Qubit] + "\t" + i[con_nanodrop] + "\t" + i[
        #     #           DV200] + "\t" + i[RIN] +
        #     #       "\t" + i[cell_count] + "\t" + i[qc_nec] + "\n")
        if num1 in enDic:
            print(str(enDic.get(num)),num,"Yessss")
            # print((i[Subject_ID] + "\t"+pubID.get(num) + "\t" + i[Parent_ID] + "\t" + enDic.get(num) + "\t" + i[BSI_ID] + "\t" +str(enDic.get(num1))))
            inven_Output.write(i[Subject_ID] + "\t"+str(pubID.get(i[Subject_ID])) + "\t"+i[Original_Id]+"\t"+str(subspec.get(num2))+"\t" + i[Parent_ID] + "\t" + str(enDic.get(num)) + "\t" + i[BSI_ID] + "\t" +str(enDic.get(num1))+
             "\t"+i[Material_Type] + "\t" + i[Fixative] + "\t" + i[Volume] + "\t" + i[Volume_Unit] + "\t" + i[con_Qubit] +
            "\t" + i[con_nanodrop] + "\t" + i[DV200] + "\t" +i[DIN]+"\t"+ i[RIN] +"\t" + i[cell_count] + "\t" + i[qc_nec] + "\n")
        else:
            print(num1)







