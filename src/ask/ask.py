#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
from filter import filtered_sentences
import settings
from parts import question_parts
from questions import gen_question
from question_ranking import ranked_questions
from multiprocessing import Pool
import time
import math
from random import shuffle

parser = stanford.Parser()

def multi_parse(sentences):
    parses = list(parser.raw_parse_sents(sentences))
    out = []
    for i in xrange(len(sentences)):
        out.append((sentences[i], parses[i].next()))
    return out

def stanford_ner(parts_list):
    subjs = [parts[0].replace('\n',' ').encode('utf-8',errors='ignore') for parts in parts_list]
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
    questions = [(gen_question(item), item) for item in mod_list]
    questions = filter(lambda x: x[0], questions)
    t5 = time.time()
    questions = [(sent, parts) for (sent,(parts,_)) in questions]
    (wh_ranked, verb_ranked) = ranked_questions(questions)
    t6 = time.time()
    print "filter",t1-t0
    print "parse",t2-t1
    print "parts",t3-t2
    print "mod",t4-t3
    print "gen",t5-t4
    print "rank",t6-t5
    print wh_ranked
    print verb_ranked
    if debug:
        for rank in wh_ranked:
            print rank
        for rank in verb_ranked:
            print rank
    return shuffle_questions(wh_ranked, verb_ranked, nquestions)

def shuffle_questions(wh_questions, verb_questions, nquestions):
    questions = []

    verb_num_questions = 0
    wh_num_questions = 0

    if(len(verb_questions) < len(wh_questions)):
        verb_num_questions = int(math.floor(nquestions/2))
        wh_num_questions = nquestions - verb_num_questions
    else:
        wh_num_questions = int(math.floor(nquestions/2))
        verb_num_questions = nquestions - wh_num_questions

    verb_ctr = 0
    for question in verb_questions:
        if (verb_ctr < verb_num_questions):
            questions.append(question)
        #end if
        verb_ctr += 1
    #end for

    wh_ctr = 0
    for question in wh_questions:
        if(wh_ctr < wh_num_questions):
            questions.append(question)
        #end if
        wh_ctr += 1
    #end for

    shuffle(questions)

    return questions

if __name__ == '__main__':
    #unit testing
    pass
