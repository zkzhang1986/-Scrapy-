# -*- coding: utf-8 -*-
# 测试随机代理中间件

import scrapy
import json

class TestRandomProxySpider(scrapy.Spider):
    name = 'test_random_proxy'

    def start_requests(self):
        for _ in range (100):
            yield scrapy.Request('http://httpbin.org/ip',dont_filter=True)
            yield scrapy.Request('https://httpbin.org/ip',dont_filter=True)

    def parse(self,response):
        print(json.loads(response.text))
