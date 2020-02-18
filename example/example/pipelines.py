# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ExamplePipeline(object):
    def process_item(self, item, spider):
        return item

# 以下重写
class PriceConverterPipeline(object):
    # 英镑兑换人民币汇率
    exchange_rate = 8.5309
    def process_item(self, item, spider):
        # 提取item中的price字段中的£后面的值然乘以汇率
        price = float(item['price'][1:])*self.exchange_rate
        # 保留2位小数，赋值回price字段
        item['price']='￥%.2f'% price
        return item

# 数据过滤去重
from scrapy.exceptions import DropItem

class DuplicatesPipline(object):
    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['name']
        if name in self.book_set:
            raise DropItem("Duplicat book found: %s" % item)

        self.book_set.add(name)
        return item

# # 将数据保存在mongodb
# import pymongo
# from scrapy.item import Item
class MongoDBPipeline(object):
    # 设置mongodb路径
    DB_URL = 'mongodb://localhost:27017/'
    # 设置数据库名
    DB_DATE = 'scrapy_data'

    def open_spider(self, spider):
        # 数据处理之前打开数据库
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_DATE]

    def close_spider(self, spider):
        # 数据处理之后关闭数据库
        self.client.close()

    def process_item(self, item, spider):
        # 数据处理
        collection = self.db[spider.name]
        # 如果item是Item对象就把item转成字典
        post = dict(item) if isinstance(item, Item) else item
        # 把post插入到mongdb数据库中
        collection.insert_one(post)
        return item

# 将数据保存在mongodb 重写
from scrapy.item import Item
import pymongo

# 在settings中设置数据库信息
# MONGO_DB_URI = 'mongodb://localhost:27017/'
# MONGO_DB_NAME = 'scrapy_data1'

class MongoDBPipeline1(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_DB_URI'),
            mongo_db = crawler.settings.get('MONGO_DB_NAME')
        )

    # @classmethod
    # def from_crawler(cls, crawler):
    #    # 读取配件文件中的MongoDB_URI，MongoDB_NAME值
    #     以下写法错误 书中P56
    #     cls.mongo_uri = crawler.settings.get('MONGO_DB_URI')
    #     cls.mongo_db = crawler.settings.get('MONGO_DB_NAME')
    #     return cls

    def open_spider(self, spider):
        # 处理数据之间前打开数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 处理数据之后关闭
        self.client.close()

    def process_item(self, item, spider):
        # 处理数据
        self.collection = self.db[spider.name]
        self.post = dict(item) if isinstance(item, Item) else item
        self.collection.insert_one(self.post)
        return item