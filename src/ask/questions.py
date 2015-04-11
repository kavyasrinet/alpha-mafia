#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford

pronoun_map = {"he" : "who", "she": "who", "it":"what","they":None}
det_map = {"this": "what","that":"which","these":"which"}
pronouns = ["it","he","she","they"]
dets = ["this","that","these"]

def gen_question(parts):
    return to_question(*parts)

def wh_quest(subj, verb, obj):
    pass

def true_false(subj, verb, obj):
    split = subj.lower().split()
    first_word = split[0]
    #if the subject is only a pronoun, ask a question
    if first_word in pronouns and len(split) == 1:
        question = pronoun_map[first_word]
        if question:
            return "%s %s %s?" % (question.capitalize(), verb, verb_object)
        return None
    #replace specific determiners as first words, to create questions
    if first_word in dets:
        question = det_map[first_word] + ' '.join(split[1:]).capitalize()
        return "%s %s %s?" % (question.capitalize(), verb, verb_object)
    #if no pronouns and determiners, ask regular question
    pronoun = next((pronoun in subj.lower() for pronoun in pronouns),None)
    det = next((det in subj.lower() for det in dets),None)
    if not det and not pronoun:
        return "%s %s %s?" % (verb.capitalize(), subj, verb_object)
    return None

def to_question(subj, verb, verb_object):
    return true_false(subj, verb, obj)

if __name__ == '__main__':
    #unit testing
    pass
