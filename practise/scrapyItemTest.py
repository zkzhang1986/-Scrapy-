# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    tags = scrapy.Field()
    # 字段的序列化器功能
    last_updated = scrapy.Field(serializer=str)

if __name__ == '__main__':
    product = Product(name='Desktop PC', price=1000)
    print(type(product),product)
    print(product['name'])
    print(product['price'])
    print(product.get('last_updated','not set'))
    print('name' in product)
    print(product.fields)
    print('last_updated' in product.fields)

    #设置字段值
    product['tags'] = 'today'
    print(product)
    print(product.keys())
    print(product.items())


