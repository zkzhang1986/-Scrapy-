# 《精通scrapy网络爬虫》 第8章代码 
步骤1：继承spider创建BooksSpider类（即创建爬虫）

步骤2：为spider取名 

步骤3：指定起始爬取点 
（前面3步由命令 scrapy genspider 命令完成）

步骤4：实现书籍列表页面解析函数

步骤5：实现书籍页面的解析函数

my_exporters.py 以excel格式导出的Exporter

---------
小技巧：cd 用法 CD [/D] [drive:][path]

cd /d d:\project\toscrape_book

cd toscrape_book\spiders

使用 /D 开关，除了改变驱动器的当前目录之外，
还可改变当前驱动器。

# 第12章 存入数据库 
## 12.1 SQLite
    2020-03-17 
    在 pipelines.py 中实现SQLitePipeline.
    常用命令：
    创建数据库：sqlite3 dbname.db (当前目录下)
    更多见：https://www.runoob.com/sqlite/sqlite-tutorial.html
## 12.2 MySQL
    使用python连接mysql，是需要三方包的，目前主流的方式就是pymysql 和 mysqlclient（也就是Python3版本的MySQLdb）。
    还有一个cymysql（fork of pymysql with optional C speedups）
    1. 两个库的作者是同一个人INADA Naoki, pip库邮箱都指向mailto:songofacandy@gmail.com
    2. PyMySQL的代码人员methane说mysqlclient速度更快及PyMySQL的应用场景
    那么，我们应该如何选择呢？首先，需要了解下这两个包的大概。
    一、pymysql
      1） 纯Python实现的，安装简单（直接pip安装）
      2)  由于纯Python实现的，可以很好的跟gevent框架结合
    二、mysqlclient
    1）是一个C扩展模块,编译安装可能会导致报各种错误,明显没有pymysql方便
    2）速度快；
    
    大项目感觉pymysql还是有点鸡肋啊，在此建议，使用MySQLdb。
    https://blog.csdn.net/u011510825/article/details/86632598
    
    adbapi.py 为异步测试
    
    
## 12.3 MongoDB
    见代码
    class MongoDBPipeline 类
    注意：
    1.item.py
    需要加上：_id = scrapy.Field()
    如果不加会包 keys error
    2.isinstance() 
    函数来判断一个对象是否是一个已知的类型，类似 type()
    语法：
    isinstance(object, classinfo)
    参数：
    object -- 实例对象。
    classinfo -- 可以是直接或间接类名、基本类型或者由它们组成的元组。
    返回值：
    如果对象的类型与参数二的类型（classinfo）相同则返回 True，否则返回 False。。
    在 insert_db() 方法中，判断类型写法如下：
    if isinstance(item,type(item)):
        pass
     书中是 if isinstance(item,item) 
     会报 TypeError: isinstance() arg 2 must be a type or tuple of types
    
    
## 12.4 Redis
    见代码
    class RedisPipeline 类
    跟 Mongodb 写法差不多。
    
