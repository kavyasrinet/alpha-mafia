import nltk
import common.stanford as stanford
import ask.named_entities as ne
from ask.supersense_tagging import question_word
from ask.supersense_tagging import subject_supersense
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

type_map = {"what":"concept","where":"location","when":"date","who":"person","how":"concept","why":"concept"}

def get_type(question):
	first_word = question.split().lower()
	if first_word in type_map:
		return type_map[first_word]
	else:
		return "TF"


def get_supersense(question):
	entities = get_NER(question)
	 
	supersense = []
	for entity in entities:
		sup = question_word(entity[0])
		if sup[0]:
			supersense.append(sup)
	print supersense
	return supersense

def get_stemmed(question):
	#stemmer = PorterStemmer()
	stemmer = SnowballStemmer("english")
	tokens = get_tokens(question)
	stemmed_toks = []
	for tok in tokens:
		stemmed_toks.append(stemmer.stem(tok))
	print stemmed_toks
	return stemmed_toks

def get_tokens(question):
	return nltk.word_tokenize(question)

def get_NER(question):
	question = question.encode('utf-8')
	toks = stanford.ner(get_tokens(question))
	entities = ne.named_entities(toks)
	return entities

def main():
	get_supersense("Who were the Abha European to correctly depict the Crux?")
