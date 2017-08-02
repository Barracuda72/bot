#!/usr/bin/env python2
# encoding: utf-8

import json
import urllib
from HTMLParser import HTMLParser
import re

html_parser = HTMLParser()
link_regex = '>>[ ]*([0-9]+)'

def get_text(url):
    f = urllib.urlopen(url)
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
