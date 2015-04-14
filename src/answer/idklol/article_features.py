from Levenshtein import distance
import numpy as np

def compute_levenshtein(token, sent_tokens):
	word = (map(lambda x: (x,distance(token,x)), sent_tokens))
	word = min(word, key = lambda t: t[1])
	print "The closest word to "+token+" is "+word[0]
	return word[0]

