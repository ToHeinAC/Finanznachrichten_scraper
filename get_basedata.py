# Created by He at 06.01.2021

# Feature: basic data scraper

# Scenario: scrape the data

#---------------------------------------------------------

#import requests
from helper import *

url = 'https://www.finanznachrichten.de/suche/uebersicht.htm?suche={}'
stocks = ['nvidia']

try:
    for stock in stocks:
        now,soup=get_content(url.format(stock))
        #i.span.text ist die Uhrzeit, falls heute; ansosnten der Wochentag
        #i.span.get('title') ist None, falls heute; ansonsten das Datum und die Uhrzeit
        daten = get_news(soup)

        now,soup=get_nextpagecontent(0, url.format(stock))
        daten1 = get_news(soup)
        daten = daten.append(daten1, ignore_index=True)

        now,soup=get_nextpagecontent(1, url.format(stock))
        daten2 = get_news(soup)
        daten = daten.append(daten2, ignore_index=True)

        now,soup=get_nextpagecontent(2, url.format(stock))
        daten3 = get_news(soup)
        daten = daten.append(daten3, ignore_index=True)
except:
    for stock in stocks:
        now, soup = get_content(url.format(stock))
        # i.span.text ist die Uhrzeit, falls heute; ansosnten der Wochentag
        # i.span.get('title') ist None, falls heute; ansonsten das Datum und die Uhrzeit
        daten = get_news(soup)

        now, soup = get_nextpagecontent(0, url.format(stock))
        daten1 = get_news(soup)
        daten = daten.append(daten1, ignore_index=True)

        now, soup = get_nextpagecontent(1, url.format(stock))
        daten2 = get_news(soup)
        daten = daten.append(daten2, ignore_index=True)

        now, soup = get_nextpagecontent(2, url.format(stock))
        daten3 = get_news(soup)
        daten = daten.append(daten3, ignore_index=True)

#daten.to_csv('./tmp/scraped_news.csv', encoding='utf-8-sig')
daten.to_csv('./tmp/scraped_news.csv')
print('Extraction successful!')