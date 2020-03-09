# 测试阿里云通用文字识别－高精版OCR文字识别
# 接口实例
# 请求说明
# {
#   //图像数据：base64编码，要求base64编码后大小不超过4M，最短边至少15px，最长边最大4096px，支持jpg/png/bmp格式，和url参数只能同时存在一个
#   "img": "",
#   //图像url地址：图片完整URL，URL长度不超过1024字节，URL对应的图片base64编码后大小不超过4M，最短边至少15px，最长边最大4096px，支持jpg/png/bmp格式，和img参数只能同时存在一个
#   "url": "",
#   //是否需要识别结果中每一行的置信度，默认不需要。 true：需要 false：不需要
#   "prob": false,
#   //是否需要单字识别功能，默认不需要。 true：需要 false：不需要
#   "charInfo": false,
#   //是否需要自动旋转功能，默认不需要。 true：需要 false：不需要
#   "rotate": false,
#   //是否需要表格识别功能，默认不需要。 true：需要 false：不需要
#   "table": false,
#   //字块返回顺序，false表示从左往右，从上到下的顺序，true表示从上到下，从左往右的顺序，默认false
#   "sortPage": false
# }

#python3
import urllib.request
import urllib.parse
import json
import time
import base64

with open('scraing.png', 'rb') as f:  # 以二进制读取本地图片
    data = f.read()
    encodestr = str(base64.b64encode(data),'utf-8')
#请求头
headers = {
    # 'Authorization': 'APPCODE 你自己的AppCode',
    'Authorization':'APPCODE 73b27e5fb65c4383b485153301dddcd8',
    'Content-Type': 'application/json; charset=UTF-8'
}

def posturl(url,data={}):
  try:
    params=json.dumps(dict).encode(encoding='UTF8')
    req = urllib.request.Request(url, params, headers)
    r = urllib.request.urlopen(req)
    html =r.read()
    r.close();
    return html.decode("utf8")
  except urllib.error.HTTPError as e:
      print(e.code)
      print(e.read().decode("utf8"))
  time.sleep(1)

if __name__=="__main__":
    url_request="https://ocrapi-advanced.taobao.com/ocrservice/advanced"
    dict = {'img': encodestr}
    html = posturl(url_request, data=dict)
    print(html)