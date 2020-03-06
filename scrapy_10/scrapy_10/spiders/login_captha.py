# OCR识别登录 spider
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import FormRequest
import json
from scrapy.log import logger
from PIL import Image
import pytesseract
from io import BytesIO

class CaptchLoginSpider(scrapy.Spider):
    name = "login_captch"
    start_url = ['http://XXX.com/']

    def parse(self, response):
        # 解析登录后下载页面。
        pass

    # X网站登录的页面 url (虚构)
    login_url = 'http://XXX.com/login'
    user = ''
    password = ''

    def start_requests(self):
        # start_requests 请求登录页面
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self,response):
        # 该方法既是登录页面的解析函数，又是下载验证码图片的响应处理函数

        # 判断response.meta['login_response']是否存在，
        # 如果存在，当前response为验证码图片的响应
        # 如果不存在，当前response为登录页面的响应
        login_response = response.meta.get('login_response')
        if not login_response:
            # Step 1: 不存在
            # 此时 response 为登录页面的响应，从中提取验证图片的 url，下载验证码图片
            captchaUrl = response.css('label.field.prepend-icon img::attr(src)').extract_first()
            captchaUrl = response.urljoin(captchaUrl)
            # 构造 Request 时，将当前response保存在 meta 字典中
            yield Request(captchaUrl,
                          callback=self.login,
                          meta={'login_response':response},
                          dont_filter=True)
            """
            两种方法能够使 requests 不被过滤: 
            1. 在 allowed_domains 中加入 url 
            2. 在 scrapy.Request() 函数中将参数 dont_filter=True 设置为 True
            """

        else:
            # Step 2: 存在
            # login_response 为登录页面的响应，用其构造表单请求并发送
            formdata = {
                'email':self.user,
                'password':self.password,
                # 调用OCR识别
                'code':self.get_captha_by_OCR(response.body),
            }

            yield FormRequest(login_response,
                              callback=self.parse_login,
                              formdata=formdata,
                              dont_filter=True)


    def parse_login(self, response):
        # 根据响应结果判断是否成功登录
        info = json.loads(response.text)
        if info['error'] == 0:
            logger.info('登录成功:-')
            return super().start_requests()

        logger.info('登录失败:-(,重新登录...')
        return self.start_requests()

    def get_captha_by_OCR(self,data):
        # OCR 识别
        img = Image.open(BytesIO(data))
        img = img.convert('L')
        captha = pytesseract.image_to_string(img)
        img.close()

        return captha

    def get_captha_by_network(self,data):
        # 平台识别
        pass

    def get_captha_by_user(self,data):
        # 人工识别
        img = Image.open(BytesIO(data))
        img.show()
        captha = input('请输入验证码：')
        img.close()
        return captha

