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
# 实例通过allow_domains参数提取页面example1.html中所有github.com 和 stackoverflow.com这两个域的链接
domains = ['github.com','stackoverflow.com']
le_allow_domains = LinkExtractor(allow_domains=domains)
links_allow_domains = le_allow_domains.extract_links(response1)
html1_url_allow_domains = [link_allow_domains.url for link_allow_domains in links_allow_domains]
print('html1_url_allow_domains:',html1_url_allow_domains)

# deny_domains
# 接收一个域名或一个域名列表，与allow_domains相反，排除指定域的链接
# 实例通过deny_domains参数提取页面example1.html中除github.com 域的所有链接
le_deny_domains = LinkExtractor(deny_domains='github.com')
links_deny_domains = le_deny_domains.extract_links(response1)
html1_url_deny_domains = [link_deny_domains.url for link_deny_domains in links_deny_domains]
print('html1_url_deny_domains:',html1_url_deny_domains)

# restrict_xpaths
# 接收一个XPath表达式或一个XPath表达列表，提取XPath表达式选中区域下的链接
# 实例通过restrict_xpaths参数提取页面example1.html中<div id="top">元素下的链接
le_restrict_xpaths = LinkExtractor(restrict_xpaths='//div[@id="top"]')
links_restrict_xpaths = le_restrict_xpaths.extract_links(response1)
html1_url_restrict_xpaths = [link_restrict_xpaths.url for link_restrict_xpaths in links_restrict_xpaths]
print('html1_url_restrict_xpaths:',html1_url_restrict_xpaths)

# restrict_css
# 接收一个CSS表达式或一个CSS选择器列表，提取CSS选择器选中区域下的链接
# 实例通过restrict_css参数提取页面example1.html中<div @id="bottom">元素下的链接
le_restrict_css = LinkExtractor(restrict_css='div#bottom')
links_restrict_css = le_restrict_css.extract_links(response1)
html1_url_restrict_css = [link_restrict_css.url for link_restrict_css in links_restrict_css]
print('html1_url_restrict_css:',html1_url_restrict_css)

# tags
# 接收一个标签（字符串）或一个标签列表，提取指定标签内的链接，默认为['a','area']
# attrs
# 接收一个属性（字符串）或一个属性列表，提取指定属性内的链接，默认为['href].
# 实例 提取example2.html中引用JavaScript 文件的链接（即：提取script标签中的src链接）
le_tags_attrs = LinkExtractor(tags='script',attrs='src')
links_tags_attrs = le_tags_attrs.extract_links(response2)
html2_url_tags_attrs = [link_tags_attrs.url for link_tags_attrs in links_tags_attrs]
print('html2_url_tags_attrs:',html2_url_tags_attrs)

# process_value
# 接收一个形如func(value)的回调函数。
# 如果传递了该参数，LinkExtractor将调用该回调函数对提取的每一个链接（如a标签的href链接）进行处理，
# 回调函数正常情况下应该返回一个字符串（处理结果），想要抛弃所处理结果的链接时，返回None。
# 实例：
import re
def process(value):
    m = re.search("javascript:goToPage\('(.*?)'",value)
    if m:
        value = m.group(1)
    return value

le_process_value = LinkExtractor(process_value=process)
links_process_value = le_process_value.extract_links(response2)
html2_url_process_value = [link_process_value.url for link_process_value in links_process_value]
print('html2_url_process_value:',html2_url_process_value)