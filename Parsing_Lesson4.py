from lxml import html
from pprint import pprint
import requests

# 1 - Новоти Yandex.ru

url = 'https://yandex.ru/news/'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/90.0.4430.212 Safari/537.36'}

response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
yandex = dom.xpath("//a[contains(@href, 'rubric=Moscow')and @class='mg-card__link']/ancestor::article")

yandex_news = []
for item in yandex:
    article = {}
    text = item.xpath(".//h2[@class='mg-card__title']/text()")
    link = item.xpath(".//a[@class='mg-card__link']/@href")
    time = item.xpath(".//span[@class ='mg-card-source__time']/text()")
    source = item.xpath(".//a/text()")

    article['text'] = text
    article['link'] = link
    article['time'] = time
    article['source'] = source

    yandex_news.append(article)

pprint(yandex_news)

# 2 - Новости lenta.ru

url = 'https://lenta.ru/'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/90.0.4430.212 Safari/537.36'}

response = requests.get(url, headers=header)

dom = html.fromstring(response.text)

lenta = dom.xpath("//div[@class='b-yellow-box__wrap']/div[position()>2]")

lenta_news = []
for item in lenta:
    article = {}
    text = item.xpath(".//a/text()")
    link = item.xpath(".//a/@href")
    time = item.xpath("//../@datetime[1]")
    source = 'Lenta,ru'

    article['text'] = text
    article['link'] = link
    article['time'] = time
    article['source'] = source

    lenta_news.append(article)

pprint(lenta_news)
