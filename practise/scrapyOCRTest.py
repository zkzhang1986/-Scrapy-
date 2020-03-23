# OCR测试
# 需要先安装 tesseract-ocr 然后安装 pytesseract 调用ocr，同时也需要安装 PIL 或 Pillow 来做图片处理
# pytesseract 安装后需要配置环境变量中的系统变量，否则报错
# 系统变量配置 TESSDATA_PREFIX = C:\Program Files (x86)\Tesseract-OCR\tessdata（删除）
# 可以通过修改 pytesseract.py 中的 tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
# 因为我把tesseract-ocr安装在D盘，后面即是tesseract的路径。
# esseract OCR语言包的下载地址
# https://github.com/tesseract-ocr/tessdata


from PIL import Image
import pytesseract
# import tesserocr
img = Image.open('test02.jpg')
img = img.convert('L')
# img.show()

img1 = Image.open('timg.jpg')
# print('tesserocr_img:',tesserocr.image_to_text(img,lang='chi_sim'))
# print('tesserocr_img1:',tesserocr.image_to_text(img1,lang='chi_sim'))

print('pytesseract_img:',pytesseract.image_to_string(img,lang='chi_sim'))
print('pytesseract_img1:',pytesseract.image_to_string(img1,lang='chi_sim'))


