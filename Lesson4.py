from lxml import html
from pprint import pprint
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

# -------------lena.ru---------------
response = requests.get('https://lenta.ru/rubrics/travel/')
dom = html.fromstring(response.text)
items = dom.xpath("//div[@class='item']")
lenta_news = []

for item in items:
    lenta = {}
    lenta['link'] = item.xpath('.//@href')
    lenta['title'] = item.xpath('.//text()')[1]
    lenta['date'] = item.xpath('.//text()')[0]
    lenta_news.append(lenta)

pprint(lenta_news)

# -------------mail.ru---------------
response = requests.get('https://yandex.ru/news/')
dom = html.fromstring(response.text)
items = dom.xpath("//a[contains(@href, 'rubric=index') and @class='mg-card__link']")
yandex_news = []

for item in items:
    yandex = {}
    yandex['link'] = item.xpath('.//@href')
    yandex['title'] = item.xpath('.//text()')[0]
    yandex['date'] = item.xpath(".//span[@class='news-snippet-source-info__time']/text()")

    yandex_news.append(yandex)

pprint(yandex_news)

