#!/usr/bin/env python
import sys
import codecs
import unicodedata
from common.article import get_article
from ask.ask import get_questions

def usage():
    print "usage:"
    print ""
    print "./ask.py article.txt nquestions"
    print "    article.txt - the article to ask questions about"
    print "    nquestions  - the number of questions to ask"

def main():
    if len(sys.argv) != 3:
        usage()
        return
    article_html = None
    nquestions = None
    try:
        article_html = codecs.open(sys.argv[1],encoding='utf-8').read()
    except IOError:
        print "Could not open article file "+sys.argv[1]
        return
    try:
        nquestions = int(sys.argv[2])
    except ValueError:
        print "Could not convert " +sys.argv[2] + "to integer"
        return
    article = get_article(article_html)
    questions = get_questions(article, nquestions)
    for question in questions:
        print question

if __name__ == '__main__':
    main()
