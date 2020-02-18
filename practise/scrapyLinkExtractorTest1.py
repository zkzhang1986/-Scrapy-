# 《精通 scrapy 网络爬虫》第6章 第2节（即6.2）描述提取规则
# 使用LinkExtract 提取链接
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
html1 = open('scrapyLinkExtractorTest1.html','r',encoding='utf-8').read()
html2 = open('scrapyLinkExtractorTest2.html','r',encoding='utf-8').read()
response1 = HtmlResponse(url='http://example1.com',body=html1,encoding='utf8')
response2 = HtmlResponse(url='http://example2.com',body=html2,encoding='utf8')
# print(response1,response2)
le = LinkExtractor()
links = le.extract_links(response1)
#此时 links 提取的链接为绝对链接
html1_url = [link.url for link in links]
print('html1_url:',html1_url)

# allow
# 接收一个正则表达式或正则表达式列表，提取绝对值url与正则表达式匹配的链接，
# 如果该参数为空（默认），就提取全部链接
# 实例通过allow参数提取页面example1.html中路径以/intro开头的链接
pattern = '/intro/.+\.html'
le_allow = LinkExtractor(allow=pattern)
links_allow = le_allow.extract_links(response1)
html1_url_allow = [link_allow.url for link_allow in links_allow]
print('html1_url_allow:',html1_url_allow)

# deny
# 接收一个正则表达式或正则表达式列表，与allow相反，排除绝对值url与正则表达式匹配的链接.
# 实例通过deny参数提取页面example1.html中所有站外链接（即排除站内链接）
from urllib.parse import urlparse
pattern = '^'+ urlparse(response1.url).geturl()
print('deny_pattern:',pattern)
le_deny = LinkExtractor(deny=pattern)
links_deny = le_deny.extract_links(response1)
html1_url_deny = [link_deny.url for link_deny in links_deny]
print('html1_url_deny:',html1_url_deny)

# allow_domains
# 接收一个域名或一个域名列表，提取到指定域的链接

