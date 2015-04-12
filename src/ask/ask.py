#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
from filter import filtered_sentences
import settings
from parts import question_parts
from questions import gen_question
from rank import rank_questions
from multiprocessing import Pool
import time

parser = stanford.Parser()

def multi_parse(sentences):
    parses = list(parser.raw_parse_sents(sentences))
    out = []
    for i in xrange(len(sentences)):
        out.append((sentences[i], parses[i].next()))
    return out

def stanford_ner(parts_list):
    subjs = [parts[0] for parts in parts_list]
    output = stanford.ner(subjs).split('\n')
    print len(subjs)
    print len(output)
    parts_ner = []
    for i in xrange(len(parts_list)):
        parts_ner.append((parts_list[i],output[i]))
    return parts_ner

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def stanford_parse(sentences, pool):
    chunk_list = chunks(sentences, max(1, len(sentences)/(2*settings.NUM_CORES)))
    out_list = []
    for partial in pool.imap(multi_parse, chunk_list):
        out_list.extend(partial)
    return out_list


def get_questions(article, nquestions, debug=False):
    pool = Pool(settings.NUM_CORES)
    t0 = time.time()
    sentences = filtered_sentences(article, debug)
    t1 = time.time()
    parses = stanford_parse(sentences, pool)
    t2 = time.time()
    parts_list = []
    for partial in pool.imap(question_parts, parses):
        parts_list.extend(partial)
    t3 = time.time()
    mod_list = stanford_ner(parts_list)
    t4 = time.time()
    print "filter",t1-t0
    print "parse",t2-t1
    print "parts",t3-t2
    print "mod",t4-t3
    print mod_list
    questions = [(gen_question(item), item) for item in mod_list]
    questions = filter(lambda x: x[0], questions)
    #ranked = rank_questions(questions)





    ranked = rank_questions(questions)
    if debug: print "### ranked ###"
    return ranked[0:nquestions]

if __name__ == '__main__':
    #unit testing
    pass
