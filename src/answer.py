#!/usr/bin/env python
import sys

def usage():
    print "usage:"
    print ""
    print "./answer.py article.txt questions.txt"
    print "    article.txt  - the article to answer questions with"
    print "    question.txt - the questions to answer"

def main():
    if len(sys.argv) != 3:
        usage()
    article = None
    questions = None
    try:
        article = open(sys.argv[1],"r").read()
    except IOError:
        print "Could not open article file "+sys.argv[1]
    try:
        questions = open(sys.argv[2],"r").readlines()
    except IOError:
        print "Could not open questions file "+sys.argv[2]
    print article, questions

if __name__ == '__main__':
    main()
