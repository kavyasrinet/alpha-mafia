#!/usr/bin/env python
import wikipedia
import os.path

CACHE_DIR = 'cache'

def cached_page(page_name):
    text = None
    page = page_name.replace(' ','').lower()
    cache_page = os.path.join(CACHE_DIR, page)
    if os.path.isfile(cache_page):
        return codecs.open(cache_page, encoding='utf-8').read().encode('ascii','replace')
    else:
        ny = wikipedia.page(page_name)
        with open(cache_page,'w') as outfile:
            outfile.write(ny.content.encode('utf8'))
        return ny.content