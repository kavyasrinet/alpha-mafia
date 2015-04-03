#!/usr/bin/env python
import nltk
import common.stanford as stanford
from multiprocessing import Pool
import settings
import re

parser = stanford.Parser()

class TreeFinder:

    tree = None
    index = None

    def __init__(self, tree, output):
        results = output[0].split(':')
        tree_num = int(results[0])
        item_num = int(results[1])
        self.find_tree(tree, item_num, 1)

    def find_tree(self, tree, index, so_far):
        #print tree
        #print so_far
        if not isinstance(tree,nltk.Tree):
            return so_far
        #print tree.height()
        for i, item in enumerate(tree):
            so_far += 1
            if so_far == index:
                self.tree = tree
                self.index = i
                return so_far+1
            so_far = self.find_tree(item, index, so_far)
            if so_far > index: return so_far
        return stuff


def original_text(sentence, tokens):
    #build regex
    regex_string = ''
    for i,token in enumerate(tokens):
        if token.startswith('-') and token.endswith('-'):
            continue
        regex_string += re.escape(token)
        if i != len(tokens) -1:
            regex_string += '.*';
    #search for regex in original string
    match = re.search(regex_string, sentence)
    if match:
        return match.group(0)
    return None


def get_parts(np, vp, sentence, verb_length):
    subject = original_text(sentence, np)
    if len(vp) < verb_length:
        return None
    verb = original_text(sentence, vp[0:verb_length])
    verb_object = original_text(sentence, vp[verb_length:])
    if subject and verb and verb_object:
        return subject, verb, verb_object
    return None

#should make sure things work
def question_part(sentence):
    parse = parser.raw_parse_sents([sentence]).next().next()
    #call tregex
    pattern = 'NP $. (VP <, (VBZ|VBD|VBP|VB <, is|are|was|were))'
    #try to get the tree
    output = stanford.tregex(str(parse), pattern, ['-x'])
    #output = stanford.tregex(str(parse), pattern, [])
    #print output
    f = None
    try:
        f = TreeFinder(parse, output)
    except:
        return None
    np = f.tree[f.index]
    vp = f.tree[f.index+1]
    return get_parts(np.leaves(), vp.leaves(), sentence, 1)


def question_parts(ranked, debug=False):
    for rank in ranked:
        temp = question_part(rank)
        if temp: yield temp
    #pool = Pool(settings.NUM_CORES)
    #for parts in pool.imap(question_part, ranked):
    #    if parts: yield parts


if __name__ == '__main__':
    question = "Jane, the daughter of a magistrate, is coming to town next Saturday."
    original_text(question,['the','daughter','of'])
    #print question_part(question)
    #unit testing
    pass
