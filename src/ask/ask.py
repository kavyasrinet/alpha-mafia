#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
from filter import filtered_sentences
from parts import question_parts
from questions import gen_question
from rank import rank_questions

def get_questions(article, nquestions, debug=False):
    sentences = filtered_sentences(article, debug)
    questions = []
    for parts in question_parts(sentences, debug):
        question = gen_question(parts)
        if not question: continue
        if debug: print question
        questions.append(question)
    ranked = rank_questions(questions)
    if debug: print "### ranked ###"
    return ranked[0:nquestions]

if __name__ == '__main__':
    #unit testing
    pass
