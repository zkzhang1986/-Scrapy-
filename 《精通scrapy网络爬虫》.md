#《精通scrapy网络爬虫》
## 第 1 章 初识 Scrapy
    1.1 网络爬虫是什么
    1.2  Scrapy 简介及安装
        scrapy 是使用 Python 语言（基于 Twisted 框架）编写的开源网络爬虫框架。
        安装：pip install scrapy （如果安装失败自行百度。依赖库有 lxml、 pyOpenSSL 、 Twisted 、pywin32）
        判断是否安装成功：
        >>> import scrapy
        >>> scrapy.version_info
        帮助： scrapy -h      
    1.3 编写第一个 Scrapy 爬虫
        流程：
        1.3.1 项目需求：
            需要达到什么效果,例如取哪些字段值
        1.3.2 创建项目
            命令：scrapy startproject < project_name >--创建一个爬虫项目 <project_name--项目名>
            帮助：scrapy startproject -h
        1.3.3 分析页面
            分析字段值对应的页面元素
        1.3.4 实现 Spider
            命令：scrapy genspider [options] < spider_name > < domain > --创建一个爬虫（在startproject里创建）
            帮助：scrapy genspider -h
            spider 在 project_name/spiders 目录下
            spider 代码解释 https://github.com/zkzhang1986/-Scrapy-/blob/master/example/example/spiders/book_spider.py
            
            name 属性： 一个 Scrapy 项目中可能有多个爬虫，每个爬虫的 name 属性是其自身的唯一标识，
                        在同一个项目中不能有同名的爬虫。                        
            start_urls 属性：一个爬虫总要从某个（某些）页面开始爬取，这样的页面称为起始爬取点，
                            start_urls 属性用来设置一个爬虫的起始爬取点
            parse 方法：当一个页面下载完成后，Scrapy 引擎会回调一个我们指定的页面解释函数（默认为 parse 方法）解析页面。
                        一个页面的解析函数通常需要完成以下两个任务：
                        a.提取页面中的数据（使用Xpath 或 CSS 选择器）
                        b.提取页面中的链接，并产生对链接页面的下载请求。
             注意：页面解释函数通常被实现以个生成器函数，每一项从页面中提取的数据以及每一个对链接页面的下载请求都由 yield 语句
                   提交给 Scrapy 引擎
        1.3.5 运行爬虫
            命令：scrapy crawl < spider > -o < file > --运行爬虫导出数据
            帮助：scrapy -h
    1.4 本章小结
## 第 2 章 编写 Spider
## 第 3 章 使用 Selector 提取数据
## 第 4 章 使用 Item 封装数据
## 第 5 章 使用 Item Pipeline 处理数据
## 第 6 章 使用 LinkExtractor 提取链接
## 第 7 章 使用 Exporter 导出数据
## 第 8 章 项目练习
## 第 9 章 下载文件和图片
## 第 10 章 模拟登录
## 第 11 章 爬取动态页面
## 第 12 章 存入数据库
## 第 13 章 使用 HTTP 代理
## 第 14 章 分布式爬虫 