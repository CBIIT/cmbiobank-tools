import io,os,nltk,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# word_tokenize accepts
# a string as an input, not a file.
os.chdir("/Users/mohandasa2/Desktop/Laura-study/RAVE")
stop_words = nltk.corpus.stopwords.words('english')
wordlist=open("StopwordsList.txt",'r',encoding="ISO-8859-1")
output=open("Filteredtargeted-therapy.txt","w")
wh=wordlist.readlines()
for word in wh:
    stop_words.append(word.rstrip())

with open("TargetedTherapy-file.txt",'r') as f:
	for go in f:
		b=go.rstrip().split("\t")
		s = re.sub("[\(\[].*?[\)\]]", "", b[2])
		val=s.replace("+",",")
		# print(val)
		doc = word_tokenize(val)
		# print(doc)
		wordsFiltered = []
		for w in doc:
			if w not in stop_words:
				wordsFiltered.append(w)
		output.write("\t".join(b[:2])+"\t"+str(wordsFiltered)+"\t"+"\t".join(b[3:])+"\n")
		print(wordsFiltered)



# for r in val:
# 	print(r)
	# if not r in stop_words:
	# 	appendFile = open('filteredtext.txt','a')
	# 	appendFile.write(" "+s+"\n")
	# 	appendFile.close()
