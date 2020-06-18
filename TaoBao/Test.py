import requests
import re
import json
from fake_useragent import UserAgent

ua = UserAgent()

header = {
    'cookie' : 't=add2f635082de13a4ba5d6fbfe49b118; enc=HeAKUF1%2FJDWsEN%2FOV4fbs9rTlBs8CNZYTfaWZ%2BYXi2mseTW95kEZit%2BA54vwZ%2BQnIsbKGhNGsns9twcY96wOGQ%3D%3D; thw=cn; _m_h5_tk=8b68da420ca8f041520b5d1e9a2d14a7_1590226027803; _m_h5_tk_enc=eaa99872dc02128b9f0b26c6a97b1f6d; lLtC1_=1; cookie2=100904e65c3b1c6001e75745e290adf2; _tb_token_=ee17be1b68eea; _samesite_flag_=true; cna=BGg+FyjzyXMCAXAkV7UyHfxu; v=0; tfstk=c611BJxrDcm1SNfZTiae3RB4j2RAwGlB-XxF59VXK_lJt31mpb-7qfYsAXpJR; sgcookie=EnM2IdBCSoofSnFm6oxps; unb=2900179294; uc3=id2=UUGiGxUs3scNiQ%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&nk2=s03nW8R7T8TwvYHguLU%3D&vt3=F8dBxGZiTP%2B0Y2keA3U%3D; csg=07db24d0; lgc=%5Cu4FE1%5Cu7B14%5Cu4E66%5Cu5199%5Cu4E00%5Cu5EA7%5Cu57CE; cookie17=UUGiGxUs3scNiQ%3D%3D; dnk=%5Cu4FE1%5Cu7B14%5Cu4E66%5Cu5199%5Cu4E00%5Cu5EA7%5Cu57CE; skt=a3164dac2f9cf52a; existShop=MTU5MDIzODgwOA%3D%3D; uc4=nk4=0%40sTL0a2XWvX6Kg5bk6qumZ%2F8uHtNeL0XOJA%3D%3D&id4=0%40U2OVEwq6Es4HQbjTQeqoF%2BQgsyt0; tracknick=%5Cu4FE1%5Cu7B14%5Cu4E66%5Cu5199%5Cu4E00%5Cu5EA7%5Cu57CE; _cc_=VFC%2FuZ9ajQ%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%9F%8E47; _nk_=%5Cu4FE1%5Cu7B14%5Cu4E66%5Cu5199%5Cu4E00%5Cu5EA7%5Cu57CE; cookie1=WvSazNZFSZv1fwooatcasdST7Hrp2mdBMoGVfVLO6dQ%3D; mt=ci=10_1; uc1=cookie14=UoTV7NTS4ncKJA%3D%3D&existShop=false&cookie15=URm48syIIVrSKA%3D%3D&cookie21=UIHiLt3xTIkz&pas=0&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D; l=eBMHuI2PQ3qU4c8tBOfwourza77OSIRAguPzaNbMiOCP_YCk5pddWZA6EL8DC3GVh6v9R3ykIQI6BeYBqQAonxvte5DDwQHmn; isg=BKengGtKtXfbazGFE0GaEv_nNttxLHsO_4xMBHkUwzZdaMcqgfwLXuVqjmh2gFOG',
    'User-Agent' : ua.random
}

url = 'https://item.taobao.com/item.htm?spm=a230r.1.14.23.15586fbeNqhL48&id=572122505073&ns=1&abbucket=17#detail'
response = requests.get(url, headers=header)
print(response.text)