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

def to_question(subj, verb, verb_object):
    split = subj.lower().split()
    first_word = split[0]
    #if the subject is only a pronoun, ask a question
    print "subject is ",subj

    
    ners  = stanford.ner([subj])#named_entities(subj)
    entities = named_entities(ners)
    print entities
    indicator = 0
    supersense= []
    if entities:
        if entities[0][1]=="ORGANIZATION":
            #return
            print "What"
            entity = entities[0][0]
            sup = question_word(entity)
            #return
            print sup
    else:
        if first_word in pronouns and len(split) == 1:
            question = pronoun_map[first_word]
            if question:
                return "%s %s %s?" % (question.capitalize(), verb, verb_object)
        #replace specific determiners as first words, to create questions
        if first_word in dets:
            question = det_map[first_word] + ' '.join(split[1:]).capitalize()
            return "%s %s %s?" % (question.capitalize(), verb, verb_object)

        sup = subject_supersense(subj)
        print sup
        x = get_wh(sup[0][1], sup[0][2])
        
        print x #return 

    #     #if no pronouns and determiners, ask regular question
    #     pronoun = next((pronoun in subj.lower() for pronoun in pronouns),None)
    #     det = next((det in subj.lower() for det in dets),None)
    #     if not det and not pronoun:
    #         return "%s %s %s?" % (verb.capitalize(), subj, verb_object)
    #     return None
    return None


def get_wh(wh,cls):
    if cls in dont_discard_class:
        return wh+" "+cls
    else:
        return wh



if __name__ == '__main__':
    #unit testing
    pass
