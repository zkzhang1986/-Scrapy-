import scrapy
from ..items import BookItem
from scrapy.linkextractors import LinkExtractor
class BooksSpider(scrapy.Spider):
    # 爬虫名，每一个爬虫的唯一标识
    name = 'books'
    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个。
    #start_urls = ['http://books.toscrape.com/']

    # 实现 start_resquests 方法代替start_urls类属性
    def start_requests(self):
        yield scrapy.Request('http://books.toscrape.com/',
                             callback=self.parse,
                             headers={'User-Agent':'Mozill/5.0'},
                             dont_filter=True)


    def parse(self, response):
        # 提取数据
        # 重写
        for sel in response.css('article.product_pod'):
            book = BookItem() # from ..items import BookItem 类
            book['name'] = sel.xpath('./h3/a/@title').extract_first()
            book['price'] = sel.css('p.price_color::text').extract_first()
            yield book

        # for book in response.css('article.product_pod'):
            # name = book.xpath('./h3/a/@title').extract_first()
            # price = book.css('p.price_color::text').extract_first()
            # yield {
            #     'name': name,
            #     'price': price
            # }

        # 提取下一页链接
        # 下一页链接在 ul.pager > li.next > a 里
        '''
        <ul class="pager">          
            <li class="current"> Page 1 of 50 </li>           
            <li class="next"><a href="catalogue/page-2.html">next</a></li>            
        </ul>
		#default > div > div > div > div > section > div:nth-child(2) > div > ul.pager > li.next > a
        '''
        # next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        # if next_url:
        #     next_url = response.urljoin(next_url)
        #     yield scrapy.Request(next_url, callback=self.parse)

        # 提取下一页链接重写（用 LinkExtractor提取）
        # 说明 from scrapy.linkextractors import LinkExtractor
        le = LinkExtractor(restrict_css='ul.pager li.next')
        links = le.extract_links(response)
        # print(type(links),links)
        if links:
            # 用links[0]获取的Link对象属性是绝对链接地址，无需要用response.urljoin拼接
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

