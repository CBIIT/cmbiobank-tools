
#code for cleaning the non targeted therapy file using regex and stop word algorithm
import io,os,nltk,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# word_tokenize accepts
# a string as an input, not a file.
os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
stop_words = nltk.corpus.stopwords.words('english')
wordlist=open("StopwordsListNT.txt",'r',encoding="ISO-8859-1")
output=open("FilteredNontargeted-therapy.txt","w")
filternon=open("nontargetedListUnique.txt",'w')
wh=wordlist.readlines()
for word in wh:
    stop_words.append(word.rstrip())
filterednonDrug={}
with open("NonTargeted-file.txt",'r') as f:
	for go in f:
		b=go.rstrip().split("\t")
		s = re.sub("[\(\[].*?[\)\]]", "", b[1])
		# print(s)
		val=s.replace("+",",")
		# print(val)
		doc = word_tokenize(val)
		# print(doc)
		wordsFiltered = []
		for w in doc:
			if w not in stop_words:
				s=w.replace("-","").replace("FOLFOX6","FOLFOX").replace("CyD","Cyclophosphamide-dexamethasone").replace("Zoledronic","Zoledronic Acid").replace("Liver","Liver SBRT").replace("mFOLFOX","FOLFOX").replace("Auto","Auto stem cell transplant").replace("autologous","Auto stem cell transplant").replace("ASCT","Auto stem cell transplant").replace("Folfox","FOLFOX").replace("Folfiri","FOLFIRI").replace("Trifluridine-Tipiracil","trifluridine/tipiracil")
				wordsFiltered.append(s)
				if w in filterednonDrug:
					continue
				else:
					filterednonDrug[s]=0
		output.write("\t".join(b[:1])+"\t"+str(wordsFiltered)+"\t"+"\t".join(b[2:])+"\n")
		# print(wordsFiltered)

for l,k in filterednonDrug.items():
	filternon.write(l+"\n")
