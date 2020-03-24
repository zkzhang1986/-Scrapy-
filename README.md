# 《精通scrapy网络爬虫》 
  example文件夹内容： 第一章至第七章代码 
  
  practise文件夹内容：书本中的练习

  toscrape_book 文件夹内容：第八章 代码（ps在原代码基础增加了：去掉重复、以xls格式导出，选择器用的是css）

  matplotlib_examples 文件夹内容 ：第九章 案例中下载matplotlib网站文件

  so_image 文件夹内容：第9章 第二节 下载360图片 （为什么只下载到第一页呢？？？没实现翻页）

  scrapy_10 文件夹内容：第10章 代码
  
  browse_cookie 文件夹内容 :第10章 第4节 内容
  
  splash_example 文件夹内容：第11章 代码 分别是项目实战：爬取toscrape中的名人名言 、爬取京东商城中的书籍信息
  
  toscrape_book  文件夹内容：第八章 代码 包含 第 12 章 数据存储代码（里面还有个异步存储数据的小例子。）
  
  

1.spiders 蜘蛛

2.items.py 数据保存

3.pipelines.py 数据处理

4.settings.py 设置

5.my_exporters.py 自定义的数据导出格式


## 常用命名：

scrapy crawl < spider > --运行爬虫
  
scrapy crawl < spider > -o < file > --运行爬虫导出数据

scrapy startproject < name > --创建一个爬虫项目
  
scrapy genspider [options] < name >  < domain > --创建一个爬虫（在startproject里创建）

scrapy shell [url|file] --测试

## 帮助

scrapy -h

Use "scrapy <command> -h" to see more info about a command


## 小技巧：

cd 用法 CD [/D] [drive:][path]

cd /d d:\project\toscrape_book

cd toscrape_book\spiders

使用 /D 开关，除了改变驱动器的当前目录之外， 还可改变当前驱动器。

-----------------------
url 过滤
两种方法能够使 requests 不被过滤: 
1. 在 allowed_domains 中加入 url 
2. 在 scrapy.Request() 函数中将参数 dont_filter=True 设置为 True
