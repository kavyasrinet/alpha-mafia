#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
import named_entities as ne
from supersense_tagging import question_word
from supersense_tagging import subject_supersense
from question_formatter import *

pronoun_map = {"he" : "who", "she": "who", "it":"what","they":None,"there" : None}
det_map = {"this": "what","that":"which","these":"which"}
pronouns = ["it","he","she","they","there"]
dets = ["this","that","these"]
dont_discard_class = ["city","language","constellation","musical_instrument"]
ner = {"ORGANIZATION":"what"}

def gen_question(parts):
    (subj, verb, obj), tag = parts
    return to_question(subj, verb, obj, tag)

def determiner_question(first_word, rest, verb, obj, tag):
    question = det_map[first_word] + rest
    return format_wh(question.capitalize(), verb, obj)

def get_wh(wh,cls):
    if wh == "Who":
        return None
    if cls in dont_discard_class:
        return wh+" "+cls
    else:
        return None

def supersense_question(subj, verb, obj):
    #rds, to create questions
    sup = subject_supersense(subj)
    if sup:
        x = get_wh(sup[0][1], sup[0][2])
        if x:
            return format_wh(x,verb,obj)
        return None
    return None

def named_entity_question(subj, verb, obj, tag):
    subj = subj.encode('utf-8')
    entities = ne.named_entities(tag)
    if entities:
        if entities[0][1]=="ORGANIZATION":
            return format_wh("What",verb,obj)
        entity = entities[0][0]
        sup = question_word(entity)
        if sup[0] == "Who":
            return None
        else:
            x = get_wh(sup[0],sup[1])
            if x:
                return format_wh_class(sup[0],sup[1],verb,obj)
    return None

def true_false(subj, verb, obj, tag):
    #if no pronouns and determiners, ask regular question
    pronoun = next((pronoun in subj.lower() for pronoun in pronouns), None)
    det = next((det in subj.lower() for det in dets), None)
    if not det and not pronoun:
        return format_is(subj, verb.capitalize(), obj, tag)
    return None


def pronoun_question(first_word, verb, obj):
    question = pronoun_map[first_word]
    if question:
        return format_wh(question.capitalize(), verb, obj)

def to_question(subj, verb, obj, tag):
    words = nltk.word_tokenize(subj)
    first_word = words[0].lower()
    if first_word in pronouns:
        if len(words) == 1:
            return pronoun_question(first_word, verb, obj)
        return None
    question = named_entity_question(subj, verb, obj, tag)
    if question:
        return question
    if first_word in dets:
        question = determiner_question(first_word, subj[len(first_word):], verb, obj, tag)
    else:
        question = supersense_question(subj, verb, obj)
    if question:
        return question
    return true_false(subj, verb, obj, tag)

if __name__ == '__main__':
    #unit testing
    pass
