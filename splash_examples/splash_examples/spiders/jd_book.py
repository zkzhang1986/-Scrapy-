# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
import json

# lua语言
lua_script='''
--定义一个函数，参数是splash。                    
function main(splash) 
    -- 打开url页面，这里指打开 splash.args.url 就相当于加载时配置的URL参数（即SPLASH_URL = 'http://192.168.99.100:8050'）
    splash:go(splash.args.url) 
    -- 等待页面渲染2秒
    splash:wait(2)
    -- 执行JavaScript语句，不返回值。滚动浏览器到访问 HTML 元素中的 "calass=page"，意思是滚动浏览器到底端（page位置）。
    splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
    -- 等待页面渲染2秒
    splash:wait(2)
    -- 返回获取当前页面的 html 文本
    return splash:html()
end
'''

class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    # start_urls = ['http://search.jd.com/']
    base_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&wq=python' # 起始页

    def start_requests(self):
        # 请求第一页， 无需 JS 渲染
        yield Request(self.base_url, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self,response):
        # 获取商品总数，计算出总页数
        # total = int(response.css('span#J_resCount::text').extract_first())
        total = response.css('span#J_resCount::text').re_first('\d+.+\d')
        total = int(float(total)*10000)
        pageNum = total // 60 + (1 if total % 60 else 0 )

        # 测试时可以不用取那么多页
        pageNum = 2

        # 构造每页的url，向 Splash 的 execute 端点发送请求
        for i in range(pageNum):
            url = '%s&page=%s' % (self.base_url, 2 * i + 1)
            # print(url)
            yield SplashRequest(url,
                                endpoint='execute',
                                args={'lua_source':lua_script},
                                cache_args=['lua_source'])

    def parse(self, response):
        # 获取每一个页面中每本书的名字和价格
        for sel in response.css('ul.gl-warp.clearfix > li.gl-item'):
            yield {
                'name':sel.css('div.p-name').xpath('string(.//em)').extract_first(),
                'pric':sel.css('div.p-price i::text').extract_first(),
            }


