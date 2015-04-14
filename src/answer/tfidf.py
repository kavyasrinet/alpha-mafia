#!/usr/bin/env python
import nltk
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.lancaster import LancasterStemmer


def tfidf_list(original, sentences, question, count):
    n = len(sentences)
    m = len(question)
    feature_matrix = np.zeros((n, m))
    for i, sentence in enumerate(sentences):
        for j, word in enumerate(question):
            feature_matrix[i][j] = count(word, sentence)
    transformer = TfidfTransformer(norm=None, sublinear_tf=True, use_idf=True, smooth_idf=True)
    tfidf = transformer.fit_transform(feature_matrix).toarray()
    sentence_scores = zip(original, tfidf)
    return sentence_scores


if __name__ == '__main__':
    sentences = [["Bob","has","a","cat"],["jerry","is","a","loser"]]
    question = ["Bob","is","jerry"]
    print tfidf_list(question, sentences, count=lambda x,y: x in y)
