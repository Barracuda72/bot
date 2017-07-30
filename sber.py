#!/usr/bin/env python2
# encoding: utf-8

import loader
import datetime

def get_curr():
    date = datetime.date.today().strftime('%d.%m.%Y')
    data = loader.get_json('http://www.sberbank.ru/common%2Fjs%2Fget_quote_values.php%3Fversion%3D1%26inf_block%3D123%26_number_amount114%3D10000%26qid%5B%5D=3%26qid%5B%5D=2%26cbrf%3D0%26period%3Don%26_date_afrom114%3D' + date + '%26_date_ato114%3D'+ date + '%26mode%3Dfull%26display%3Djson')
    euro = (0.0, 0.0)
    usd = (0.0, 0.0)
    for k in data:
        sell = float(data[k]['quotes'].values()[0]['sell'])
        buy = float(data[k]['quotes'].values()[0]['buy'])
        if (data[k]['meta']['TITLE_ENG'] == u'USD'):
            usd = (buy, sell)
        elif (data[k]['meta']['TITLE_ENG'] == u'Euro'):
            euro = (buy, sell)
            
    return (usd, euro)

if (__name__ == '__main__'):
    print get_curr()
