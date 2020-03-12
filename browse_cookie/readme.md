《精通scrapy网络爬虫》第10章 第4节 内容
#说明
    记得得先登录浏览器
    
# 测试    
    进入到browse_cookie
    scrapy shell
    url = 'http://example.webscraping.com/'
    from scrapy import Request
    res = Request(url, meta={'cookiejar':'chrome'})
    fetch(res)
    view(response)
    
    