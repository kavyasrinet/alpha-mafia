import wikipedia
import nltk
import urllib
import codecs,sys
from bs4 import BeautifulSoup
import os
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.lancaster import LancasterStemmer

# ny = wikipedia.page('New York')
# print ny.content

crux = wikipedia.page("Violin")

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
#question = "What is the name of Santiago's public bus transport system ?"
question = "Who made the instrument known as Lady Blunt ?"

def answer(article, question):
	st = LancasterStemmer()
	def stemmed_sentence(sentence):
		tokens = nltk.word_tokenize(sentence)
		return [st.stem(token) for token in  tokens]

	stop_words = set(stopwords.words('english'))

	sentences = nltk.sent_tokenize(content.strip())
	tokenized_sentences = [stemmed_sentence(sentence) for sentence in sentences]

	question_words = set(stemmed_sentence(question)) - stop_words
	question_dict = dict([(y, x) for (x, y) in enumerate(question_words)])

	sentence_vectors = []
	for sentence_tokens in tokenized_sentences:
		sentence_vector = [0]*len(question_dict)
		for word in sentence_tokens:
			if word in question_dict:
				sentence_vector[question_dict[word]] += 1
		sentence_vectors.append(sentence_vector)

	transformer = TfidfTransformer(norm = None, sublinear_tf = True)
	tfidf = transformer.fit_transform(sentence_vectors)


	tfidf_array = tfidf.toarray()

	max_value = max(tfidf_array, key=lambda row: row.sum()).sum()
	row_indexes = [i for (i,v) in enumerate(tfidf_array) if v.sum() == max_value]

	return [sentences[index] for index in row_indexes];

print answer(content, question)