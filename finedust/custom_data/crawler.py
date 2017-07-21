# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time

#driver = webdriver.Chrome('../../chromedriver/mac/chromedriver')
driver = webdriver.PhantomJS('../../phantomjs/mac/bin/phantomjs')
driver.implicitly_wait(3)

driver.get('https://nid.naver.com/nidlogin.login')
time.sleep(3)

driver.find_element_by_name('id').send_keys('kaistsw2017')
driver.find_element_by_name('pw').send_keys('naver111!')
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
driver.get('http://cafe.naver.com/dustout2?iframe_url=/ArticleList.nhn%3Fsearch.clubid=29031243%26search.boardtype=L')
driver.switch_to.frame("cafe_main");

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

notices = soup.select("td.board-list > span > span.aaa")
print(len(notices))
for n in notices:
    print(n.text.strip())


