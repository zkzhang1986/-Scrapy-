# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request

class ImagesSpider(scrapy.Spider):
    BASE_URL = 'https://image.so.com/zjl?ch=art&sn=%s&listtype=new&temp=1'
    start_index = 0

    # 限制最大下载数量，防止磁盘用量过大
    # 解释 MAX_DOWNLOAD_NUM并不是下载的图片数，而是构成url的链接数，可以理解为61/30 = 2 +1
    # 构了3条  url
    # 分别是：https://image.so.com/zjl?ch=art&sn=%0&listtype=new&temp=1；
    # https://image.so.com/zjl?ch=art&sn=%30&listtype=new&temp=1；
    # https://image.so.com/zjl?ch=art&sn=%60&listtype=new&temp=1；
    # 下载的图片数是90张
    MAX_DOWNLOAD_NUM = 61

    name = 'images'

    # 设置allowed_domains的含义是过滤爬取的域名，
    # 在插件scrapy.spidermiddlewares.offsite.OffsiteMiddleware启用的情况下（默认是启用的），
    # 不在此允许范围内的域名就会被过滤，而不会进行爬取.(但是对于起止url是不会过滤的即start_url)。
    # 2020-02-28 09:23:38 [scrapy.middleware] INFO: Enabled spider middlewares:
    # ['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
    #  'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
    #  'scrapy.spidermiddlewares.referer.RefererMiddleware',
    #  'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
    #  'scrapy.spidermiddlewares.depth.DepthMiddleware']
    # allowed_domains = ['images.so.com']

    start_urls = [BASE_URL % 0]

    # 取前面四页
    # def start_requests(self):
    #     for sn in range(0, 120, 30):
    #         # true_link = self.start_urls[0].format(sn)
    #         true_link = self.BASE_URL % sn
    #         yield scrapy.Request(url=true_link, callback=self.parse)

    def parse(self, response):
        # 使用json 模块解析响应结果
        infos = json.loads(response.body.decode('utf-8'))
        # 提取所有图片下载 url 到一个列表，赋给 item 的 "image_urls" 字段
        yield {'image_urls': [info['qhimg_url'] for info in infos['list']]}

        # 如果 count 字段 大于0，并且下载数量小于 MAX_DOWNLOAD_NUM ，继续获取下一页图片信息。
        self.start_index = self.start_index + infos['count']
        # print(self.start_index)
        if infos['count'] > 0 and self.start_index < self.MAX_DOWNLOAD_NUM:
            yield Request(self.BASE_URL % self.start_index, callback=self.parse)