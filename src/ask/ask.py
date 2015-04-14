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

reload(sys)
sys.setdefaultencoding('utf-8')
parser = stanford.Parser()

def multi_parse(sentences):
    parses = list(parser.raw_parse_sents(sentences))
    out = []
    for i in xrange(len(sentences)):
        out.append((sentences[i], parses[i].next()))
    return out

def stanford_ner(parts_list):
    subjs = [parts[0].replace('\n',' ').encode('utf-8') for parts in parts_list]
    output = stanford.ner(subjs).split('\n')
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
    sentences = filtered_sentences(article, debug)
    parses = stanford_parse(sentences, pool)
    parts_list = []
    for partial in pool.imap(question_parts, parses):
        parts_list.extend(partial)
    mod_list = stanford_ner(parts_list)
    questions = [(gen_question(item), item) for item in mod_list]
    questions = filter(lambda x: x[0], questions)
    questions = [(sent, parts) for (sent,(parts,_)) in questions]
    (wh_ranked, verb_ranked) = ranked_questions(questions)
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

    #if any category falls short of questions
    if(len(questions) < nquestions):
        num_questions = len(questions)

        if verb_ctr < verb_num_questions:
            for i in range(wh_ctr, len(wh_questions)):
                questions.append(wh_questions[i])
            #end for
        else:
            for i in range(verb_ctr, len(verb_questions)):
                questions.append(verb_questions[i])
            #end for
        #end if
    #end if

    shuffle(questions)

    return questions

if __name__ == '__main__':
    #unit testing
    pass
