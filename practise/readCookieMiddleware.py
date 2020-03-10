# from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
# CookiesMiddleware 阅读

import os
# six 一个专门用来兼容 Python 2 和 Python 3 的库。它解决了诸如 urllib 的部分方法不兼容问题
import six
# logging 记录 python 日志
import logging
# from collections import defaultdict
# 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict：
from collections import defaultdict

from scrapy.exceptions import NotConfigured
from scrapy.http import Response
from scrapy.http.cookies import CookieJar
from scrapy.utils.python import to_native_str

logger = logging.getLogger(__name__)


class CookiesMiddleware(object):
    """This middleware enables working with sites that need cookies"""
    """
        中间件在Scrapy启动时实例化.其中jars属性是一个默认值为CookieJar对象的dict.
        该中间件追踪web server发送的cookie,保存在jars中,并在之后的request中发送回去,
        类似浏览器的行为.
        COOKIES_ENABLED 默认 True
        COOKIES_DEBUG 默认:False
        """

    def __init__(self, debug=False):
        # 使用标准库 defaultdict 创建一个默认字典，该字典中每一项的值都是scrapy.http.cookies.CookieJar对象，
        # CookiesMiddleware 可以让scrapy爬虫同时使用多个不同的CookiJar。
        self.jars = defaultdict(CookieJar)
        self.debug = debug

    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件读取 COOKIES_ENABLED,决定是否启用。（默认：False）
        # 如果启用，调用构造器创建对象，否则抛出NotConfigured异常，scrapy忽略该中间件
        if not crawler.settings.getbool('COOKIES_ENABLED'):
            raise NotConfigured
        return cls(crawler.settings.getbool('COOKIES_DEBUG'))

    def process_request(self, request, spider):
        # 处理每一个待发送的 request对象，尝试从 request.meta['cookieJar'] 获取用户指定使用的cookieJar，
        # 如果用户未指定，就使用默认的 CookieJar(self.jars[None])。
        # 调用self.get_request_cookies方法获取发送请求request应携带的 Cookie 信息，填到 HTTP 请求
        if request.meta.get('dont_merge_cookies', False):
            return

        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        cookies = self._get_request_cookies(jar, request)
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)

        # set Cookie header
        request.headers.pop('Cookie', None)
        jar.add_cookie_header(request)
        self._debug_cookie(request, spider)

    def process_response(self, request, response, spider):
        # 处理每一个 Response 对象，依然是通过 request,meta['cookiejar']获取cookiejar对象，
        # 调用extract_cookies方法将 HTTP 响应头部中的 Cookie 信息保存在 CookieJar 对象中。
        if request.meta.get('dont_merge_cookies', False):
            return response

        # extract cookies from Set-Cookie and drop invalid/expired cookies
        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        jar.extract_cookies(response, request)
        self._debug_set_cookie(response, spider)

        return response

    def _debug_cookie(self, request, spider):
        if self.debug:
            cl = [to_native_str(c, errors='replace')
                  for c in request.headers.getlist('Cookie')]
            if cl:
                cookies = "\n".join("Cookie: {}\n".format(c) for c in cl)
                msg = "Sending cookies to: {}\n{}".format(request, cookies)
                logger.debug(msg, extra={'spider': spider})

    def _debug_set_cookie(self, response, spider):
        if self.debug:
            cl = [to_native_str(c, errors='replace')
                  for c in response.headers.getlist('Set-Cookie')]
            if cl:
                cookies = "\n".join("Set-Cookie: {}\n".format(c) for c in cl)
                msg = "Received cookies from: {}\n{}".format(response, cookies)
                logger.debug(msg, extra={'spider': spider})

    def _format_cookie(self, cookie):
        # build cookie string
        cookie_str = '%s=%s' % (cookie['name'], cookie['value'])

        if cookie.get('path', None):
            cookie_str += '; Path=%s' % cookie['path']
        if cookie.get('domain', None):
            cookie_str += '; Domain=%s' % cookie['domain']

        return cookie_str

    def _get_request_cookies(self, jar, request):
        if isinstance(request.cookies, dict):
            cookie_list = [{'name': k, 'value': v} for k, v in \
                    six.iteritems(request.cookies)]
        else:
            cookie_list = request.cookies

        cookies = [self._format_cookie(x) for x in cookie_list]
        headers = {'Set-Cookie': cookies}
        response = Response(request.url, headers=headers)

        return jar.make_cookies(response, request)
