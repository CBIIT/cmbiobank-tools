#code for cleaning the targeted therapy file using regex and stop word algorithm

import io,os,nltk,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# word_tokenize accepts
# a string as an input, not a file.
os.chdir("/Users/mohandasa2/Desktop/dbGap Data/Submission-V2/Version 2/RAVE")
stop_words = nltk.corpus.stopwords.words('english')
wordlist=open("StopwordsListT.txt",'r',encoding="ISO-8859-1")
output=open("Filteredtargeted-therapy.txt","w")
filter=open("targetedListUnique.txt",'w')
wh=wordlist.readlines()
for word in wh:
	stop_words.append(word.rstrip())
filterdrug={}
with open("FinalList.txt",'r') as f:
	for go in f:
		b=go.rstrip().split("\t")
		s = re.sub("[\(\[].*?[\)\]]", "", b[9])
		# print(s)
		doc = word_tokenize(s)
		# print(doc)
		wordsFiltered = []
		for w in doc:
			if w not in stop_words:
				ss=w.replace("Gemtuzumab","Gemtuzumab ozogamicin").replace("RVD","Revlimid Velcade").replace("Darzalex","Darzalex Faspro").replace("Nivo","Nivolumab").replace("Belantamab","belantamab mafodotin").replace("daratumumab-hyaluronidase-fihj","daratumumab").replace("Nivolumablumab","Nivolumab")
				wordsFiltered.append(ss)
				if w in filterdrug:
					continue
				else:
					filterdrug[ss]=0
		output.write("\t".join(b[:2])+"\t"+str(wordsFiltered)+"\t"+"\t".join(b[2:])+"\n")
		print(wordsFiltered)

for m,n in filterdrug.items():
	filter.write(m+"\n")