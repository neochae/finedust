# -*- coding: utf-8 -*-

import sys
import os
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.util.dbconnector import *
from finedust.util.database import *

#TODO, Crawling
class GlobalDataCrawler :
    def __init__(self):
        self.basicUrl = 'https://api.waqi.info/api/feed/@'
        self.lastUrl = '/obs.kr.json'
        self.engine = DBconnector().connect_DB()
        self.source_info = database_get_source_id(self.basicUrl)
        self.crawler_info = database_create_crawler_event(self.source_info)
        self.region_info = database_get_china_region()
        self.dust_info = database_get_dust_info()

    def get_globaldata(self,id):
        requests.get('http://aqicn.org/',headers={'User-agent': 'Mozilla/5.0'} )
        requests.get(self.basicUrl + id + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        resp = requests.get(self.basicUrl + id + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        # print(self.dust_info)
        # print(resp.text)
        json_data = self.get_json(resp)
        js_normal_data = json_normalize(json_data['rxs'][0])
        # self.get_forecast_aqi_data(js_normal_data)
        # self.get_forecast_wind_data(js_normal_data)
        self.get_current_dust_data(js_normal_data)
        # print(self.region_info)
        # print(self.crawler_info)

    # def get_forecast_aqi_data(self, data):
    #     df_dust_aqi = json_normalize(data['msg.forecast.aqi'][0])
    #     aqi_time = pd.DataFrame({'AQI_TIME': df_dust_aqi['t']})
    #     aqi_min = pd.DataFrame({'AQI_MIN': [item[0] for item in df_dust_aqi['v']]})
    #     aqi_max = pd.DataFrame({'AQI_MAX': [item[1] for item in df_dust_aqi['v']]})
    #     df_total_aqi = pd.concat([aqi_time, aqi_min, aqi_max], axis=1)
    #     df_total_aqi['AQI_CITY_NAME'] = data['msg.city.name'][0]
    #     #aqi_data insert
    #     df_total_aqi.to_sql(name='finedust_global_aqi', con = self.engine, if_exists='append', index=False)
    #     # self.DBengine.commit()
    #     print("=====AQI 대기질 데이터 불러오기=====")
    #     return print(df_total_aqi)
    #
    # def get_forecast_wind_data(self, data):
    #     df_dust_wind = json_normalize(data['msg.forecast.wind'][0])
    #     wind_time = pd.DataFrame({'WIND_TIME': df_dust_wind['t']})
    #     wind_speed = pd.DataFrame({'WIND_SPEED': [item[0] for item in df_dust_wind['w']]})
    #     wind_direction = pd.DataFrame({'WIND_DIRECTION': [item[2] for item in df_dust_wind['w']]})
    #     df_total_wind = pd.concat([wind_time, wind_speed, wind_direction], axis=1)
    #     df_total_wind['WIND_CITY_NAME'] = data['msg.city.name'][0]
    #     df_total_wind.to_sql(name='finedust_global_wind', con=self.engine, if_exists='append', index=False)
    #     print("=====풍속, 풍향 데이터 불러오기=====")
    #     return print(df_total_wind)

    def get_current_dust_data(self, data):

        df_dust_current = json_normalize(data['msg.iaqi'][0])
        # print(df_dust_current)
        #dust_data_columns = ['PM25','PM10','O3','NO2','SO2','CO','TEMP','DEW','PRESSURE','HUMID','WIND']
        df_dust_current['info'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        df_dust_current['data_avg'] = [item[0] for item in df_dust_current['v']]
        df_dust_current['data_min'] = [item[1] for item in df_dust_current['v']]
        df_dust_current['data_max'] = [item[2] for item in df_dust_current['v']]
        dust_data = df_dust_current[['info', 'data_min', 'data_max', 'data_avg']]
        # dust_data = pd.DataFrame([[item[0] for item in df_dust_current['v']]], columns=df_dust_current['p'].tolist())
        # dust_data = pd.DataFrame([[item[0] for item in df_dust_current['v']]], columns=dust_data_columns)

        dust_data['time'] = df_dust_current['h'][0][0]
        dust_data['region'] = self.region_info[data['msg.city.name'][0]]

        # print(dust_data['info'][0])
        db = DBConnector()
        cursor = db.connection_DB()
        for index, data in dust_data.iterrows():
            sql = "INSERT INTO `finedust_data` " \
                  "VALUES ('0'," + str(data['info']) + "," + str(data['data_min']) + "," + str(data['data_max']) + "," + str(data['data_avg']) + ")"
            print(sql)
            cursor.execute(sql)
            id = cursor.lastrowid

            sql = "INSERT INTO `open_api` " \
                  "VALUES ('0'," + "'" + str(data['time']) + "'" + "," + str(data['region']) + "," + str(self.crawler_info) + "," + str(id) + ")"
            print(sql)
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.

        db.commit_DB()
        cursor.close()
        db.close_DB()

        #dust_data['region'] = data['msg.city.name'][0]
        #dust_data.to_sql(name='finedust_global_info', con=self.engine, if_exists='append', index=False)
        #print("=====실시간 데이터 불러오기=====")
        return dust_data



    def get_json(self, data):
        self.data = data
        return pd.read_json(data.text)

    def get_location(selfs):
        location_info = ['1451','1437','1452','1506','1439']
        return location_info

    def start(self):
        locations = self.get_location()
        for location in locations :
            # print(location)
            self.get_globaldata(location)

        # self.basicUrl = 'https://api.waqi.info/api/feed'

class DBconnector :
    def connect_DB(self):
        connect_str = "mysql+mysqldb://{USER}:{PASSWORD}@{HOST}/{DBNAME}?charset=utf8".format(
            USER=DATABASES_MYSQL['USER'],
            PASSWORD=DATABASES_MYSQL['PASSWORD'],
            HOST=DATABASES_MYSQL['HOST'],
            DBNAME=DATABASES_MYSQL['SCHEMA']
        )
        engine = create_engine(connect_str, encoding='utf-8', echo=False)
        engine.connect()
        return engine


if __name__ == '__main__':
    crawler = GlobalDataCrawler()
    crawler.start()

