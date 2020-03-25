# 在 python 中 pymysql 和 MySQLdb 都可以用，但在性能上MySQLdb 比 pymysql 快，更适合大型项目中。
# import pymysql

import MySQLdb

# 连接数据库
conn = MySQLdb.connect(host='localhost', db='scrapy_db',
                       user='root', password='Zhangzk123', charset='utf8')
# 创建对象
cur = conn.cursor()

# 创建数据表
# cur.execute('CREATE TABLE person (name VARCHAR(32), age INT, sex char(1))')

# 插入一条数据
cur.execute('INSERT INTO person VALUES(%s,%s,%s)',('刘硕', 34, 'M'))

# 保存变更，commit 后数据才被实际写入数据库
conn.commit()

# 查询
cur.execute('select * from person')
print("search result：",cur.fetchone())

# 关闭数据库
conn.close()
