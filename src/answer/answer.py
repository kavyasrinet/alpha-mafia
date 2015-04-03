#!/usr/bin/env python
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.lancaster import LancasterStemmer

def answer_all(article, questions):
    return [answer(article, question)[0] for question in questions]

def answer(article, question):
    st = LancasterStemmer()
    def stemmed_sentence(sentence):
        tokens = nltk.word_tokenize(sentence)
        return [st.stem(token) for token in  tokens]

    stop_words = set(stopwords.words('english'))

    sentences = nltk.sent_tokenize(article.strip())
    tokenized_sentences = [stemmed_sentence(sentence) for sentence in sentences]

    question_words = set(stemmed_sentence(question)) - stop_words
    question_dict = dict([(y, x) for (x, y) in enumerate(question_words)])

    sentence_vectors = []
    for sentence_tokens in tokenized_sentences:
        sentence_vector = [0]*len(question_dict)
        for word in sentence_tokens:
            if word in question_dict:
                sentence_vector[question_dict[word]] = 1
        sentence_vectors.append(sentence_vector)

    transformer = TfidfTransformer(norm = None, sublinear_tf = True)
    tfidf = transformer.fit_transform(sentence_vectors)


    tfidf_array = tfidf.toarray()

    max_value = max(tfidf_array, key=lambda row: row.sum()).sum()
    row_indexes = [i for (i,v) in enumerate(tfidf_array) if v.sum() == max_value]

    return [sentences[index] for index in row_indexes];


if __name__ == '__main__':
    #unit testing
    pass
