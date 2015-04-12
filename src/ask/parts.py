#!/usr/bin/env python
import nltk
import settings
from filter import all_linking
import common.stanford as stanford
import re

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
            regex_string += '[^a-zA-Z0-9]*';
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

def get_patterns(sentence):
    sentence_object = (nltk.word_tokenize(sentence), sentence)
    for verb in all_linking(sentence_object):
        if len(verb) == 1:
            p1 = 'NP $. (VP <, (/VB.?/ <, %s))'
            p2 = 'NP $. (VP <, (/MD.?/ <, %s))'
            p1 = p1 % verb[0]
            p2 = p2 % verb[0]
            yield [p1, p2]
        if len(verb) == 2:
            p1 = 'NP $. (VP < (VP <,(/VB.?/ <, %s) <2 (VP <, (/VB.?/ <, %s))))'
            p2 = 'NP $. (VP <,(/VB.?/ <, %s) <2 (VP <, (/VB.?/ <, %s)))'
            p1 = p1 % (verb[0],verb[1])
            p2 = p2 % (verb[0],verb[1])
            yield [p1, p2]


#should make sure things work
def question_part(sentence, parse):
    parts_list = []
    for pattern_list in get_patterns(sentence):
        f = None
        for pattern in pattern_list:
            #call tregex
            output = stanford.tregex(str(parse), pattern, ['-x'])
            try:
                #try to get the tree
                f = TreeFinder(parse, output)
                break
            except:
                pass
        #if we didn't find anything, abandon ship
        if not f: continue
        np = f.tree[f.index]
        vp = f.tree[f.index+1]
        #print "NP: ", np.leaves()
        #print "VP: ", vp.leaves()
        yolo = get_parts(np.leaves(), vp.leaves(), sentence, 1)
        parts_list.append(yolo)
    return parts_list

def question_parts(rank, debug=False):
    sentence, parse = rank
    output = []
    for parts in question_part(sentence, parse):
        output.append(parts)
    return output


if __name__ == '__main__':
    question = "Jane, the daughter of a magistrate, is coming to town next Saturday."
    original_text(question,['the','daughter','of'])
    pass
