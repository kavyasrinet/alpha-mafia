#!/usr/bin/env python
import sys
import codecs
from common.article import get_article
from answer.answer import answer_all

def usage():
    print "usage:"
    print ""
    print "./answer.py article.txt questions.txt"
    print "    article.txt  - the article to answer questions with"
    print "    question.txt - the questions to answer"

def main():
    if len(sys.argv) != 3:
        usage()
        return
    article_html = None
    questions = None
    try:
        article_html = codecs.open(sys.argv[1], encoding='utf-8').read()
    except IOError:
        print "Could not open article file "+sys.argv[1]
        return
    try:
        questions = codecs.open(sys.argv[2], encoding='utf-8').read()
    except IOError:
        print "Could not open questions file "+sys.argv[2]
        return
    article = get_article(article_html)
    questions = questions.splitlines()
    answers = answer_all(article, questions)
    for answer in answers:
        print answer

if __name__ == '__main__':
    main()
