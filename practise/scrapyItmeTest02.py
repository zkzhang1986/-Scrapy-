# 《精通 scrapy 网络爬虫》第4章 第1节（即4.1）Item 和 Field 实例
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class BookItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()

if __name__ == '__main__':
    book1 = BookItem(name='Needful Things', price='45.0')
    print(book1)
    book2 = BookItem()
    print(book2)
    book2['name'] = 'Life of Pi'
    book2['price'] = 32.5
    print(book2)
    print(book1['name'])
    print(book1.get('price',60))
    print(list(book1.items()))
    print(list(book1.fields))
    print(list(book1.keys()))



