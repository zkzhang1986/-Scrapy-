# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login1'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/login']

    def parse(self, response):
        return FormRequest.from_response(response,
                                         formdata={'email':'zk_zhang1986@sina.com','password':'zzk123'},
                                         callback=self.after_login)

    def after_login(self,response):
        if 'Welcome' in response.text:
            print('登录成功')
        else:
            print('登录失败')
        return