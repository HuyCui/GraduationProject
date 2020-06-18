#encoding=utf-8
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import re
import requests
import json
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from requests.packages.urllib3.util.retry import Retry
import urllib3.contrib.pyopenssl
from bs4 import BeautifulSoup
import pandas as pd
import csv
from DbTools import CsvTool
def func(str1, url):
    prodect_id = re.search('\d+', url).group(0)
    time.sleep(5)
    return str1, [str(prodect_id),str(prodect_id),str(prodect_id),str(prodect_id)], time.time()

def get_result(future):
    res = future.result()
    print(res[0])
    print(res[1])
    print('---'*20)




if __name__ == '__main__':

    browser = webdriver.Chrome()
    url = 'https://item.jd.com/100012407280.html#comment'
    browser.get(url)
    count = 0
    wait = WebDriverWait(browser, 10)
    comments = []
    while True:
        try:
            if count % 10 == 0 and count < 20:
                time.sleep(3)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#comment .comments-list [data-tab=item] .comment-con")))
            soup = BeautifulSoup(browser.page_source.encode("utf-8"), 'lxml')
            url_list = soup.select("#comment .comments-list [data-tab=item] .comment-con")
            stars = soup.select('.comment-star')
            for url, stat in zip(url_list, stars):
                comments.append([url.text.strip(), stat['class'][1][4]])
            count += 1
            next_page = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#comment .ui-page .ui-pager-next")))
            browser.execute_script("arguments[0].click();", next_page)  # 被图标遮挡了
        except TimeoutException:
            print("已爬取", count, "页评论")
            #file.close()
            break
    print(comments)
    CsvTool.wirte2csv('csvData', comments)

    # pool = ThreadPoolExecutor(max_workers=5)
    # for i in range(10000, 10050):
    #     url = 'https://item.jd.com/%d.html' % i
    #     feture = pool.submit(func, 'hello'+str(i), url)
    #     feture.add_done_callback(get_result)
    #
    # pool.shutdown()


