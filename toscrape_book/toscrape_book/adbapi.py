# 异步测试
from twisted.internet import reactor, defer
from twisted.enterprise import  adbapi
import threading

# 建立数据库连接
# adbapi.ConnectionPool 方法可以创建一个数据库连接池对象，其中包含多个连接对象，每个连接对象在独立的线程工作。
# adbapi 只是提供了异步访问数据库的编程框架，在其内部依然使用MySQLdb，sqlite3 这样的库访问。
# ConnectionPool 方法第1个参数就是用来指定使用哪个库访问数据。其他参数在创建连接对象时使用。
dbpool = adbapi.ConnectionPool('MySQLdb',host='localhost',database='scrapy_db',
                               user='root',password='Zhangzk123')

def insert_db(tx,item):
    print('In Thread:',threading.get_ident())
    sql = 'INSERT INTO person VALUES (%s,%s,%s)'
    tx.execute(sql,item)

for i in range(1000):
    item = ('person%s'% i,25,'M')
    # dbpool.runInteraction(insert_db,item) 以异步方式调用 insert_db 函数，dbpool 会选择连接池中的一个连接对象在独立线程中
    # 调用 insert_db，其中 参数 item 会被传给 insert_db 的第二个参数，传给 insert_db 的第一个参数是一个 Transaction 对象，
    # 其接口 与 Cursor 对象类似，可以调用 execute 方法 执行 SQL 语句，insert_db 执行完后，连接对象会自动调用 commit 方法
    dbpool.runInteraction(insert_db,item)

reactor.run()