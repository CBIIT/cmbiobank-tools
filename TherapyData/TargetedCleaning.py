#code for cleaning the targeted therapy file using regex and stop word algorithm

import io,os,nltk,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# word_tokenize accepts
# a string as an input, not a file.
os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
stop_words = nltk.corpus.stopwords.words('english')
wordlist=open("StopwordsListT.txt",'r',encoding="ISO-8859-1")
output=open("Filteredtargeted-therapy.txt","w")
filter=open("targetedListUnique.txt",'w')
wh=wordlist.readlines()
for word in wh:
    stop_words.append(word.rstrip())
filterdrug={}
with open("TargetedTherapy-file.txt",'r') as f:
	for go in f:
		b=go.rstrip().split("\t")

		# print(b[2])
		s = re.sub("[\(\[].*?[\)\]]","", b[2])
		# dd= re.sub(r"(?<=\w) ", "", b[2])
		print(s)

		# val=s.replace(",","")
		# print(val)
		doc = word_tokenize(s)
		# print(doc)
		wordsFiltered = []
		for w in doc:
			if w not in stop_words:
				s=w.replace("Gemtuzumab","Gemtuzumab ozogamicin").replace("Targeted","Targeted Therapy").replace("Darzalex","Darzalex Faspro")
				wordsFiltered.append(s)
				if w in filterdrug:
					continue
				else:
					filterdrug[s]=0
		output.write("\t".join(b[:2])+"\t"+str(wordsFiltered)+"\t"+"\t".join(b[3:])+"\n")
		# print(wordsFiltered)

for m,n in filterdrug.items():
	filter.write(m+"\n")