# 《精通scrapy网络爬虫》 第11章 11.1.1 测试 Splash render.html

import requests
from scrapy.selector import Selector

# 用render.html 返回一个经过Javascript渲染之后的页面的HTML代码。
splash_url = 'http://192.168.99.100:8050/render.html'
url = 'http://quotes.toscrape.com/js'
# 构建参数
args = {'url':url, 'timeout':5, 'image':0}
response = requests.get(splash_url, params=args)
sel = Selector(response)
print(sel.css('div.quote span.text::text').extract())

# 直接获取页面
response0 = requests.get(url)
sel0 = Selector(response0)
print(sel0.css('div.quote span.text::text').extract())
