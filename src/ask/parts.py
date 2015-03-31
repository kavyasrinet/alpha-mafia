#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford

parser = stanford.Parser()

def get_np_vp(tree):
    idx = next((i for i,x in enumerate(tree) if x.label() == 'NP'), -1)
    if idx >= 0 and idx < len(tree) - 1:
        return tree[idx], tree[idx+1]
    return None, None

def question_parts(ranked, debug=False):
    for sentence in ranked:
        parts = question_part(sentence)
        if not parts: continue
        yield parts

def question_part(sentence):
    parse = parser.raw_parse_sents([sentence]).next().next()
    #call tregex
    pattern = '__ < (NP $. (VP <, (VBZ|VBD|VBP|VB <, is|are|was|were)))'
    output = stanford.tregex(str(parse), pattern, [])
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
    #unit testing
    pass
