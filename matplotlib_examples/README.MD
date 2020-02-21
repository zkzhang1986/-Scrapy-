第9章 代码分析

用 FilesPipeline 和 ImagesPipeline 下载

配置：
settings.py 中配置
ITEM_PIPLELINES = {'scrapy.pipelines.filse.FilesPipeline':1} # 文件设置
FILES_STORE = '/porject0611' # 文件下载目录

###### 为图片生成缩略图
IMAGES_THUMBS = {
	'small':(50,50),
	'big':(270,270),
}

##### 过滤尺寸过小的图片
IMAGES_MIN_WIDTH = 110 # 最小宽度
IMAGES_MIN_HEIGHT = 110 # 最小高度


##### 需求：
下载 https://matplotlib.org网站中的所有例子的源码文件到本地

##### 分析：
https://matplotlib.org/gallery/index.html 例子

提取每个例子链接
链接:每个例子的链接 <a class="reference internal" href="images_contours_and_fields/affine_image.html#sphx-glr-gallery-images-contours-and-fields-affine-image-py"><span class="std std-ref">Affine transform of an image</span></a>
可以用 LinkExtractor 提取 
from scrapy.linkextractors import LinkExtractor
 le = LinkExtractor(restrict_css='a.reference')
 links = le.extract_links(response)
 [link.url for link in links]

feth(url) #crapy shell 分析中的回调函数，把url录入可以回调。

提取下载url
下载路径：<a class="reference download internal" download="" href="../../_downloads/4ee10f51bc70fd3964fb1b8b3f64d054/bar_stacked.py"><code class="xref download docutils literal notranslate"><span class="pre">Download</span> <span class="pre">Python</span> <span class="pre">source</span> <span class="pre">code:</span> <span class="pre">bar_stacked.py</span></code></a>
href = response.css('a.reference::attr(href)').extract_first()
herf = response.css('a.reference.download.internal::attr(href)').extract_first()
download_url = response.urljoin(href)
------------------------
分析不对，起始网站就错了~~5555555555555555555555555
