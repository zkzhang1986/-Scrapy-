# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # allowed_domains = ['quotes.toscrape.com']
    # 起始页
    start_urls = ['http://quotes.toscrape.com/js']

    def start_requests(self):
        # 请求第一页
        for url in self.start_urls:
            print(url)
            # SplashRequest 调用 'http://192.168.99.100:8050/render.html' 为 http://quotes.toscrape.com/js 渲染。
            yield  SplashRequest(url, args={'images': 0,'timeout':3})

    def parse(self, response):
        # 获取名言和作者
        for sel in response.css('div.quote'):
            quote = sel.css('span.text::text').extract_first()
            author = sel.css('small.author::text').extract_first()
            yield{'quote':quote,'author':author}

        # 获取下一页的路径
        href = response.css('li.next a::attr(href)').extract_first()
        # print(href)
        if href:
            url = response.urljoin(href)
            # SplashRequest 调用 'http://192.168.99.100:8050/render.html' 为 http://quotes.toscrape.com/js 渲染。
            # 然后获取名言何作者
            yield SplashRequest(url, args={'image': 0,'timeout':3},callback=self.parse)
            # yield SplashRequest(url, args={'image': 0, 'timeout': 3})
