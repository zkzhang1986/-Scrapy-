# 11 爬取动态页面
    安装  在docker中安装 splash
    运行：$ docker pull scrapinghub/splash
    运行： 在docker中运行 splash
    运行：$ docker run -p 8050:8050 scrapinghub/splash
    
## 11.2 在 Scrapy 中使用 Splash
## 11.3 项目实战：爬取toscrape中的名言

##### 配置 settings.py

    # Splash 服务器地址
    SPLASH_URL = 'http://192.168.99.100:8050'

    # 设置去重过滤
    DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
     
    # Enable or disable spider middlewares
    # See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
    # 用来支持 cache_args (可选)
    SPIDER_MIDDLEWARES = {
       # 'splash_examples.middlewares.SplashExamplesSpiderMiddleware': 543,
        'scrapy_splash.SplashDeduplicateArgsMiddleware':100,
    }
    
    # Enable or disable downloader middlewares
    # See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
    DOWNLOADER_MIDDLEWARES = {
       # 'splash_examples.middlewares.SplashExamplesDownloaderMiddleware': 543,
        'scrapy_splash.SplashCookiesMiddleware':723,
        'scrapy_splash.SplashMiddleware':725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware':810
    }
    
## 11.4 项目实战：爬取京东商城中的书籍信息
    涉及点：JavaScript、jQuery以及 console 调试 
    用 execute 端点爬取
    settings.py
    # 伪装成常规浏览器
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/78.0.3904.108 Safari/537.36'
             
