#!/usr/bin/env python2
# encoding: utf-8

import sys
import re
from HTMLParser import HTMLParser
import lang
import imgboards

def get_categories():
    try:
        return imgboards.get_json('https://2ch.hk/makaba/mobile.fcgi?task=get_boards')
    except:
        return []

def get_board_catalog(board):
    try:
        return imgboards.get_json('https://2ch.hk/%s/catalog.json' % board)
    except:
        return {'threads':[]}

def get_thread(board, tid):
    return imgboards.get_json('https://2ch.hk/%s/res/%s.json' % (board, tid))

if (__name__ == '__main__'):
    categories = get_categories()
    for category in categories:
        print u'Категория "%s"' % category
        for board in categories[category]:
            board_name = board['name']
            board_id = board['id']
            print u'Доска %s (%s)' % (board_name, board_id)
            cat = get_board_catalog(board_id)
            for thread_h in cat['threads']:
                thread_num = thread_h['num']
                print u'Тред %s' % thread_num
                try:
                    thread = get_thread(board_id, thread_num)
                except:
                    continue
                posts = thread['threads'][0]['posts']
                posts_dict = dict()
                for post in posts:
                    posts_dict[int(post['num'])] = post

                for post in posts:
                    comment = post['comment']
                    replies_to = [m.group(1) for m in re.finditer(imgboards.link_regex, comment)]
                    if (len(replies_to) == 1):
                        orig = posts_dict.get(int(replies_to[0]))
                        if (orig):
                            replies_to_o = [m.group(1) for m in re.finditer(link_regex, orig['comment'])]
                            if (len(replies_to_o) <= 1):
                                o_c = imgboards.strip_comment(orig['comment'])
                                r_c = imgboards.strip_comment(post['comment'])
                                l_oc = len(o_c)
                                l_rc = len(r_c)
                                if (l_oc > 3 and l_oc < 100 and l_rc > 3 and l_rc < 100):
                                    #print r_c, 'replies to', o_c
                                    lang.add_reply(o_c, r_c)
