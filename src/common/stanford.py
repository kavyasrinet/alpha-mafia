from nltk.parse import stanford
import os
import os.path
from subprocess import Popen, PIPE

STANFORD_JARS_FOLDER = '../dependencies/stanford-parser'
STANFORD_TREGEX = '../dependencies/stanford-tregex/tregex.sh'

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
