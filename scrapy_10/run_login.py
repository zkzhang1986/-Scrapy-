# 在Pycharm中调试scrapy爬虫 https://www.jianshu.com/p/6f7cf38d5792
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('login')    #  你需要将此处的spider_name替换为你自己的爬虫名
    process.start()
    
