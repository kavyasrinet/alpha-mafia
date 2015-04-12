#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford
from named_entities import named_entities
from supersense_tagging import question_word
from supersense_tagging import subject_supersense


pronoun_map = {"he" : "who", "she": "who", "it":"what","they":None,"there" : None}
det_map = {"this": "what","that":"which","these":"which"}
pronouns = ["it","he","she","they","there"]
dets = ["this","that","these"]
dont_discard_class = ["city","language"]
ner = {"ORGANIZATION":"what"}

def gen_question(parts):
    return to_question(*parts)


def determiner_question(first_word, rest, verb, obj):
    question = det_map[first_word] + rest
    return "%s %s %s?" % (question.capitalize(), verb, obj)


def get_wh(wh,cls):
    if cls in dont_discard_class:
        return wh+" "+cls
    else:
        return wh

def supersense_question(subj, verb, obj):
    #rds, to create questions
    sup = subject_supersense(subj)
    print sup
    x = get_wh(sup[0][1], sup[0][2])
    print x #return


def named_entity_question(subj, verb, obj):
    ners  = stanford.ner([subj])#named_entities(subj)
    entities = named_entities(ners)
    #print entities
    if entities:
        if entities[0][1]=="ORGANIZATION":
            #return
            print "What"
            entity = entities[0][0]
            sup = question_word(entity)
            #return
            print sup
    return None

def true_false(subj, verb, obj):
    #if no pronouns and determiners, ask regular question
    pronoun = next((pronoun in subj.lower() for pronoun in pronouns),None)
    det = next((det in subj.lower() for det in dets),None)
    if not det and not pronoun:
        return "%s %s %s?" % (verb.capitalize(), subj, obj)
    return None


def pronoun_question(first_word, verb, obj):
    question = pronoun_map[first_word]
    if question:
        return "%s %s %s?" % (question.capitalize(), verb, obj)


def to_question(subj, verb, obj):
    words = nltk.word_tokenize(subj)
    first_word = words[0].lower()
    if first_word in pronouns:
        if len(words) == 1:
            return pronoun_question(first_word, verb, obj)
        return None
    question = named_entity_question(subj, verb, obj)
    if question:
        return question
    if first_word in dets:
        question = determiner_question(first_word, subj[len(first_word):], verb, obj)
    else:
        question = supersense_question(subj, verb, obj)
    if question:
        return question
    return true_false(subj, verb, obj)

if __name__ == '__main__':
    #unit testing
    pass
