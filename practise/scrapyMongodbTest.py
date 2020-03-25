# Mongodb 测试
from pymongo import MongoClient

# 连接 mongodb，得到一个客户端对象
client = MongoClient('mongodb://localhost:27017')

# 获取名为 scrapy_db 的数据库对象
db = client.scrapy_db

# 获取名为 person 的集合对象
collection = db.person

doc = {
    'name':'刘硕',
    'age':34,
    'sex':'M'
}

# 将文件插入集合
collection.insert_one(doc)

# 关闭客户端
client.close()