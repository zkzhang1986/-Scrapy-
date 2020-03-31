#《精通scrapy网络爬虫》
## 第 1 章 初识 Scrapy
### 1.1 网络爬虫是什么
    略
### 1.2  Scrapy 简介及安装
        scrapy 是使用 Python 语言（基于 Twisted 框架）编写的开源网络爬虫框架。
        安装：pip install scrapy （如果安装失败自行百度。依赖库有 lxml、 pyOpenSSL 、 Twisted 、pywin32）
        判断是否安装成功：
        >>> import scrapy
        >>> scrapy.version_info
        帮助： scrapy -h      
### 1.3 编写第一个 Scrapy 爬虫 --重点
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
### 1.4 本章小结
    略

## 第 2 章 编写 Spider
### 2.1 Scrapy 框架结构及工作原理 --重点
    ENGINE: 引擎，框架核心，其他组件在其控制下协同工作--内部组件
    SCHEDULER: 调度器，负责对 SPIDER 提交的下载请求进行调度--内部组件
    DOWNLOADER: 下载器，负责下载页面（发送 HTTP 请求/接收 HTTP 响应）--内部组件
    SPIDER: 爬虫，负责提取页面中的数据，并产生对新页面的下载请求--用户实现
    MIDDLEWARE: 中间件，负责对 Request 对象和 Response 对象进行处理--可选组件
    ITEMPIPELINE: 数据管道，负责对爬取到数据进行处理--可选组件   
### 2.2 Request 和 Response 对象 --重点
    2.2.1 Request 对象 官方：https://docs.scrapy.org/en/latest/topics/request-response.html#request-objects
          scrapy.http.Request(url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, 
                             encoding='utf-8', priority=0, dont_filter=False, errback=None, flags=None, cb_kwargs=None)
          常用参数： url， 
                    method(请求方式，默认 GET)， 
                    headers(请求头部，dict 类型)，
                    body（请求正文 bytes 或 str 类型）， 
                    meta （Request的元数据字典，dict 类型，用于给框架中其他组件传递信息，比如中间件 ItemPipeline。
                          其他组件可以使用 Request对象 meta 属性访问该元素数据字典（request.meta）, 
                          也可以用于给响应处理函数传递信息）， 
                    dont_filter （过滤）                              
    2.2.2 Response 对象 官方：https://docs.scrapy.org/en/latest/topics/request-response.html#response-objects
          scrapy.http.Response(url, status=200, headers=None, body=b'', flags=None, request=None, certificate=None
          常用属性：xpath(query) ;
                    css(query);
                    urljoin(url) 用于构造绝对 url;
          子类有：
                TextResponse
                HTMLResponse
                XmlResponse
### 2.3 Spider 开发流程 --重点
    Spider.py 写法：
                    a.继承 scrapy.Spider
                    b.为 Spider 取名 即(name = ???)
                    c.设定起始爬取点 即(start_urls = [])也可以通过重新 def start_requests(self):来代替 start_urls = []
                                    具体可以看看原码
                    d.实现页面解析函数 即(def parse(self,response):)
### 2.4 本章小结
    略
    
## 第 3 章 使用 Selector 提取数据
### 3.1 Selector 对象
    Selector 基于 lxml 库构建，并简化了 Api（BeautifulSoup） 接口,集两者优点于一身。
    scrapy.selector.Selector（response = None，text = None，type = None，root = None，** kwargs ）
    3.1.1 创建对象
        方法1：
        from scrapy.selector import Selector
        text = """ 解析内容 """
        selector = Selector(text = text)
        方法2：
        from scrapy.selector import Selector
        from scrapy.http import HtmlResponse
        body = """" 解析内容 """
        response = HtmlResponse(url,body=body,encoding='utf-8')
        selector = Selector(response = response)
        或 response.selector
    3.1.2 选中数据
        调用 Selector 对象的 xpath 或 css 方法，返回的是  SelectorList 对象。可以使用 for 迭代访问每一个 Selector 对象。
    3.1.3 提取数据
        extract()
        re()
        extract_first()  SelectorList专有
        re_first()       SelectorList专有
### 3.2 Response 内置 Selector
    可以直接使用 Response 对象内置的 Selector 对象
    response.selector
### 3.3 XPath --重点
### 3.4 CSS选择器 --重点
### 3.5 本章小结
    略

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