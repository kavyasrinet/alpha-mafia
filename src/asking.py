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

phrases = ["is"]
def contains_phrase(sentence):
    for phrase in phrases:
        if phrase in nltk.word_tokenize(sentence):
            return True
    return False


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

sentences = nltk.sent_tokenize(ny.strip())
soi = [sentence for sentence in sentences if contains_phrase(sentence)]

def stanford_parser():
    STANFORD_JARS_FOLDER = '../dependencies/stanford-parser'
    os.environ['STANFORD_PARSER'] = STANFORD_JARS_FOLDER
    os.environ['STANFORD_MODELS'] = STANFORD_JARS_FOLDER
    return stanford.StanfordParser()

pattern = '__ < (NP $. (VP <, (VBZ|VB < is|are|was|were)))'

parser = stanford_parser()
for sentence in soi:
    #print sentence
    p = parser.raw_parse_sents([sentence])[0]
    with open(os.devnull, 'wb') as devnull:
        tregex = Popen(['../dependencies/stanford-tregex/tregex.sh', pattern ,'-filter'], stdout=PIPE, stdin=PIPE, stderr=devnull)
    out = tregex.communicate(str(p))
    #print out[0]
    try:
        tree = nltk.Tree.fromstring(out[0])
        while tree[0].label() != 'NP':
            tree = tree[1:]
        subj = ' '.join(tree[0].leaves())
        if 'it' in subj.split() or 'It' in subj.split() or 'this' in subj.split() or 'This' in subj.split():
             continue
        verbphrase = tree[1].leaves()
        verb = verbphrase[0]
        capverb = verb[0].upper()+verb[1:]
        phrase = verbphrase[1:]
        print capverb+' '+subj+' '+' '.join(phrase)+'?'
    except:
        pass
    #print p.label()

#sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
# print sentences
# # GUI
# for sentence in sentences:
#     sentence.draw()

# ny = wikipedia.page('New York')
# print ny.content

# crux = wikipedia.page("Violin")
# # print crux.title + "\n"
# # print crux.url + "\n"
# #print crux.content + "\n"  
# content = crux.content

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
#text = nltk.sent_tokenize(content.split("\n"))