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
    def __init__(self):
        self.basicUrl = 'https://api.waqi.info/api/feed/@'
        self.lastUrl = '/obs.kr.json'

    def get_globaldata(self,id):
        resp = requests.get(self.basicUrl + id + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        # print(resp.text)
        json_data = self.get_json(resp)
        js_normal_data = json_normalize(json_data['rxs'][0])
        print(self.get_forecast_aqi_data(js_normal_data))
        print(self.get_forecast_wind_data(js_normal_data))
        print(self.get_current_dust_data(js_normal_data))

    def get_forecast_aqi_data(self, data):
        df_dust_aqi = json_normalize(data['msg.forecast.aqi'][0])
        aqi_time = pd.DataFrame({'AQI_TIME': df_dust_aqi['t']})
        aqi_min = pd.DataFrame({'AQI_MIN': [item[0] for item in df_dust_aqi['v']]})
        aqi_max = pd.DataFrame({'AQI_MAX': [item[1] for item in df_dust_aqi['v']]})
        df_total_aqi = pd.concat([aqi_time, aqi_min, aqi_max], axis=1)
        df_total_aqi['CITY_NAME'] = data['msg.city.id'][0]
        print("=====AQI 대기질 데이터 불러오기=====")
        return print(df_total_aqi)

    def get_forecast_wind_data(self, data):
        df_dust_wind = json_normalize(data['msg.forecast.wind'][0])
        wind_time = pd.DataFrame({'WIND_TIME': df_dust_wind['t']})
        wind_speed = pd.DataFrame({'WIND_SPEED': [item[0] for item in df_dust_wind['w']]})
        wind_direction = pd.DataFrame({'WIND_DIRECTION': [item[2] for item in df_dust_wind['w']]})
        df_total_wind = pd.concat([wind_time, wind_speed, wind_direction], axis=1)
        df_total_wind['CITY_NAME'] = data['msg.city.id'][0]
        print("=====풍속, 풍향 데이터 불러오기=====")
        return print(df_total_wind)

    def get_current_dust_data(self, data):
        df_dust_current = json_normalize(data['msg.iaqi'][0])

        # print(df_dust_current)
        dust_data_columns = ['PM25','PM10','O3','NO2','SO2','CO','TEMP','DEW','PRESSURE','HUMID','WIND']
        # dust_data = pd.DataFrame([[item[0] for item in df_dust_current['v']]], columns=df_dust_current['p'].tolist())
        dust_data = pd.DataFrame([[item[0] for item in df_dust_current['v']]], columns=dust_data_columns)
        dust_data['TIME'] = df_dust_current['h'][0][0]
        dust_data['CITY_NAME'] = data['msg.city.id'][0]
        print("=====실시간 데이터 불러오기=====")
        return print(dust_data)



    def get_json(self, data):
        self.data = data
        return pd.read_json(data.text)

    def get_location(selfs):
        location_info = ['1451','1449','1450','1453']
        return location_info

    def start(self):
        locations = self.get_location()
        for location in locations :
            # print(location)
            self.get_globaldata(location)

        # self.basicUrl = 'https://api.waqi.info/api/feed'



if __name__ == '__main__':
    crawler = GlobalDataCrawler()
    crawler.start()
