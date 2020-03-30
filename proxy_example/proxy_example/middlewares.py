# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# 测试中间件
# from scrapy.utils.project import get_project_settings
# class ProxyMiddleware(object):
#
#     def process_request(self, request, spider):
#         proxy = random.choice(get_project_settings('PROXIES'))
#         request.meta['proxy'] = proxy


# 实现随机代理 2020-03-27
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
# 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict
from collections import defaultdict
import json
import random

class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self,auth_encoding='latin-1',proxy_list_file=None):
        if not proxy_list_file:
            # 当程序出现错误，python会自动引发异常，也可以通过raise显示地引发异常。一旦执行了raise语句，raise后面的语句将不能执行
            raise NotConfigured

        self.auth_encoding = auth_encoding
        # 分别用两个列表维护 HTTP 和 HTTPS 的代理 {'http':[...],'https':[...]}
        self.proxies = defaultdict(list)

        # 从json 文件中读取代理服务器信息，填入self.proxies
        with open (proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['proxy_scheme']
                url = proxy['proxy']
                # self.proxies[scheme].append(self._set_proxy(url,scheme))
                self.proxies[scheme].append(self._get_proxy(url,scheme))

    # HttpProxyMiddleware原代码
    # def __init__(self, auth_encoding='latin-1'):
    #     self.auth_encoding = auth_encoding
    #     self.proxies = {}
    #     for type_, url in getproxies().items():
    #         self.proxies[type_] = self._get_proxy(url, type_)


    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件中读取用户验证信息的编码
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING','latain-1')
        # 从配置文件中读取代理文件服务器列表文件（json）的路径
        proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')
        return cls(auth_encoding,proxy_list_file)

    # HttpProxyMiddleware原代码
    # @classmethod
    # def from_crawler(cls, crawler):
    #     if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
    #         raise NotConfigured
    #     auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING')
    #     return cls(auth_encoding)

    def _set_proxy(self, request, scheme):
        # 随机选择一个代理
        a = self.proxies[scheme]
        creds,proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
        if creds:
            request.headers['Proxy_Authorization'] = b'Basic' + creds

    # HttpProxyMiddleware原代码
    # def _set_proxy(self, request, scheme):
    #     creds, proxy = self.proxies[scheme]
    #     request.meta['proxy'] = proxy
    #     if creds:
    #         request.headers['Proxy-Authorization'] = b'Basic ' + creds

# 以下为原代码
class ProxyExampleSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyExampleDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
