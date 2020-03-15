# 11.2 在 Scrapy 中使用 Splash

## 配置 settings.py

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