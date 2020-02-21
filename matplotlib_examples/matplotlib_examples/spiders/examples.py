# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ExampleItem


class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotlib.org']
    # start_urls = ['https://matplotlib.org/gallery/index.html'] # zzk
    # 《精通scrapy网络爬虫》书中的起止网站
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        # 《精通scrapy网络爬虫》中代码
        # 获取每个例子链接 先用div.toctree-wrapper.compound提取，再用参数deny过滤
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound',deny='/index.html$')
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(url=link.url, callback=self.parse_example)

        # zzk 用start_urls = ['https://matplotlib.org/gallery/index.html'] 分析 获取例子链接
        # le = LinkExtractor(restrict_css='a.reference')
        # links = le.extract_links(response)
        # for link in links:
        #     yield scrapy.Request(url=link.url, callback=self.parse_example)

    def parse_example(self, response):
        # 《精通scrapy网络爬虫》中代码
        href = response.css('a.reference.external::attr(href)').extract_first()
        # zzk
        # href = response.css('a.reference.download.internal::attr(href)').extract_first()
        url = response.urljoin(href)
        example = ExampleItem()
        example['file_urls'] = [url]
        return example
