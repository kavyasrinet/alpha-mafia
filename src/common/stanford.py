from nltk.parse import stanford
import os
import os.path
from subprocess import Popen, PIPE

BASE_PATH = ''
STANFORD_JARS_FOLDER = BASE_PATH + '../dependencies/stanford-parser'
STANFORD_TREGEX = BASE_PATH + '../dependencies/stanford-tregex/tregex.sh'
STANFORD_NER = BASE_PATH + '../dependencies/stanford-ner/ner-alpha.sh'


def Parser():
    #set up the environment for the stanford parse
    os.environ['STANFORD_PARSER'] = STANFORD_JARS_FOLDER
    os.environ['STANFORD_MODELS'] = STANFORD_JARS_FOLDER
    return stanford.StanfordParser()

def tregex(tree, pattern, option=[]):
    #extend the argument with user specified options
    args = [STANFORD_TREGEX, pattern ,'-filter']
    args.extend(option)
    #create a tregex process
    with open(os.devnull, 'wb') as devnull:
        tregex_proc = Popen(args, stdout=PIPE, stdin=PIPE, stderr=devnull)
    #get the output
    return tregex_proc.communicate(str(tree))

def ner(sentences):
     #extend the argument with user specified options
    args = [STANFORD_NER]
    #args.extend(option)
    #create a tregex process
    with open(os.devnull, 'wb') as devnull:
        ner_proc = Popen(args, stdout=PIPE, stdin=PIPE, stderr=devnull)
    #get the output
    output = ner_proc.communicate('\n'.join(sentences))
    try:
        return output[0]
    except:
        return ''

if __name__ == '__main__':
    print ner(["Barrack Obama won a cheesecake at the Cheesecake Factory"])

