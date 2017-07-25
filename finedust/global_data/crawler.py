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
        json_data = self.get_json(resp)
        js_normal_data = json_normalize(json_data['rxs'][0])
        self.get_forecast_wind_data(js_normal_data)
        self.get_current_dust_data(js_normal_data)

    def get_forecast_wind_data(self, js_normal_data):
        df_dust_wind = json_normalize(js_normal_data['msg.forecast.wind'][0])
        wind_time = pd.DataFrame({'WIND_TIME': df_dust_wind['t']})
        wind_speed = pd.DataFrame({'WIND_SPEED': [item[0] for item in df_dust_wind['w']]})
        wind_direction = pd.DataFrame({'WIND_DIRECTION': [item[2] for item in df_dust_wind['w']]})
        df_totoal_wind = pd.concat([wind_time, wind_speed, wind_direction], axis=1)
        return print(df_totoal_wind)

    def get_current_dust_data(self, data):
        df_dust_current = json_normalize(data['msg.iaqi'][0])

        # print(df_dust_current)
        dust_data_columns = ['PM25','PM10','O3','NO2','SO2','CO','TEMP','DEW','PRESSURE','HUMID','WIND']
        # dust_data = pd.DataFrame([[item[0] for item in df_dust_current['v']]], columns=df_dust_current['p'].tolist())
        dust_data = pd.DataFrame([[item[0] for item in df_dust_current['v']]], columns=dust_data_columns)
        dust_data['TIME'] = df_dust_current['h'][0][0]
        dust_data['CITYNAME'] = data['msg.city.id']
        return print(dust_data)



    def get_json(self, data):
        self.data = data
        return pd.read_json(data.text)

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