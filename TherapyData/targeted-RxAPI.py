#!/usr/bin/python
import os
import sys
import requests
import simplejson as json
import urllib.request

os.chdir("/Users/mohandasa2/Desktop/Laura-study/Therapy")
file=open("targetedListUnique.txt",'r')
filehead=file.readlines()
out=open("satndarNamesT.txt",'w')

for i in filehead:
	i=i.rstrip().split("\t")
	if "Targeted Therapy" in i[0]:
		continue
	else:
		# print(i[0])
		if " " in i[0]:
			with urllib.request.urlopen("https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term=" + i[0].replace(" ",'%20') + "&maxEntries=4") as url:
				data = url.read()
				values = json.loads(data)
				store = values['approximateGroup']['candidate'][0]['rxcui']
				# print(store)
		else:
			with urllib.request.urlopen("https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term=" + i[0] + "&maxEntries=4") as url:
				data = url.read()
				values = json.loads(data)
				store=values['approximateGroup']['candidate'][0]['rxcui']
				print(store)
		with urllib.request.urlopen("https://rxnav.nlm.nih.gov/REST/rxcui/"+ store +"/related.json?tty=IN") as link:
			content=link.read()
			contVal= json.loads(content)
			# targeted=
			out.write(i[0]+"\t"+contVal['relatedGroup']['conceptGroup'][0]['conceptProperties'][0]['name']+"\n")
			print(i[0],"\t",contVal['relatedGroup']['conceptGroup'][0]['conceptProperties'][0]['name'])




