#!/usr/bin/env python
import nltk
import common.stanford as stanford
from multiprocessing import Pool
import settings
parser = stanford.Parser()

def get_np_vp(tree):
    idx = next((i for i,x in enumerate(tree) if x.label() == 'NP'), -1)
    if idx >= 0 and idx < len(tree) - 1:
        return tree[idx], tree[idx+1]
    return None, None

def question_parts(ranked, debug=False):
    pool = Pool(settings.NUM_CORES)
    for parts in pool.imap(question_part, ranked):
        if parts: yield parts

def get_pattern(type):
    #normal Is/Was/Were
    if type ==1 :
        pattern = '__ < (NP $. (VP <, (VBZ|VBD|VBP|VB <, is|are|was|were)))'
    #variants of has been 
    elif type ==2:
        pattern = '__ < (NP $. (VP < (VP <,(VB|VBZ|VBP /VB*/ <, has|have) <2 (VP <, (VBN <, been))))) '
    #has been if the previous fails
    elif type == 3:
        pattern = '__ < (NP $. (VP <,(VB|VBZ|VBP <, has|have) <2 (VP <, (VBN <, been)))) '
    return pattern



def question_part(sentence):
    ls = ["has","been"]
    ls2 = ["have","been"]  
    #sentence = "Since the 1950s it has been regarded as a centre for intellectuals and artists."
    parse = parser.raw_parse_sents([sentence]).next().next()
    #call tregex
    #print sentence
    type  =2
    if type ==2: 
        if all(word in sentence for word in ls) or all(word in sentence for word in ls2):
            pattern = get_pattern(type)
        else:
            return
    pattern = get_pattern(type)
    #pattern = '__ < (NP $. (VP <, (VBZ|VBD|VBP|VB <, is|are|was|were)))'
    output = stanford.tregex(str(parse), pattern, [])
    if not output[0] and type==2:
        type =3
        pattern = get_pattern(type)
        output = stanford.tregex(str(parse), pattern, [])
        if not output[0]:
            print "Has been couldn't generate anything"
            return


    #try to get the tree
    tree = None
    try:
        tree = nltk.Tree.fromstring(output[0])
    except:
        return None
    #split into verb phrase and noun phrase
    np, vp = get_np_vp(tree)
    if not np:
        return None
    #get subject verb and object
    subj = ' '.join(np.leaves())
    verb = vp.leaves()[0]
    verb_object = ' '.join(vp.leaves()[1:])

    return (subj, verb, verb_object)

if __name__ == '__main__':

    question = "HARDCODED QUESTION"
    print question_part(question)
    #unit testing
    pass
