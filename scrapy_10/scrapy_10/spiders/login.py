# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']

    # 书中错的跳转url
    # start_urls = ['http://example.webscraping.com/user/profile']

    # 登录后跳转url
    start_urls = ['http://example.webscraping.com/places/default/user/profile']

    def parse(self, response):
        # 解析登录后下载的页面，此例子中为用户个人信息页面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        yield dict(zip(keys,values))

    # -----------------登录-----------------
    # 登录页面的 url

    # 书中错的url  报raise ValueError("No <form> element found in %s" % response)
    # login_url = 'http://example.webscraping.com/user/login'

    login_url = 'http://example.webscraping.com/places/default/user/login'

    def start_requests(self):
        # start_requests 最新请求登录页面
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        # 登录页面的解析函数，在该方法中进行模拟登录，构造表单请求并提交
        fd = {'email':'zk_zhang1986@sina.com','password':'zzk123'}
        # return FormRequest.from_response(response,formdata=fd,callback=self.parse_login)
        yield FormRequest.from_response(response,formdata=fd,callback=self.parse_login)

    def parse_login(self, response):
        # 表单请求响应处理函数，通过在页面上判断特殊字符判断是否登录成功，
        # 如果成功调用基类是start_requests方法继续爬取start_urls中的页面
        if 'Welcome' in response.text:
            print('登录成功')
            yield from super().start_requests()
        else:
            print('登录失败')
        # return
