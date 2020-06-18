#!/usr/bin/python3
# coding: utf-8
# 根据某件商品的链接获取商品的评论
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



#处理评论的返回信息回调函数
def parse_comments(res):
    print(res)
    goodId = res[0]
    responseTexts = res[1]
    if responseTexts:
        CsvTool.writeDetail2Csv(goodId, responseTexts)
    time.sleep(2)



#取得单一商品的评论返回信息
def getOneGoodComment(goodId, maxPage):
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
            for comment in comments:
                responseTexts.append(comment.text.strip())
            count += 1
            next_page = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#comment .ui-page .ui-pager-next")))
            driver.execute_script("arguments[0].click();", next_page)
        driver.quit()
        time.sleep(random.randint(1, 9))
        return goodId, responseTexts
    except TimeoutException as err:
        print(err)
        return None


#取得单一商品的评论返回信息
def getOneGoodComment2(goodId, maxPage):
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
            for comment in comments:
                responseTexts.append(comment.text.strip())
            count += 1
            next_page = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#comment .ui-page .ui-pager-next")))
            driver.execute_script("arguments[0].click();", next_page)
        driver.quit()
        time.sleep(random.randint(1, 9))
        return goodId, responseTexts
    except TimeoutException as err:
        print(err)
        return None

#
# if __name__ == '__main__':
#
#     comments = getOneGoodComment('100006728101', 5)
#     print(len(comments[1]))
#     parse_comments(comments)