import wikipedia
import nltk
import codecs, sys
import os.path
import stanford

#prevents from downloading from the internet every time. I have bad internet
def cached_page(page_name):
    text = None
    page = page_name.replace(' ','').lower()
    if os.path.isfile(page + '.cache'):
        return codecs.open(page + '.cache', encoding='utf-8').read().encode('ascii','replace')
    else:
        ny = wikipedia.page(page_name)
        with open(page + '.cache','w') as outfile:
            outfile.write(ny.content.encode('utf8'))
        return ny.content

phrases = ["is", "was", "are", "were"]
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

pronoun_map = {"he" : "who", "she": "who", "it":"what","they":None}
det_map = {"this": "what","that":"which","these":"which"}

def to_question(subj, verb, verb_object):
    pronouns = ["it","he","she","they"]
    dets = ["this","that","these"]
    split = subj.lower().split()
    first_word = split[0]
    if first_word in pronouns and len(split) == 1:
        question = pronoun_map[first_word]
        if question:
            return "%s %s %s?" % (question.capitalize(), verb, verb_object)
        return None
    if first_word in dets:
        question = det_map[first_word] + ' '.join(split[1:]).capitalize()
        return "%s %s %s?" % (question.capitalize(), verb, verb_object)

    pronoun = next((pronoun in subj.lower() for pronoun in pronouns),None)
    det = next((det in subj.lower() for det in dets),None)
    if not det and not pronoun:
        return "%s %s %s?" % (verb.capitalize(), subj, verb_object)
    return None

ny = cached_page('New York')
sentences = filterd_sentences(ny)
ranked = ranked_sentences(sentences)



parser = stanford.Parser()

for sentence in ranked:
    parse = parser.raw_parse_sents([sentence]).next().next()
    #call tregex
    pattern = '__ < (NP $. (VP <, (VBZ|VBD|VBP|VB <, is|are|was|were)))'
    output = stanford.tregex(str(parse), pattern, [])
    #no error checking #yolo
    tree = None
    try:
        tree = nltk.Tree.fromstring(output[0])
    except:
        continue
    np, vp = get_np_vp(tree)
    if not np:
        continue
    subj = ' '.join(np.leaves())
    verb = vp.leaves()[0]
    verb_object = ' '.join(vp.leaves()[1:])

    question = to_question(subj, verb, verb_object)
    if question:
        print question