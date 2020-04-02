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
    Xpath 即 XML 路径语言
    3.3.1 基础语法
    https://blog.csdn.net/u010553139/article/details/104006117
    实例代码：https://github.com/zkzhang1986/-Scrapy-/blob/master/practise/scrapySelectorXpathTest.py
    表达式	    描述
    /	        选中文档的根（root）
    .	        选中当前节点
    ..	        选中当前节点的父节点
    ELEMENT	    选中子节点中所有ELEMENT元素节点
    //ELEMENT	选中后代节点中所ELEMENT元素节点
    *	        选中所有元素子节点
    text()	    选中所文本子节点
    @ATTR	    选中名为ATTR的属性节点
    @*	        选中所有属性节点
    [谓语]	    谓语用来查找特定的节点或者包含某个特定值的节点
    3.3.2 常用函数
    string(arg):返回参数的字符串值
    contaions(str1,str2):判断 str1 中是否包含 str2 ，返回布尔值
### 3.4 CSS选择器 --重点
    实例代码：https://github.com/zkzhang1986/-Scrapy-/blob/master/practise/scrapySelectorCSSTest.py
    表达式 
    表达式	            描述	                                                例 子
    *                   选中所有元素	                                            *
    E                   选中E元素	                                            p
    E1,E2	            选中E1和E2元素	                                        div,pre
    E1 E2	            选中E1后代元素中的E2元素	                                div p
    E1>E2	            选中E1子元素中的E2元素	                                div>p
    E1+E2	            选中E1兄弟元素中的E2元素	                                p+strong
    .class	            选中class属性包含class的元素	                            .info
    #ID	                选中id属性为ID的元素	                                    #main
    [ATTR]	            选中包含ATTR属性的元素	                                [href]
    [ATTR=VALUE]	    选中包含ATTR属性且值 为 VALUE的元素	                    [method=post]
    [ATTR~=VALUE]	    选中包含ATTR属性且值 包 含VALUE的元素	                    [class~=clearfix]
    E:nth-child(n)	    选中E元素，且该元素必须是父元素的第n个子元素	            a:nth-child(1)
    E:nth-last-child(n)	选中E元素，且该元素必须是父元素的**（倒数）**第n个子元素	a:nth-last-child(2)
    E:first-child	    选中E元素，且该元素必须是父元素的第一个子元素	            a:first-child
    E:last-child	    选中E元素，且该元素必须是父元素的**（倒数）**第一个子元素	a:last-child
    E:emty	            选中没有子元素的E元素	                                div:empty
    E::text	            选中E元素的文本节点（Text Node）	                        p::text
### 3.5 本章小结
    略

## 第 4 章 使用 Item 封装数据
### 4.1 Item 和 Field --重点
    Item 基类 自定义数据类（如 BookItem）的基类
    Field 类  用来描述自定义数据类包含哪些字段（如 name，price 等）
        class BookItem(scrapy.Item):
            name = scrapy.Field()
            price = scrapy.Field()
### 4.2 扩展 Item 子类 --重点
    根据需求对已有自定义数据类（Item 子类）进行扩展。
    如：在example项目中又有一个新的 Spider ，他负责在另外的图书网站爬取国外书籍（中文翻译版）的信息。
        此类数据的信息比之前多了一个译者字段。此时可以继承 BookItem 类定义一个 ForeignBookItem 类
        class ForeignBookItem(BookItem):
            translator = Field()
### 4.3 Field 元数据
    实例代码：https://github.com/zkzhang1986/-Scrapy-/blob/master/practise/scrapyItemFieldTest.py
    这节没深入了解，只知道 Field 是字典类型   汗
### 4.4 本章小结
    略

## 第 5 章 使用 Item Pipeline 处理数据 --重点
    Item Pipeline 的典型应用：清洗数据；验证数据的有效性；过滤掉重复数据；将数据存入数据库
