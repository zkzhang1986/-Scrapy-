# 测试 browsercookie 库

# import  browsercookie
# chrom_cookies = browsercookie.chrome()
# print(type(chrom_cookies),chrom_cookies)

# for cookie in chrom_cookies:
#     print(cookie)
#     找到某网站cookies
#     if 'baidu.com' in str(cookie):
#         print('baiducookies:',cookie)
#     else:
#         break



# 《精通scrapy网络爬虫》第10章 第4节 （10.4.3）
# 实现 browserCookiesMiddleware
# 核心思想：使用 browsercookie 将浏览器中的cookis提取，存储到 CookieJar 字典 self.jars中。
import browsercookie
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware

class BrowserCookiesMiddleware(CookiesMiddleware):
    def __init__(self,debug=False):
        super().__init__(debug)
        self.load_browser_cookies()

    def load_browser_cookies(self):
        # 加载chrome浏览器中的Cookie
        jar = self.jars['chrome']
        chrome_cookiejar = browsercookie.chrome()
        for cookie in chrome_cookiejar:
            jar.set_cookie(cookie)


