# 《精通 scrapy 网络爬虫》第3章 第4节（即3.4）CSS 实例
from scrapy.http import HtmlResponse

body = '''
<html>
	<head>
		<base href='http://example.com'/>
		<title>Example website</title>
	</head>
	<body>
		<div id='images-1' style="width:1230px;">
			<a href='image1.html'>Name:Image 1 <br/><img src="image1.jpg"/></a>
			<a href='image2.html'>Name:Image 2 <br/><img src="image2.jpg"/></a>
			<a href='image3.html'>Name:Image 3 <br/><img src="image3.jpg"/></a>
		</div>

        <div id="images-2" class="small">
            <a href='image4.html'>Name:Image 4 <br/><img src="image4.jpg"/></a>
			<a href='image5.html'>Name:Image 5 <br/><img src="image5.jpg"/></a>
        </div>
	</body>
</html>
'''
response = HtmlResponse(url='http://www.example.com/', body=body, encoding='utf-8')

# E:选中E元素
print(response.css('img')) # 等同于 print(response.xpath('//img'))
# E1,E2:选中E1和E2元素
print(response.css('base,title'))
# E1 E2:选中E1后代中E2元素
print(response.css('div img')) # 等同 print(response.xpath('//div//img'))
# E1>E2:选中E1元素中的E2元素
print(response.css('body>div'))
# [ATTR]:选中包含ATTR属性的元素
print(response.css('[style]')) # print(response.xpath('//div/@style'))
# [ATTR=VALUE]:选中包含ATTR属性且值为VALUE的元素
print(response.css('[id="images-1"]')) # print(response.xpath('//div[@id="images-1"]'))
# E:nth-child(n):选中E元素，且该元素必须是其父元素的第n个子元素
# 选中每个div的第一个
print(response.css('div>a:nth-child(1)'))
# 选中第二个div的第一个
print(response.css('div:nth-child(2)>a:nth-child(1)'))
# E:first-child:选中E元素，该元素必须其父元素的第一个子元素
# E:last-child:选中E元素，该元素必须其父元素的倒数第一个子元素
print(response.css('div:first-child>a:first-child'))
print(response.css('div:last-child>a:last-child'))
# E::text:选中E元素的文本节点
print(response.css('a::text').extract()) # print(response.xpath('//a/text()').extract())