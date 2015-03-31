#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
from filter import filtered_sentences
from parts import question_parts

def get_questions(article, nquestions, debug=False):
    sentences = filtered_sentences(article, debug)
    return question_parts(sentences, nquestions, debug)

if __name__ == '__main__':
    #unit testing
    pass
