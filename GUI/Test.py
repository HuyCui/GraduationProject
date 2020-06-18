import re
import emoji
link = "https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w20166435-22830699636.2.8b5a75973Eahwi&id=613832405367&scene=taobao_shop&sku_properties=10004:7195672376;5919063:6536025"
res = re.search('(\d*?)&scene', link)
print(res.group(1))
str =  '女生用电脑其他不太懂，颜值至上！😁长得很漂亮无限接近macbook，价格还便宜很多，很满意哦！屏幕清晰度很高，大小也刚刚好，完美！'
l = emoji.demojize(str)
print(l)