#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import re
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

MAX_LENGTH = 30
#linking verbs
verbs = [["are"],  ["is"], ["should"], ["was"], ["would"], ["were"]]

#linking verbs of length == 2 words
verb_phrases = [["are", "being"], ["had", "been"], ["has", "been"],
["have", "been"], ["is", "being"], ["should", "be"], ["was", "being"],
["will", "be"], ["would", "be"], ["were", "being"]]

def short_enough(sentence):
    return len(sentence[0]) < MAX_LENGTH

def is_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))

def all_linking(sentence):
    for verb in verbs:
        if is_sublist(sentence[0], verb):
            yield verb
    for verb_phrase in verb_phrases:
        if is_sublist(sentence[0], verb_phrase):
            yield verb_phrase

#checks if linking verbs are present
def contains_linking(sentence):
    return len(list(all_linking(sentence))) != 0

def sentence_to_features(sentence):
    tags = nltk.pos_tag(sentence[0])
    nouns, pronouns = nouns_and_pronouns(tags)
    named_entities = named_entity_count(tags)
    return ((pronouns, nouns, named_entities),sentence[1])

#checks if the sentence has a noun
def nouns_and_pronouns(sentence):
    nn = re.compile('NN.*')
    pp = re.compile('PRP.*')
    nn_count = len(filter(nn.match, sentence[0]))
    pp_count = len(filter(pp.match, sentence[0]))
    return nn_count, pp_count

def named_entity_count(sentence):
    return len(ne_chunk(sentence))

def good_enough(sentence):
    pronouns, nouns, named_entities = sentence[0]
    return nouns > 2 and named_entities > 0 and pronouns < 1

def goodness(sentence):
    pronouns, nouns, named_entities = sentence[0]
    return float(5*named_entities + nouns - 10*pronouns)/float(len(sentence))

#filter sentences for linking verbs, named entities etc.
def filtered_sentences(article, debug=False):
    #get sentences from the article
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'e.g', 'i.e'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(article.strip())
    #tokenize all of the sentences
    sentences = [(nltk.word_tokenize(sentence), sentence) for sentence in sentences]
    #throw out sentences with no linking verb
    sentences = filter(short_enough, sentences)
    sentences = filter(next(all_linking(sentence), None), sentences)
    #pos tag the remaining sentences
    sentences = [sentence_to_features(sentence) for sentence in sentences]
    #filter(good_enough, sentences)
    sorted(sentences, key=goodness)
    return [sentence[1] for sentence in sentences]



#def get_continuous_chunks(text):
#    chunked = ne_chunk(pos_tag(word_tokenize(text)))
#    prev = None
#    continuous_chunk = []
#    current_chunk = []
#
#    for i in chunked:
#        if type(i) == Tree:
#            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
#        elif current_chunk:
#            named_entity = " ".join(current_chunk)
#            if named_entity not in continuous_chunk:
#                continuous_chunk.append(named_entity)
#                current_chunk = []
#        else:
#            continue
#
#    return continuous_chunk


