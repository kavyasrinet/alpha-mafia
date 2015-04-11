#!/usr/bin/env python
from bs4 import BeautifulSoup

def get_article(html):
    soup = BeautifulSoup(html)
    return ' '.join(p.text for p in soup.select('p')).replace('\n', '')
