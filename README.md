# 《精通scrapy网络爬虫》 

example文件夹内容： 第一章至第七章代码

practise文件夹内容：书本中的练习

toscrape_book 文件夹内容：第八章 代码（ps在原代码基础增加了：去掉重复、以xls格式导出，选择器用的是css）

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
