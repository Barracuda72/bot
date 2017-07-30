#!/usr/bin/env python2
# encoding: utf-8

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
import sqlite3
import random
import sber
import datetime

db = sqlite3.connect('data.db', check_same_thread=False)

stemmer = SnowballStemmer("russian")

try:
    c = db.cursor()
    c.execute('CREATE TABLE sentences (sentence TEXT, hash INT)')
    c.execute('CREATE TABLE answers (hash_question INT, hash_answer INT)')
    db.commit()
except:
    print 'Tables already exists!'

def hash_text(text):
    leave = set(['S', 'V', 'S-PRO', 'NUM=ciph'])
    #sents = sent_tokenize(text.decode('utf-8'))
    sents = sent_tokenize(text)
    words = [word_tokenize(x) for x in sents]
    tags = [nltk.pos_tag(sent, lang='rus') for sent in words]
    hs = 0
    for sent in tags:
        for word in sent:
            #print word[0], word[1],
            if ((word[1] in leave) or (word[1] == 'NONLEX' and len(word[0]) > 2)):
                w = stemmer.stem(word[0])
                h = hash(w.lower())
                hs = hs * 31 + h
                #print w, h,
        #print ''
    if (hs == 0):
        return None
    else:
        return hs & 0x7FFFFFFFFFFFFFFF

def ext_get_curr():
    curr = sber.get_curr()
    return 'Доллар %.02f/%.02f, евро %.02f/%.02f' % (curr[0][0], curr[0][1], curr[1][0], curr[1][1])

def ext_get_time():
    return u'Сейчас ' + datetime.datetime.now().strftime(u'%H:%M') + u' в моей временной зоне'

prepared = {
    hash_text(u'Курису, скажи курс валют'): ext_get_curr,
    hash_text(u'Курису, сколько времени'): ext_get_time
}

def produce_reply(text):
    hs = hash_text(text)
    if (not hs):
        return dummy_reply()

    prep = prepared.get(hs)
    if (prep):
        return prep()

    c = db.cursor()
    c.execute('SELECT COUNT(*) FROM answers WHERE hash_question=?', (hs,))
    (num,) = c.fetchone()

    if (num == 0):
        return dummy_reply()
    else:
        rows = c.execute('SELECT hash_answer FROM answers WHERE hash_question=?', (hs,))
        data = [x for x in rows]
        ch = int(random.choice(data)[0])
        c.execute('SELECT sentence FROM sentences WHERE hash=?', (ch,))
        return c.fetchone()[0]

    return u'Я что-то даже не знаю, что и сказать...'

def add_reply(question, answer):
    hs_q = hash_text(question)
    hs_a = hash_text(answer)
    if (hs_q and hs_a):
        c.executemany('INSERT INTO sentences VALUES (?,?)',
            [
                (question, hs_q),
            (answer, hs_a),
            ]
        )
        c.execute('INSERT INTO answers VALUES (?,?)', (hs_q, hs_a))
        db.commit()

def dummy_reply():
    replies = [
        u'Ты что, дурак?',
        u'Отвратительно! Исчезни!',
        u'Извращенец!',
        u'Ты думаешь, что вообще говоришь?',
        u'Иди нафиг',
    ]
    return random.choice(replies)