### 5.1 Item Pipelin --重点
    官方手册：https://docs.scrapy.org/en/latest/topics/item-pipeline.html
    5.1.1 实现 Item Pipeline 
        例：
        # 第 5 章 5.1.1实现英镑与人民币转换
        class PriceConverterPipeline(object):
            # 英镑兑换人民币汇率
            exchange_rate = 8.5309
            def process_item(self, item, spider):
                # 提取item中的price字段中的£后面的值然乘以汇率
                price = float(item['price'][1:])*self.exchange_rate
                # 保留2位小数，赋值回price字段
                item['price']='￥%.2f'% price
                return item
        注：一个 Item Pipeline 不需要继承特点基类，只需要实现某些特定的方法，例如 process_item、open_spider、close_spider。
            一个 Item Pipeline 必须实现一个 process_item(item,spider) 方法，该方法用来处理每一项由 Spider 爬到的数据，
            其中的两个参数：
            Item：爬到的一项数据（Item 或字典）
            Spider：爬取此项数据的 Spider 对象。
            补充说明：1.如果 process_item 在处理某项 item 时返回了一项数据（Item 或字典），
                    返回的数据会传递给下一级 Item Pipeline （如果有）继续处理。
                    2.如果 process_item 在处理某项 item 时抛出（raise）一个 DropItem 异常（scrapy.exception.DropItem）,
                    该项 item 便会被抛弃，不再传递给后面的 Item Pipeline 处理，也不会导出文件。通常在检测到无效数据或
                    想要过滤数据时，抛出 DropItem 异常。
        除 process_item 外另外常用方法：
            open_spider(self,spider): Spider 打开时（处理数据前）回调该方法，通常该方法用于在开始处理数据之前完成某些初始化工作，
                                      如：连接数据库。
            close_spider(self,spider): Spider 关闭时（处理数据后）回调该方法，通常该用法用于在处理完所有数据之后完成某些清理工作，
                                      如：关闭数据库。
            from_crawler(cls,crawler):创建 Item Pipeline 对象时回调该类方法。通常，在该方法中通过 crawler.settings.get 读取配置，
                                      根据配置创建 Item Pipeline 对象。
    5.1.2 启用 Item Pipeline 
        在 settings.py 中配置 代码见：https://github.com/zkzhang1986/-Scrapy-/blob/master/example/example/settings.py
        # Configure item pipelines
        # See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
        ITEM_PIPELINES = {
            # 'example.pipelines.ExamplePipeline': 300,
            # 激活价格换算
            'example.pipelines.PriceConverterPipeline': 302,
            # 激活去重
            'example.pipelines.DuplicatesPipline': 301,
            # 把数据保存到MongoDB
            # 'example.pipelines.MongoDBPipeline':303,
            # 把数据保存到MongoDB 用from_crawler 函数设置
            # 'example.pipelines.MongoDBPipeline1': 304,
        }       
### 5.2 更多例子
    5.2.1 过滤重复
        from scrapy.exceptions import DropItem
        class DuplicatesPipline(object):
            def __init__(self):
                self.book_set = set()       
            def process_item(self, item, spider):
                name = item['name']
                # 如果 name 存在用 raise 抛出 DropItem 异常。
                if name in self.book_set:
                    raise DropItem("Duplicat book found: %s" % item)        
                self.book_set.add(name)
                return item
    5.2.2 将数据存入在 MongoDB
        代码见：https://github.com/zkzhang1986/-Scrapy-/blob/master/example/example/pipelines.py    
### 5.3 本章小结
    略

## 第 6 章 使用 LinkExtractor 提取链接
    应用场景：在爬取一个网站时，需要爬取的数据通常分布在多个页面中，每个页面包含一部分数据以及到其他页面的链接。
    提取链接有 Selector 和 LinkExtractor 提取。
### 6.1 使用 LinkExtractor
    from scrapy.linkextractors import LinkExtractor
    # 创建 LinkExtractor 对象
    le = LinkExtractor(restrict_css='ul.pager li.next')
    # 调用 LinkExtractor 对象的 extract_list() 方法传入一个 Response 对象，返回一个 link 列表。
    links = le.extract_links(response)
    # print(type(links),links)
    if links:
        # 用links[0]获取的Link对象属性是绝对链接地址，无需要用response.urljoin拼接
        next_url = links[0].url
        yield scrapy.Request(next_url, callback=self.parse)
    1.导入 LinkExtractor 位于 scrapy.linkextractors
    2.创建 LinkExtractor 对象。le = LinkExtractor(restrict_css='ul.pager li.next') 描述出下一页链接所在的区域（在 li.next 下）
    3.调用 LinkExtractor 对象的 extract_list() 方法传入一个 Response 对象，该方法依据创建对象时所描述的提取规则，在 Response对象
        所包含的页面中提取链接，最终返回一个列表，其中的每一个元素都是一个 link 对象，即提取到的一个链接。
    4.判断是否有 link 值。由于本例中，下一页链接只有一个链接，因此用links[0]获取对象，link 对象的 url 属性就是链接页面的绝对 url。
    5.用 yield scrapy.Request()继续请求。     
