#!/usr/bin/env python
import nltk
import codecs, sys
import common.stanford as stanford

phrases = ["is", "was", "are", "were"]
pronoun_map = {"he" : "who", "she": "who", "it":"what","they":None}
det_map = {"this": "what","that":"which","these":"which"}
pronouns = ["it","he","she","they"]
dets = ["this","that","these"]

def contains_phrase(sentence):
    for phrase in phrases:
        if phrase in nltk.word_tokenize(sentence):
            return True
    return False

def filterd_sentences(article):
    sentences = nltk.sent_tokenize(article.strip())
    return [sentence for sentence in sentences if contains_phrase(sentence)]
    
def ranked_sentences(sentences):
    return sorted(sentences, key=lambda x: len(x))

def get_np_vp(tree):
    idx = next((i for i,x in enumerate(tree) if x.label() == 'NP'), -1)
    if idx >= 0 and idx < len(tree) - 1:
        return tree[idx], tree[idx+1]
    return None, None

def to_question(subj, verb, verb_object):
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

def get_questions(article, nquestions, debug=False):
    sentences = filterd_sentences(article)
    ranked = ranked_sentences(sentences)

    parser = stanford.Parser()

    questions = []
    for sentence in ranked:
        parse = parser.raw_parse_sents([sentence]).next().next()
        #call tregex
        pattern = '__ < (NP $. (VP <, (VBZ|VBD|VBP|VB <, is|are|was|were)))'
        output = stanford.tregex(str(parse), pattern, [])
        #try to get the tree
        tree = None
        try:
            tree = nltk.Tree.fromstring(output[0])
        except:
            continue
        #split into verb phrase and noun phrase
        np, vp = get_np_vp(tree)
        if not np:
            continue
        #get subject verb and object
        subj = ' '.join(np.leaves())
        verb = vp.leaves()[0]
        verb_object = ' '.join(vp.leaves()[1:])
        #construct question
        question = to_question(subj, verb, verb_object)
        if not question:
            continue
        #append if legit    
        if debug:
            print question
        questions.append(question)
        if len(questions) == nquestions:
            return questions
    return questions

if __name__ == '__main__':
    #unit testing
    pass
