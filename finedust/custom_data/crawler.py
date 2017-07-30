# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import sys
import re
import datetime
from selenium.common.exceptions import TimeoutException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.util.screen import *
from finedust.util.database import *

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
        self.source_info = database_get_source_id(self.base_url)
        self.crawler_info = database_create_crawler_event(self.source_info)
        self.region_info = database_get_custom_region()
        self.dust_info = database_get_dust_info()
        self.range_ex = ["(\d+-\d+)", "(\d+~\d+)"]
        self.max_ex = ["최대\s*(\d+)", "~\s*(\d+)"]
        self.single_ex = ["초미세\s*(\d+)", "\s+(\d+)$", "\w+(\d+)$"]

        self.driver = webdriver.PhantomJS(PHANTOM_WEBDRIVER)
        #self.driver = webdriver.Chrome('../chromedriver/mac/chromedriver')
        self.driver.implicitly_wait(20)
        self.driver.set_page_load_timeout(20)
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
        time.sleep(2)
        print('login complete')

    def process_category(self):
        main_url = self.base_url + '?iframe_url=/ArticleList.nhn?search.clubid=%s' % (self.club_id)
        main_url = main_url + '%26' + 'search.boardtype=L'

        try:
            self.driver.get(main_url)
        except TimeoutException as e:
            print(e)
            return dict()

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
                        categories[title] = menuid[0]

        return categories


    def process_main_url(self, menuid=None):
        main_url = self.base_url + '?iframe_url=/ArticleList.nhn?search.clubid=%s' % (self.club_id)
        if menuid is not None:
            main_url = main_url + '%26' + 'search.menuid=%s' % (menuid)
        main_url = main_url + '%26' + 'search.boardtype=L'

        #articles
        try:
            self.driver.get(main_url)
            time.sleep(10)
        except TimeoutException as e:
            print(e)
            return

        self.driver.switch_to.frame(self.main_iframe);
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #image save
        if self.capture:
            page_screenshot(self.driver, IMAGE_DIR + 'main_%s.png' % (menuid))

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
        try:
            self.driver.get(detail_url)
        except TimeoutException as e:
            print(e)
            return

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #image save
        if self.capture:
            page_screenshot(self.driver, IMAGE_DIR + 'article_%s.png' % (articleid))

        #contente
        category = self.find_element(soup, self.detail_category)
        title = self.find_element(soup, self.detail_title)
        writer = self.find_element(soup, self.detail_writer)
        date = self.find_element(soup, self.detail_date)
        content = self.find_element(soup, self.detail_content)

        #contente, for database
        date = datetime.datetime.strptime(date, '%Y.%m.%d. %H:%M')
        min, max, avg = self.find_dust_data([title, content])

        print(detail_url)
        print(category, title, writer, date, content)
        print(min, max, avg)

        if avg is not None:
            if category in self.region_info.keys():
                print("수치 정보를 database에 추가합니다 ", articleid, "\n")
                database_add_finedust_custom_data(
                    self.region_info[category],
                    self.crawler_info,
                    date.strftime("%Y-%m-%d %H:%M:%S"),
                    self.dust_info['PM25'],
                    min, max, avg,
                    articleid,
                    title,
                    content,
                    writer,
                    detail_url)
            else:
                print("지역 정보를 찾을 수 없습니다 ", articleid, category, "\n")
        else:
            print("수치 정보를 찾을 수 없습니다 ", articleid, "\n")

    def find_element(self, soup, rule):
        elements = soup.select(rule)
        for ele in elements:
            return ele.text.strip()
        return ''

    def find_dust_data(self, datas):
        for data in datas:
            for ex in self.range_ex:
                range = re.findall(ex, data)
                if (len(range) > 0):
                    range_string = range[0].replace('~', '-')
                    min_max_val = [int(s) for s in range_string.split("-") if s.isdigit()]
                    min = min_max_val[0]
                    max = min_max_val[0]
                    avg = int(sum(min_max_val)/len(min_max_val))
                    return min, max, avg

            for ex in self.max_ex:
                max = re.findall(ex, data)
                if (len(max) > 0):
                    max_val = int(max[0])
                    return max_val, max_val, max_val

            for ex in self.single_ex:
                single = re.findall(ex, data)
                if (len(single) > 0):
                    single_val = int(single[0])
                    return single_val, single_val, single_val

        return None, None, None

    def start_first(self):
        self.login()

        articles = list()
        categories = self.process_category()
        for menu in categories.keys():
            print(menu, categories[menu], " 지역 게시판 자료를 수집합니다")
            articles.extend(self.process_main_url(menuid=categories[menu]))

        print("게시글에 대한 상세 자료를 수집합니다", len(articles))
        for article in articles:
            self.process_sub_url(articleid=article)

    def start(self):
        self.login()
        print("메인 페이지에서 갱신된 새로운 글 자료를 수집합니다")
        articles = self.process_main_url()
        print("게시글에 대한 상세 자료를 수집합니다", len(articles))
        for article in articles:
            self.process_sub_url(articleid=article)


    def test(self):
        test_data = ["광명6동 3-5", "관악구 남현동 4~6", "금천경찰서 근처 75-80(칼더)", "성북구 안암동(10~13)",
                     "광명하안8단지, 최대21 [1]", "광명 철산동 ~~60", "금천경찰서 근처 최대 98",
                     "관악 삼성동 초미세23", "초미세 34", "잠실4동 23", "고양시 삼송지구신원동16"]

        range_ex = ["(\d+-\d+)", "(\d+~\d+)"]
        max_ex = ["최대\s*(\d+)", "~\s*(\d+)"]
        single_ex = ["초미세\s*(\d+)", "\s+(\d+)$", "\w+(\d+)$"]

        for content in test_data:
            for ex in range_ex:
                range = re.findall(ex, content)
                if (len(range) > 0):
                    range_string = range[0].replace('~', '-')
                    min_max_val = [int(s) for s in range_string.split("-") if s.isdigit()]
                    print("범위 수치", content, " : ", min_max_val)
                    break

            for ex in max_ex:
                max = re.findall(ex, content)
                if (len(max) > 0):
                    max_val = int(max[0])
                    print("최대 수치", content, " : ", max_val)
                    break

            for ex in single_ex:
                single = re.findall(ex, content)
                if (len(single) > 0):
                    single_val = int(single[0])
                    print("단독 수치", content, " : ", single_val)
                    break

if __name__ == '__main__':
    crawler = CustomDataCrawler()
    crawler.start_first()
    crawler.start()
