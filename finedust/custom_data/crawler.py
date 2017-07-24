# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys
import re
from io import BytesIO
from PIL import Image

sys.path.append("..")
sys.path.append("../..")

from finedust.settings.local_setting import *
from finedust.util.screen import *

class CustomDataCrawler:
    def __init__(self):
        self.club_id = 29031243
        self.base_url = 'http://cafe.naver.com/dustout2'
        self.mobile_base_url = 'http://m.cafe.naver.com/dustout2'
        self.login_url = 'https://nid.naver.com/nidlogin.login'
        self.login_xpath = '//*[@id="frmNIDLogin"]/fieldset/input'
        self.main_iframe = 'cafe_main'
        self.main_element = 'td.board-list > span > span.aaa'
        self.detail_category = '#ct > div.post_title > a.tit_menu > span.ellip'
        self.detail_title = '#ct > div.post_title > h2'
        self.detail_writer = '#ct > div.post_title > * > a.nick > span.end_user_nick > span'
        self.detail_date = '#ct > div.post_title > * > span.date.font_l'
        self.detail_content = '#postContent'
        self.capture = False

        self.driver = webdriver.PhantomJS(PHANTOM_WEBDRIVER)
        #self.driver = webdriver.Chrome('../chromedriver/mac/chromedriver')
        self.driver.implicitly_wait(3)
        self.groups = {"서울시 수치 공유": {'category': 6, 'start': 7, 'end': 16},
                       "경기도 수치 공유": {'category': 17, 'start': 18, 'end': 35},
                       "강원도 수치 공유": {'category': 36, 'start': 37, 'end': 42},
                       "충청도 수치 공유": {'category': 43, 'start': 44, 'end': 55},
                       "경상도 수치 공유": {'category': 56, 'start': 57, 'end': 72},
                       "전라도 수치 공유": {'category': 73, 'start': 74, 'end': 84},
                       "제주도 수치 공유": {'category': 85, 'start': 86, 'end': 87}}

    def login(self):
        print('login ...')
        self.driver.get(self.login_url)
        time.sleep(5)
        self.driver.find_element_by_name('id').send_keys(NID)
        self.driver.find_element_by_name('pw').send_keys(NPWD)
        self.driver.find_element_by_xpath(self.login_xpath).click()
        self.driver.implicitly_wait(3)
        time.sleep(2)
        print('login complete')

    def process_category(self):
        main_url = self.base_url + '?iframe_url=/ArticleList.nhn?search.clubid=%s' % (self.club_id)
        main_url = main_url + '%26' + 'search.boardtype=L'

        self.driver.get(main_url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        categories = dict()
        for key in self.groups.keys():
            menu_group = '#group%d' % (self.groups[key]['category'])
            element = soup.select(menu_group)
            if len(element) == 1:
                for content in element[0].contents:
                    if hasattr(content, "contents"):
                        menuid = re.findall('menuid=(\d+)', content.contents[2].attrs['href'])
                        title = content.contents[2].contents[0]
                        categories[title] = menuid

        return categories


    def process_main_url(self, menuid=None):
        main_url = self.base_url + '?iframe_url=/ArticleList.nhn?search.clubid=%s' % (self.club_id)
        if menuid is not None:
            main_url = main_url + '%26' + 'search.menuid=%s' % (menuid)
        main_url = main_url + '%26' + 'search.boardtype=L'

        #articles
        self.driver.get(main_url)
        time.sleep(10)
        self.driver.switch_to.frame(self.main_iframe);
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #image save
        if self.capture:
            page_screenshot(self.driver, 'images/main_%s.png' % (menuid))

        articles = list()
        links = soup.select(self.main_element)
        for n in links:
            detail_href = n.contents[1].attrs['href']
            articleid = re.findall('articleid=(\d+)', detail_href)
            if len(articleid) == 1:
                articles.append(articleid[0])
        return articles

    def process_sub_url(self, articleid=None):
        if articleid is None:
            pass

        #detail pages
        detail_url = self.mobile_base_url + '/%s' % (articleid)
        self.driver.get(detail_url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #image save
        if self.capture:
            page_screenshot(self.driver, 'images/article_%s.png' % (articleid))

        #contente
        category = self.find_element(soup, self.detail_category)
        title = self.find_element(soup, self.detail_title)
        writer = self.find_element(soup, self.detail_writer)
        date = self.find_element(soup, self.detail_date)
        content = self.find_element(soup, self.detail_content)

        print(detail_url)
        print(category, title, writer, date, content, '\n')

    def find_element(self, soup, rule):
        elements = soup.select(rule)
        for ele in elements:
            return ele.text.strip()
        return ''

    def start(self):
        self.login()

        categories = self.process_category()
        for key in categories.keys():
            print(key, categories[key])

        articles = self.process_main_url()
        for article in articles:
            self.process_sub_url(articleid=article)


if __name__ == '__main__':
    crawler = CustomDataCrawler()
    crawler.start()
