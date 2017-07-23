# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys

sys.path.append("..")
sys.path.append("../..")
from finedust.settings.setting import *
#from finedust.settings.local_setting import *

base_url = 'http://cafe.naver.com/dustout2'
driver = webdriver.PhantomJS(PHANTOM_WEBDRIVER)
driver.implicitly_wait(3)

#login
driver.get('https://nid.naver.com/nidlogin.login')
time.sleep(3)
driver.find_element_by_name('id').send_keys(NID)
driver.find_element_by_name('pw').send_keys(NPWD)
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

#access main page
url = base_url + '?iframe_url=/ArticleList.nhn?search.clubid=29031243&search.boardtype=L'
driver.get(url)
driver.switch_to.frame("cafe_main");

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

notices = soup.select("td.board-list > span > span.aaa")
print(len(notices))
for n in notices:
    print(n.text.strip())


