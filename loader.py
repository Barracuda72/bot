#!/usr/bin/env python2
# encoding: utf-8

import json
import urllib

def get_text(url):
    f = urllib.urlopen(url)
    return f.read()

def get_json(url):
    return json.loads(get_text(url))
