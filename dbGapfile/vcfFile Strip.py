
import os

os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V3/RAVE/DME_Download/VCF/VCF_Report")
# os.system("mkdir /Users/mohandasa2/Desktop/new_a/")
for i in os.listdir():
    if ".DS_Store" in i:
        continue
    else:
        os.system("touch /Users/mohandasa2/Desktop/new_b/"+i)
        os.system("grep -v '##fileDate=' "+i+"|grep -v '##fileUTCtime=' >/Users/mohandasa2/Desktop/new_b/"+i)


