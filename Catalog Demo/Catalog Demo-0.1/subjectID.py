import os,sys
#Creates Specimen ID using teh Public ID using the first 1000 ID's
os.chdir("/Users/mohandasa2/Desktop/Sample ID")
#opening the text file with 1000 ID's
file=open("ID.txt",'r')
output=open("ID-declared.txt",'w')
output.write("Public ID"+"\t"+"Specimen ID"+"\n")
fl=file.readlines()
# looping in the file to create a list
for line in fl:
    line=line.rstrip().split("\t")
    if line[0].startswith("Public ID"):
        continue
    else:
        #declaring a counter for the iD
        count=1
        # for id in range(10):
        #     output.write(line[0]+"\t"+line[0]+'-0'+str(count)+"\n")
        #     print(line[0],line[0]+'-'+str(count))
        #     #incrementing the counter
        #     count+=1

        for id in range(10):
            if count==10:
                output.write(line[0]+"\t"+line[0]+'-'+str(count)+"\n")
                print(line[0],line[0]+'-'+str(count))
            else:
                output.write(line[0]+"\t"+line[0]+'-0'+str(count)+"\n")
                print(line[0],line[0]+'-0'+str(count))
            #incrementing the counter
            count+=1