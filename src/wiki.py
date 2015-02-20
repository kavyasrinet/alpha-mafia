import wikipedia
import nltk
import urllib
import codecs
from bs4 import BeautifulSoup
import os
from nltk.parse import stanford
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer


STANFORD_JARS_FOLDER = '../dependencies/stanford-parser'

os.environ['STANFORD_PARSER'] = STANFORD_JARS_FOLDER
os.environ['STANFORD_MODELS'] = STANFORD_JARS_FOLDER

# parser = stanford.StanfordParser()

# sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
# print sentences

# # GUI
# for sentence in sentences:
#     sentence.draw()

# ny = wikipedia.page('New York')
# print ny.content

crux = wikipedia.page("Santiago")
# print crux.title + "\n"
# print crux.url + "\n"
#print crux.content + "\n"	
content = crux.content

# history =  crux.section("History")
# summary = wikipedia.summary("Santiago", sentences=5)	
#question = "Where is Crux located ?"
#question = "What is it dominated by ?"
#question = "Is it commonly known as the Southern Cross ?"
#question = "Do the brightest stars of the Crux appear on the Austrailian flag ?"
#question = "what is the most prominent dark nebula in the skies ?"
#question = "Which constellation borders the Crux on east, north and west ?"
#question = "Is the Crux easily visible from the Northern Hemisphere throughout the year ?"
#question = "Is Santiago the capital of Chile ?"
#question  = "Has the air pollution in Santiago reduced in 2010 ?"
#question = "Are the eastern communes in Santiago richer than the western communes ?"
question = "What is the name of Santiago's public bus transport system ?"
#text = nltk.sent_tokenize(content.split("\n"))


i=0
#print len(content.split("\n"))
text = []
for l in content.split("\n"):
	text.extend(nltk.sent_tokenize(l))

#print len(text)

stopWords = stopwords.words('english')

map_s = []
for line in text:
	list_w = [0 for i in range(len(question.split()))]
	for k,word in enumerate(question.split()):
		if word in stopWords:
			continue
		if word in line:
			list_w[k] +=1
	map_s.append(list_w)

transformer = TfidfTransformer(norm = None, sublinear_tf = True)
tfidf = transformer.fit_transform(map_s)

print tfidf.toarray()

arr = tfidf.toarray()
max_r = -1

for l in arr:
	s = l.sum()
	if s > max_r:
		max_r = s
ind = 0
for l in arr:
	s = l.sum()
	if s == max_r:
		print text[ind]
	ind = ind +1

print max_r
# 	print nltk.pos_tag(text)
