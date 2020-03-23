# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ToscrapeBookPipeline(object):
    def process_item(self, item, spider):
        return item

# 2020-03-23
# 第12章 12.2 MYSQL 实现数据写入到 MYSQL 数据库中
# 在 pipleines.py 中实现 MySQLPipeline 代码如下：

import  MySQLdb
class MySQLPipeline(object):
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME','scrapy_default')
        host = spider.settings.get('MYSQL_HOST','localhost')
        port = spider.settings.get('MYSQL_PORT',3306)
        user = spider.settings.get('MYSQL_USER','root')
        password = spider.settings.get('MYSQL_PASSWORD','Zhangzk123')
        self.db_conn = MySQLdb.connect(host=host, port=port, db=db,
                                       user=user, password=password)

        self.db_cur = self.db_conn.cursor()

    def close_spider(self,spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self,item,spider):
        self.insert_db(item)
        return item

    def insert_db(self,item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock']
        )
        sql = 'INSERT INTO books VALUES(%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql,values)


# 2020-03-17
# 第12章 12.1 SQLite   实现数据写入到SQLite数据库中
# 在 pipleines.py 中实现 SQLitePipeline 代码如下：

import sqlite3
class SQLitePipeline(object):

    # open_spider 方法在开始爬取数据前被调用，
    # 在该方法中通过调用 spider.settings 对象读取用户在配置文件中指定的数据库，然后建立与数据库的链接，
    # 将得到的 connection 对象和 Cursor 对象分别赋值给 self.db_conn 和 self.db_cur, 以便之后使用
    def open_spider(self,spider):
        db_name = spider.settings.get('SQLITE_DB_NAME','scrapy_defaut.db')

        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    # 关闭爬虫时执行调用。
    # close_spider 方法在爬取完全部数据后被调用，
    # 在该方法中，调用连接对象的 commit 方法将之前所有插入数据操作一次性提交给数据库，然后关闭连接对象。
    def close_spider(self,spider):
        # 操作数据库
        # 提交数据到数据库
        self.db_conn.commit()
        # 关闭数据库
        self.db_conn.close()

    # procrss_item 方法处理抓取到的每一项数据，
    # 在该方法中调用 inser_db 方法，执行插入数据操作的 SQL 语句。
    # 需要注意在 inser_db 中并没有调用连接对象 commit 的方法，意味着每此时数据没有实际写入数据库。
    # 如果每插入一条数据都调用一次 commit 方法，会严重降低程序执行效率，并且我们对数据插入数据库实时性并没有什么要求，
    # 因此可以在完全爬取完数据后再调用 commit 方法
    def process_item(self,item,spider):
        self.inser_db(item)
        return item

    # inser_db 方法执行插入数据操作
    def inser_db(self,item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )

        sql = 'INSERT INTO books VALUES(?,?,?,?,?,?)'
        self.db_cur.execute(sql,values)

# 第8章 内容
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