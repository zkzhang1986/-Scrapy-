# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ToscrapeBookPipeline(object):
    def process_item(self, item, spider):
        return item

# 数据处理：把英文转成对应的数字
# 记得要在settings.py中设置
# ITEM_PIPELINES = {
#     'toscrape_book.pipelines.BookPipeline': 300,
# }

class BookPipeline(object):
    review_rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def process_item(self, item, spider):
        # 取到英文的rating数据
        rating = item.get('review_rating')
        if rating:
            # 取对应的英文转成数字
            item['review_rating'] = self.review_rating_map[rating] # review_rating_map[rating]字典的用法

        return item

# 数据过滤去重
from scrapy.exceptions import DropItem

class DuplicatesPipline(object):
    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        # 取出name
        name = item['name']
        # 判断name是否在book_set中
        if name in self.book_set:
            raise DropItem("Duplicat book found: %s" % item)
        else:
            self.book_set.add(name)
            return item