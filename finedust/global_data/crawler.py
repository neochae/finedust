# -*- coding: utf-8 -*-

import sys
import os
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.util.screen import *

#TODO, Crawling
class GlobalDataCrawler :
    def __init__(self,id):
        self.basicUrl = 'https://api.waqi.info/api/feed/@'
        self.id = id
        self.lastUrl = '/obs.kr.json'

    def get_globaldata(self):
        resp = requests.get(self.basicUrl + self.id + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        print(resp.text)

    def start(self):
        self.get_globaldata()
        # self.basicUrl = 'https://api.waqi.info/api/feed'



if __name__ == '__main__':
    id = '1451'
    crawler = GlobalDataCrawler(id)
    crawler.start()

# # response = urllib2.urlopen('https://api.waqi.info/api/feed/@1451/obs.kr.json')
# js_location = pd.read_json('https://api.waqi.info/api/feed/@1451/obs.en.json')

# print(js_location['rxs'][0])