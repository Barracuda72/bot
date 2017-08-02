#!/usr/bin/env python2
# encoding: utf-8

import sys
import re
from HTMLParser import HTMLParser
import lang
import imgboards

htnl_parser = HTMLParser()

def get_categories():
    return [
        'b', 'u', 'rf', 'dt', 'vg', 'r', 'cr', 'lor', 'mu', 'oe', 
        's', 'w', 'hr', 'a', 'ma', 'sw', 'hau', 'azu', 'tv', 'cp', 
        'gf', 'bo', 'di', 'vn', 've', 'wh', 'fur', 'to', 'bg', 
        'wn', 'slow', 'mad', 'd', 'news',
    ]

def get_page_count(board):
    page = imgboards.get_json('http://dobrochan.com/%s/0.json' % board)
    return int(page['boards'][board]['pages'])

def get_page(board, num):
    return imgboards.get_json('http://dobrochan.com/%s/%d.json' % (board, num))

def get_thread(tid):
    return imgboards.get_json('http://dobrochan.com/api/thread/%s/all.json?new_format&message_raw' % tid)

if (__name__ == '__main__'):
    cats = get_categories()
    for board in cats:
        try:
            page_count = get_page_count(board)
        except:
            continue
        for i in reversed(range(0, page_count)):
            try:
                page = get_page(board, i)
            except:
                continue
            for t in page['boards'][board]['threads']:
                tid = t['thread_id']
                print u'Thread %s' % tid
                try:
                    thread = get_thread(tid)
                except:
                    continue
                posts = thread['result']['posts']
                posts_dict = dict()
                for post in posts:
                    posts_dict[int(post['display_id'])] = post

                #print posts_dict

                for post in posts:
                    comment = post['message']
                    replies_to = [m.group(1) for m in re.finditer(imgboards.link_regex, comment)]
                    if (len(replies_to) == 1):
                        orig = posts_dict.get(int(replies_to[0]))
                        #print comment
                        #print orig
                        if (orig):
                            replies_to_o = [m.group(1) for m in re.finditer(imgboards.link_regex, orig['message'])]
                            if (len(replies_to_o) <= 1):
                                o_c = imgboards.strip_comment(orig['message'])
                                r_c = imgboards.strip_comment(post['message'])
                                l_oc = len(o_c)
                                l_rc = len(r_c)
                                if (l_oc > 3 and l_oc < 100 and l_rc > 3 and l_rc < 100):
                                    #print r_c, 'replies to', o_c
                                    lang.add_reply(o_c, r_c)
