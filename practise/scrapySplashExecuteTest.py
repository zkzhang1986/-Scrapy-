# 《精通scrapy网络爬虫》 第11章 11.1.1 测试 Splash execute 端点

import requests
import json

lua_scripy = '''
    function main(splash)
        splash:go("http:example.com") --打开页面
        splash:wait(0.5) --等待加载
        local title = splash:evaljs("document.title") --执行 js 代码获取结果
        return {title=title} --返回 json 形式的结果
    end
'''
splash_url = 'http://192.168.99.100:8050/execute'
headers = {'content-type':'application/json'}
data = json.dumps({'lua_source':lua_scripy})
reaponse = requests.post(splash_url, headers=headers, data=data)
print(reaponse.content)
print(reaponse.json())