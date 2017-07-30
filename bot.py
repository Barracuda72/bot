#!/usr/bin/env python2
# encoding: utf-8

import config
import telebot

import json
import time

import lang

bot = telebot.TeleBot(config.bot_token)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Отвечаем только на сообщения, упоминающие бота, или ответы на его сообщения, или сообщения в приват (id > 0)
    if ((u'курису' in message.text.lower()) or
      (message.reply_to_message and message.reply_to_message.from_user and
      message.reply_to_message.from_user.first_name == 'Kurisu-chan') or
      (message.chat.id > 0)
      ):
        reply = lang.produce_reply(message.text)
        time.sleep(len(reply)/50.0) # type speed = 50 letters/min
        bot.send_message(message.chat.id, reply, reply_to_message_id = message.message_id)
    # Пытаемся обучиться
    if (message.reply_to_message):
        lang.add_reply(message.reply_to_message.text, message.text)

@bot.channel_post_handler(content_types=['text'])
def repeat_all_posts(post):
    bot.send_message(post.chat.id, u'Ты написал: '+post.text)

if (__name__ == '__main__'):
    while (True):
    #    print produce_reply(raw_input())
        #try:
            bot.polling(none_stop=True)
        #except:
            print "Exception, restarting bot..."
            time.sleep(1.0)
