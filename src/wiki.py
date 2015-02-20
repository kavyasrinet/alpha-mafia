import wikipedia
import nltk
import os
from nltk.parse import stanford

STANFORD_JARS_FOLDER = '../dependencies/stanford-parser'

os.environ['STANFORD_PARSER'] = STANFORD_JARS_FOLDER
os.environ['STANFORD_MODELS'] = STANFORD_JARS_FOLDER

parser = stanford.StanfordParser()

sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
print sentences

# GUI
for sentence in sentences:
    sentence.draw()

ny = wikipedia.page('New York')
print ny.content