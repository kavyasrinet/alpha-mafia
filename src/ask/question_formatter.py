#!/usr/bin/env python
import nltk
import named_entities
import os

def cap_subj(subj):
    if not subj[0].isupper():
        return False
    entities = named_entities.ner(subj)
    if len(entities) == 0:
        return False

def decapitalize(subj):
    return subj[:1].lower() + subj[1:] if subj else ''

def space(obj):
    return obj[0].isalnum()

def format_is(subj, verb, obj):
    if not cap_subj(subj):
        subj = decapitalize(subj)
    if space(obj):
        obj = ' '+obj
    verb = verb.capitalize()
    return "%s %s%s?" % (verb, subj, obj)

def format_wh(wh, verb, obj):
    if space(obj):
        obj = ' '+obj
    wh = wh.capitalize()
    return "%s %s%s?" % (wh, verb, obj)

def format_wh_class(wh, clss, verb, obj):
    if space(obj):
        obj = ' '+obj
    wh = wh.capitalize()
    return "%s %s %s%s?" % (wh, clss, verb, obj)

if __name__ == '__main__':
    pass
