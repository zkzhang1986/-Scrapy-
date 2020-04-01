# 《精通 scrapy 网络爬虫》第4章 第3节（即4.3）Field元数据 实例

import scrapy

class ExampleItem(scrapy.Item):
    x = scrapy.Field(a='hello', b=[1,2,3])
    y = scrapy.Field(a=lambda x:x**2)

if __name__ == '__main__':
    e = ExampleItem(x=100,y=200)
    print(type(e.fields),e.fields)
    print(type(e.fields['x']),e.fields['x'])
    print(type(e.fields['y']),e.fields['y'])
    print(issubclass(scrapy.Field,dict ))
