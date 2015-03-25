import wikipedia
import nltk
import urllib
import codecs,sys
from bs4 import BeautifulSoup
import os
from nltk.parse import stanford
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
import os.path
import codecs
from subprocess import Popen, PIPE

#only look at sentences that have a chance
phrases = ["is", "was", "are", "were"]
def contains_phrase(sentence):
    for phrase in phrases:
        if phrase in nltk.word_tokenize(sentence):
            return True
    return False

#prevents from downloading from the internet every time. I have bad internet
def cached_page(page_name):
    text = None
    page = page_name.replace(' ','').lower()
    if os.path.isfile(page + '.cache'):
        return codecs.open(page + '.cache', encoding='utf-8').read().encode('ascii','replace')
    else:
        ny = wikipedia.page(page_name)
        with open(page + '.cache','w') as outfile:
            outfile.write(ny.content.encode('utf8'))
        return ny.content

ny = cached_page('New York')

#get sentences
sentences = nltk.sent_tokenize(ny.strip())

#get sentences which could be questions
sentences_of_interest = [sentence for sentence in sentences if contains_phrase(sentence)]
#sort by length, so we look at the easier ones first
sentences_of_interest = sorted(sentences_of_interest, key=lambda x: len(x))

#complicated syntax for getting the stanford parses
def stanford_parser():
    STANFORD_JARS_FOLDER = '../dependencies/stanford-parser'
    os.environ['STANFORD_PARSER'] = STANFORD_JARS_FOLDER
    os.environ['STANFORD_MODELS'] = STANFORD_JARS_FOLDER
    return stanford.StanfordParser()

#could be a better pattern probably
pattern = '__ < (NP $. (VP <, (VBZ|VBD|VBP|VB < is|are|was|were)))'

parser = stanford_parser()
for sentence in sentences_of_interest:
    #parse the sentence
    p = parser.raw_parse_sents([sentence])[0]
    #call tregex
    with open(os.devnull, 'wb') as devnull:
        tregex = Popen(['../dependencies/stanford-tregex/tregex.sh', pattern ,'-filter'], stdout=PIPE, stdin=PIPE, stderr=devnull)
    #get the result
    out = tregex.communicate(str(p))
    #no error checking #yolo
    try:
        tree = nltk.Tree.fromstring(out[0])
        #find the start of the pattern
        while tree[0].label() != 'NP':
            tree = tree[1:]
        subj = ' '.join(tree[0].leaves())
        #get rid of pronoun subjects a bit, should be done better
        if 'it' in subj.split() or 'It' in subj.split() or 'this' in subj.split() or 'This' in subj.split():
             continue
        #build the sentence
        verbphrase = tree[1].leaves()
        verb = verbphrase[0]
        capverb = verb[0].upper()+verb[1:]
        phrase = verbphrase[1:]
        print capverb+' '+subj+' '+' '.join(phrase)+'?'
    except:
        #who cares?
        pass