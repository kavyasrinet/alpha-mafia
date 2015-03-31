#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

#linking verbs
verbs = ["are", "has", "have", "is", "should", "was", "will", "would", "were"]

#linking verbs of length == 2 words
verb_phrases = [["are", "being"], ["had", "been"], ["has", "been"],
["have", "been"], ["is", "being"], ["should", "be"], ["was", "being"],
["will", "be"], ["would", "be"], ["were", "being"]]

#checks if linking verbs are present
def contains_phrase(sentence):
    word_tokens = nltk.word_tokenize(sentence)

    #return true if the single word exists
    for verb in verbs:
        if verb in word_tokens:
            return True

    #return true if words occur in succession
    for verb_phrase in verb_phrases:
        indices = [i for i, word in enumerate(word_tokens) if word == verb_phrase[0]]

    	for index in indices:
    	    if ((index != (len(word_tokens)-1)) and (word_tokens[index+1] == verb_phrase[1])):
    		return True

    return False

#checks if the sentence has a noun
def contains_noun(sentence):
	word_tokens = nltk.word_tokenize(sentence)
	pos = nltk.pos_tag(word_tokens)

	#check if POS is a noun
	for word in pos:
	    if('NN' in word[1]):
		return True
	return False

#returns continuous chunks of Named Entities
def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk

#filter sentences for linking verbs, named entities etc.
def filtered_sentences(article, debug=False):
    sentences = nltk.sent_tokenize(article.strip())

    #check for linking verbs
    sentences = [sentence for sentence in sentences if contains_phrase(sentence)]

    #check for nouns
    sentences = [sentence for sentence in sentences if contains_noun(sentence)]

    #remove sentences which are very large
    sentences = [sentence for sentence in sentences if (len(nltk.word_tokenize(sentence)) < 15)]

    #sort by no. of named entities
    sentences = sorted(sentences, key = lambda x : -len(get_continuous_chunks(x)))

    return sentences
