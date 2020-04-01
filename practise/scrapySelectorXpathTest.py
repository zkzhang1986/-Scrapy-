# 《精通 scrapy 网络爬虫》第3章 第3节（即3.3）xpath 实例

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

body = '''
<html>
	<head>
		<base href='http://example.com'/>
		<title>Example website</title>
	</head>
	<body>
		<div id='images'>
			<a href='image1.html'>Name:Image 1 <br/><img src="image1.jpg"/></a>
			<a href='image2.html'>Name:Image 2 <br/><img src="image2.jpg"/></a>
			<a href='image3.html'>Name:Image 3 <br/><img src="image3.jpg"/></a>
			<a href='image4.html'>Name:Image 4 <br/><img src="image4.jpg"/></a>
			<a href='image5.html'>Name:Image 5 <br/><img src="image5.jpg"/></a>
		</div>
	</body>
</html>
'''
response = HtmlResponse(url='http://www.example.com/', body=body, encoding='utf-8')

# /: 一个从根开始的绝对路径
print('[1]==========/: 一个从根开始的绝对路径==========')
print(response.xpath('/html'))
print(response.xpath('/html/head'))
# E1/E2：选中E1节点中所有E2
print('[2]==========E1/E2：选中E1节点中所有E2==========')
print(response.xpath('/html/body/div/a'))
# //E: 选中文档中所有E，无论在什么位置
print('[3]==========//E: 选中文档中所有E，无论在什么位置==========')
print(response.xpath('//a'))
# E1//E2:选中E1后代节点中所有E2，无论在后代中的什么位置
print('[4]==========E1//E2:选中E1后代节点中所有E2，无论在后代中的什么位置==========')
print(response.xpath('/html/body//img'))
print(response.xpath('/html/body//a'))
# E/text():选中E的文本子节点
print('[5]==========E/text():选中E的文本子节点==========')
print(response.xpath('//a/text()'))
print(response.xpath('//a/text()'))
# E/*:选中E的所有元素子节点
print('[6]==========E/*:选中E的所有元素子节点==========')
print(response.xpath('/html/*'))
print(response.xpath('//body/*'))
# */E:选中孙节点中的所有E
print('[7]==========*/E:选中孙节点中的所有E==========')
print(response.xpath('//div/*/img'))
# E/@ATTR: 选中E的ATTR属性
print('[8]==========E/@ATTR: 选中E的ATTR属性==========')
print(response.xpath('//img/@src'))
# //@ATTR: 选中文档中所有Attr属性
print('[9]==========//@ATTR: 选中文档中所有Attr属性==========')
print(response.xpath('//@href'))
print(response.xpath('//@href'))
# E/@*:选中E的所有属性
print('[10]==========E/@*:选中E的所有属性==========')
print(response.xpath('//a[1]/img/@*'))
# .:选中当前节点，用来描述相对路径
print('[11]==========.:选中当前节点，用来描述相对路径==========')
sel = response.xpath('//a')[0]
print(sel)
print(sel.xpath('//img')) # //img 是绝对路径，从根开始搜索，不是从当前a开始
print(sel.xpath('.//img'))# .//img 描述当前节点后代中所有img
# ..: 选中当前节点的父节点，用来描述相对路径
print('[12]==========..: 选中当前节点的父节点，用来描述相对路径==========')
print(response.xpath('..//img'))
# node[谓语]：用来查找某个特定的节点或者包含某个特定值的节点
# a中的第3 个
print('[13]==========a中的第 3 个==========')
print(response.xpath('//a[3]'))
# last函数,选中最后1个
print('[14]==========last函数,选中最后1个==========')
print(response.xpath('//a[last()]'))
# position函数，选中前3个
print('[15]==========position函数，选中前3个==========')
print(response.xpath('//a[position()<=2]'))
# 选中所有含有id属性的div
print('[16]==========选中所有含有id属性的div==========')
print(response.xpath('//div[@id]'))
# 选中所有含有id属性且值为"images"的div
print('[17]==========选中所有含有id属性且值为"images"的div==========')
print(response.xpath('//div[@id="images"]'),'\n')

# 常用函数
print('==========xpath常用函数==========')
print('[1]==========string(arg):返回参数字符串值==========')
text = '<a href="#">Click here to go the <strong> Next Page </strong></a>'
sel = Selector(text=text)
print(sel)
print(sel.xpath('//a/strong').extract())
print(sel.xpath('string(/html/body/a/strong/text())').extract())
print(sel.xpath('/html/body/a//text()').extract())
print(sel.xpath('string(/html/body/a)').extract())
print('[2]==========contains(str1,str2):判断str1中是否包含str2，返回布尔值==========')
text = '''
<div>
    <p class="small info">hello world</p>
    <p class="normal info">hell scrapy</p>
</div>
'''
sel=Selector(text=text)
print(sel.xpath('//p'))
print(sel.xpath('//p[contains(@class,"small")]'))
print(sel.xpath('//p[contains(@class,"info")]'))
print(sel.xpath('//p[contains(@class,"info1")]'))