from textblob import TextBlob
import os

os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
file=open("typo.txt",'r')
fh=file.readlines()

result_string = ", ".join(str(x) for x in fh)

aa=TextBlob(result_string)

bb=aa.correct()
print(bb)
