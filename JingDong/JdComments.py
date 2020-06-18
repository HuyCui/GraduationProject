#!/usr/bin/python3
# coding: utf-8
# 爬取京东的大量评论作为数据集
# author：cuihui
import requests
import re
import time
import json
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import threading
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import HTTPError,Timeout,RequestException,ProxyError,ConnectTimeout
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from DbTools import MySQLTool
from DbTools import CsvTool
import os


#根据关键字获取第一页  找到页数
def getPage_link(keyword):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    searchUrl = 'http://search.jd.com/'
    driver.get(searchUrl)
    time.sleep(1)
    input_ = wait.until(EC.presence_of_element_located((By.ID, 'keyword')))
    submit = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "input_submit")))
    input_.clear()
    input_.send_keys(keyword)
    submit.click()

    page_ele = driver.find_element_by_css_selector('div#J_bottomPage span.p-skip > em > b') #获取商品的页数
    link_list = []
    goodsId = []
    #url_list = driver.find_elements_by_css_selector(".gl-item .p-name [target=_blank]")
    id_list = driver.find_elements_by_css_selector(".gl-item")
    for id in id_list:
        goodsId.append(id.get_attribute('data-sku'))
    return goodsId



#获取其他页的商品id
def getOtherLink(keyword, page):
    goodsId = []
    for i in range(page):
        url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=%d' %(keyword, 2*i+3)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        id_list = soup.select('li.gl-item')
        for id in id_list:
            #print(id['data-sku'])
            goodsId.append(id['data-sku'])
        time.sleep(random.randint(0,6))
    return goodsId

#处理评论的返回信息回调函数
def parse_comments(future):
    res = future.result()
    #print(res)
    keyword = res[0]
    responseTexts = res[1]
    if responseTexts:
        myLock = threading.Lock()
        myLock.acquire()
        dbtool = MySQLTool.DbTool()
        dbtool.creataTable(keyword)
        dbtool.saveComments(keyword, responseTexts)
        dbtool.closeConn()
        myLock.release()
        #CsvTool.wirte2csv(keyword, responseTexts)
    time.sleep(2)



#取得单一商品的评论返回信息
def getOneGoodComment(keyword, goodId, maxPage):
    url = 'https://item.jd.com/%s.html#comment' %(goodId)
    try:
        print('---正在爬取商品'+goodId)
        responseTexts = []
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        wait = WebDriverWait(driver, 10)
        driver.get(url)
        count = 0
        for page in range(maxPage):
            if count % 10 == 0:
                time.sleep(random.randint(3, 9))
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#comment .comments-list [data-tab=item] .comment-con")))
            soup = BeautifulSoup(driver.page_source, 'lxml')
            comments = soup.select("#comment .comments-list [data-tab=item] .comment-con")
            stars = soup.select('.comment-star')
            for comment, stat in zip(comments, stars):
                responseTexts.append([comment.text.strip(), stat['class'][1][4]])
            count += 1
            next_page = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#comment .ui-page .ui-pager-next")))
            driver.execute_script("arguments[0].click();", next_page)
        driver.quit()
        time.sleep(random.randint(1, 9))
        #print(keyword, responseTexts)
        return keyword, responseTexts
    except TimeoutException as err:
        print(err)
        return None


#根据商品id拼接评论页url 爬取评论
def getAllGoodsComments(keyword, goodsId):
    pool = ThreadPoolExecutor(3)
    for goodId in goodsId:
        maxPage = 15
        future = pool.submit(getOneGoodComment, keyword, goodId, maxPage)
        future.add_done_callback(parse_comments)
    pool.shutdown()



if __name__ == '__main__':
    starttime = time.time()
    goodsId1 = getPage_link('运动鞋')
    goodsId2 = getOtherLink('运动鞋', 14)
    goodsId1.extend(goodsId2)
    print('已获得商品的id，准备开始爬取评论。。。')
    #print(goodsId1)
    time.sleep(10)

    getAllGoodsComments('运动鞋', goodsId1)
    endtime = time.time()
    dtime = endtime - starttime
    print("程序运行时间：%.8s s" % dtime)

