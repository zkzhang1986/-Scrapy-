# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ToscrapeBookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    # 使用Field()元数据封装数据
    name = scrapy.Field() # 书名
    price = scrapy.Field() # 价格
    review_rating = scrapy.Field() # 评价等级（1~5 星）
    review_num = scrapy.Field() # 评价数量
    upc = scrapy.Field() # 产品编码
    stock = scrapy.Field() # 库存数量
    # 当存储在 mongodb 数据库中时，需要加上这么一句
    _id = scrapy.Field()
