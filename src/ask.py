#!/usr/bin/env python
import sys

def usage():
    print "usage:"
    print ""
    print "./ask.py article.txt nquestions"
    print "    article.txt - the article to ask questions about"
    print "    nquestions  - the number of questions to ask"

def main():
    if len(sys.argv) != 3:
        usage()
    article = None
    nquestions = None
    try:
        article = open(sys.argv[1],"r").read()
    except IOError:
        print "Could not open article file "+sys.argv[1]
    try:
        nquestions = int(sys.argv[2])
    except ValueError:
        print "Could not convert " +sys.argv[2] + "to integer"
    print articles, nquestions

if __name__ == '__main__':
    main()
