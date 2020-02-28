第9章 第二节 下载360图片

需求：下载360图片网站中艺术分类下的所有图片到本地

分析：
图片是异步加载（由X-Requested-With ：X-Requested-With: XMLHttpRequest可看出为ajax，如果为null为同步加载），由JavaScript脚本完成。

响应结果（json）中的list字段是一个图片信息列表，里面"qhimg_downurl": "https://dl.image.so.com/d?imgurl=https%3A%2F%2Fp2.ssl.qhimgs1.com%2Ft01d0089d6b91c7bb72.jpg&purl=https%3A%2F%2Fimage.so.com%2F%3Fsrc%3Ddl.image&key=0e06128eb9",是图片下载。

jQuery发送请求为：
https://image.so.com/zjl?ch=art&sn=30&listtype=new&temp=1
https://image.so.com/zjl?ch=art&sn=60&listtype=new&temp=1
https://image.so.com/zjl?ch=art&sn=90&listtype=new&temp=1

ch 参数 分类标签
sn 参数 从第几张图片开始加载，即结果列表中第一张图片在服务器的序号

代码撸起来
1.创建scrapy项目
2.配置ImagesPipeline，并指定图片下载目录
3.实现ImagesSpider

01.创建scrapy项目，取名为so_image 再用scrapy genspdier 创建spider
命令如下：
scrapy startproject so_image
cd so_image
scrapy genspdier imamges images.so.com
tree /f

D:.
│  scrapy.cfg
│
└─so_image
    │  items.py
    │  middlewares.py
    │  pipelines.py
    │  settings.py
    │  __init__.py
    │
    ├─spiders
    │  │  images.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          __init__.cpython-36.pyc
    │
    └─__pycache__
            settings.cpython-36.pyc
            __init__.cpython-36.pyc

02 配置 settings.py
ITEM_PIPELINES = {
   # 'so_image.pipelines.SoImagePipeline': 300,
    'scrapy.pipelines.images.ImagesPipeline': 1,
}
# 下载目录
IMAGES_STORE = 'download_images'

----------
不知道为什么只获取第一页数据

答： allowed_domains 影响的应注释掉。原因如下：

设置allowed_domains的含义是过滤爬取的域名，

在插件scrapy.spidermiddlewares.offsite.OffsiteMiddleware启用的情况下（默认是启用的），

不在此允许范围内的域名就会被过滤，而不会进行爬取.(但是对于起止url是不会过滤的即start_url)。

2020-02-28 09:23:38 [scrapy.middleware] INFO: Enabled spider middlewares:

['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',

'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',

'scrapy.spidermiddlewares.referer.RefererMiddleware',

'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',

'scrapy.spidermiddlewares.depth.DepthMiddleware']
    
    # allowed_domains = ['images.so.com']



