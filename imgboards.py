#!/usr/bin/env python2
# encoding: utf-8

import json
from urllib import FancyURLopener
from HTMLParser import HTMLParser
import re

html_parser = HTMLParser()
link_regex = '>>[ ]*([0-9]+)'

class MyURLOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)  Gecko/20170827 Firefox/52.1.0'

myopener = MyURLOpener()

def get_text(url):
    f = myopener.open(url)
    return f.read()

def get_json(url):
    return json.loads(get_text(url))

def strip_comment(c):
    c = html_parser.unescape(c)
    c = re.sub('<br>', '\n', c)
    c = re.sub('<.*?>', ' ', c)
    c = re.sub('>.*\n?', ' ', c)
    #c = re.sub(link_regex + ' +(\(OP\)|)', ' ', c)
    c = re.sub('[ \n]+', ' ', c)
    return c.strip()
