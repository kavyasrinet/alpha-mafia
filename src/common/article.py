#!/usr/bin/env python
from bs4 import BeautifulSoup

def get_article(html):
    soup = BeautifulSoup(html)
    return soup.get_text().replace('\n',' ')