### 6.2 描述提取规则
    实例代理：https://github.com/zkzhang1986/-Scrapy-/blob/master/practise/scrapyLinkExtractorTest1.py
    官方说明：https://docs.scrapy.org/en/latest/topics/link-extractors.html
    LxmlLinkExtractor(allow=(), deny=(), allow_domains=(), deny_domains=(), deny_extensions=None, restrict_xpaths=(), 
                      restrict_css=(), tags=('a', 'area'), attrs=('href', ), canonicalize=False, unique=True, 
                      process_value=None, strip=True)
    参数说明：
    # allow：
         接收一个正则表达式或正则表达式列表，提取绝对值url与正则表达式匹配的链接，
         如果该参数为空（默认），就提取全部链接
    # deny：
        接收一个正则表达式或正则表达式列表，与allow相反，排除绝对值url与正则表达式匹配的链接.
    # allow_domains：
        接收一个域名或一个域名列表，提取到指定域的链接
    # deny_domains：
        接收一个域名或一个域名列表，与allow_domains相反，排除指定域的链接
    # restrict_xpaths：
        接收一个XPath表达式或一个XPath表达列表，提取XPath表达式选中区域下的链接
    # restrict_css：
        接收一个CSS表达式或一个CSS选择器列表，提取CSS选择器选中区域下的链接
    # tags：
        接收一个标签（字符串）或一个标签列表，提取指定标签内的链接，默认为['a','area']
    # attrs：
        接收一个属性（字符串）或一个属性列表，提取指定属性内的链接，默认为['href].
    # process_value：
        接收一个形如func(value)的回调函数。
        如果传递了该参数，LinkExtractor将调用该回调函数对提取的每一个链接（如a标签的href链接）进行处理，
        回调函数正常情况下应该返回一个字符串（处理结果），想要抛弃所处理结果的链接时，返回None。
### 6.3 本章小结
    略
    
## 第 7 章 使用 Exporter 导出数据
    负责导出数据的组件被称为Exporter(导出器)
    内置导出器：JSON(JsonItemExporter),JSON lines(JsonLinesItemExporter),CSV(CsvItemExporter),XML(XmlItemExporter),
                Pickle(PickleItemExporter),Msrshal(MsrshalItemExporter)
### 7.1 指定如何导出数据
    在导出数据时，需向 Scrapy 爬虫提供以下信息：
    导出文件路径；
    导出数据格式（即选用哪个Exporter）
    如何导出数据：
    1、通过命令行参数指定；
    2、通过配置文件指定；
    7.1.1 命令行参数：
        例：scrapy crawl books -o books.csv 其中：-o books.csv 导出文件路径 -t 参数指定导出格式。
        scrapy crawl books -t csv -o books.csv 
        默认配置文件：FEED_EXPORTER_BASE
        位置：scrapy.settings.default-settings
        DOWNLOAD_HANDLERS_BASE = {
        'data': 'scrapy.core.downloader.handlers.datauri.DataURIDownloadHandler',
        'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
        'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
        'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
        's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
        'ftp': 'scrapy.core.downloader.handlers.ftp.FTPDownloadHandler',
        }
        用户配置文件：FEED_EXPORTERS
        位置：settings.py
        # 添加新的导出数据格式
        FEED_EXPORTERS = {'xls':'example.my_exporters.ExcelItemExporter'}
    7.1.2 配置文件
        FEED_URI: 导出文件路径
        FEED_FORMAT:导出数据格式
        FEED_EXPORT_ENCODING:导出文件编码
        FEED_EXPORT_FIELDS：导出数据包含的字典
        FEED_STORAGES：用户自定义Exporter字典，添加新的导出数据格式时使用
       
### 7.2 添加导出数据格式
    代码见：https://github.com/zkzhang1986/-Scrapy-/blob/master/example/example/my_exporters.py
    # 以excel格式导出的Exporter
    from scrapy.exporters import BaseItemExporter
    import xlwt
    class ExcelItemExporter(BaseItemExporter):
        def __init__(self, file, **kwargs):
            self._configure(kwargs)
            self.file = file
            self.wbook = xlwt.Workbook()
            self.wsheet = self.wbook.add_sheet('scrapy')
            self.row = 0   
        def finish_exporting(self):
            self.wbook.save(self.file)   
        def export_item(self, item):
            fields = self._get_serialized_fields(item)
            for col, v in enumerate(x for _,x in fields):
                self.wsheet.write(self.row,col,v)
            self.row += 1
### 7.3 本章小结
    略

## 第 8 章 项目练习
    见代码：https://github.com/zkzhang1986/-Scrapy-/tree/master/toscrape_book
### 8.1 项目需求
### 8.2 页面分析
### 8.3 编码实现
### 8.4 本章小结
    略

## 第 9 章 下载文件和图片
### 9.1 FilesPipeline 和 ImagesPipeline
    
### 9.2 项目实例：爬取 matplotlib例子源码文件
### 9.3 项目实例：下载 360 图片
### 9.4 本章小结
    略

## 第 10 章 模拟登录
### 10.1 登录实质
### 10.2 Scrapy 模拟登录
### 10.3 识别验证码
### 10.4 Cookie登录
### 10.5 本章小结
    略

## 第 11 章 爬取动态页面
### 11.1 Splash 渲染引擎
### 11.2 在 Scrapy 中使用 Splash
### 11.3 项目实例：爬取 toscrape 中的名人名言
### 11.4 项目实例：爬取京东商城中的书籍信息
### 11.5 本章小结
    略

## 第 12 章 存入数据库
### 12.1 SQLite
### 12.2 MySQL
### 12.3 MongoDB
### 12.4 Redis
### 12.5 本章小结
    略

## 第 13 章 使用 HTTP 代理
### 13.1 HttpProxyMiddleware
### 13.2 使用多个代理
### 13.3 获取免费代理
### 13.4 实现随机代理
### 13.5 项目实例：爬取豆瓣电影信息
        免费代理根本用不了。
### 13.6 本章小结

## 第 14 章 分布式爬虫 
### 14.1 Redis 的使用
### 14.2 scrapy-redis 源码分析
### 14.3 使用scrapy-redis 进行分布式爬取
### 14.4 本章小结
    略