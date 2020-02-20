# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import BookItem

class BooksSpider(scrapy.Spider):
    # 爬虫名
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    # 抓取网点起点
    start_urls = ['http://books.toscrape.com/']

    # 书籍列表页面的解析函数
    def parse(self, response):
        # 提取书籍列表页面中每本书的链接 （LinkExtractor提取链接的用法）
        le = LinkExtractor(restrict_css='article.product_pod h3')
        links = le.extract_links(response)
        # print('links_list_url:',links)
        for link in links :  # le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book)

        # 提取下一页（LinkExtractor提取链接的用法）
        le = LinkExtractor(restrict_css='ul.pager li.next')
        links = le.extract_links(response)
        # print('links_next_url:',links)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

    #书籍页面的解析函数：
    def parse_book(self,response):
        # 元数据保存先在item.py定义，再引用
        book = BookItem()
        sel = response.css('div.product_main')
        book['name'] = sel.css('h1::text').extract_first()
        book['price'] = sel.css('p.price_color::text').extract_first()
        book['review_rating'] = sel.css('p.star-rating::attr(class)').re_first('star-rating ([A-Za-z]+)')
        book['stock'] = sel.css('p.instock::text').re_first('stock \((.*?) available\)')

        sel = response.css('table.table-striped')
        book['upc'] = sel.css('tr:nth-child(1)>td::text').extract_first()
        book['review_num'] = sel.css('tr:nth-last-child(1)>td::text').extract_first()

        yield book
