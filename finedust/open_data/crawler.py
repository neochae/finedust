# -*- coding: utf-8 -*-
import sys
import os
import time
import datetime
import pymysql.cursors
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.util.screen import *
from finedust.util.database import *

region_dict = {
    'busan': '부산',
    'chungbuk': '충북',
    'chungnam': '충남',
    'daegu': '대구',
    'daejeon': '대전',
    'gangwon': '강원',
    'gwangju': '광주',
    'gyeongbuk': '경북',
    'gyeonggi': '경기',
    'gyeongnam': '경남',
    'incheon': '인천',
    'jeju': '제주',
    'jeonbuk': '전북',
    'jeonnam': '전남',
    'sejong': '세종',
    'seoul': '서울',
    'ulsan': '울산'
}

class OpenDataCrawler :
    def __init__(self):
        self.basicUrl = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMinuDustFrcstDspth?searchDate='
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.servieKey = '&ServiceKey=' + DATAGOKRSERVICEKEY
        self.lastUrl = '&ver=1.1&_returnType=json'
        self.avgBasicUrl = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?itemCode=PM10&dataGubun=HOUR&searchCondition=WEEK&pageNo=1&numOfRows=1'
        self.source_info = database_get_source_id(self.basicUrl)
        self.crawler_info = database_create_crawler_event(self.source_info)
        self.region_info = database_get_domestic_region()
        self.dust_info = database_get_dust_info()

    def get_oepndata(self):
        # resp = requests.get(self.basicUrl + self.today + self.servieKey + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        # json_data = self.get_json(resp)
        # json_normal_data = json_normalize(json_data['list'][0])
        # self.updateDatabase(json_normal_data)

        try:
            resp = requests.get(self.avgBasicUrl + self.servieKey + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'},
                                timeout=30)
            if (resp.status_code == 200):
                json_data = self.get_json(resp)
                json_normal_data = json_normalize(json_data['list'][0])
                self.updateAvgDatabase(json_normal_data)
            else:
                print(resp)
        except requests.exceptions.RequestException as e:
            print(e)



    def get_json(self, data):
        return json.loads(data.text)

    def updateDatabase(self, data):
        image = data['imageUrl7'][0]
        dateTime = data['dataTime'][0]

        # Connect to the database
        connection = pymysql.connect(host=DATABASES_MYSQL['HOST'],
                                     user=DATABASES_MYSQL['USER'],
                                     password=DATABASES_MYSQL['PASSWORD'],
                                     db='mydb',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `finedust_forecast` WHERE `dateTime`=%s"
                cursor.execute(sql, (dateTime,))
                result = cursor.fetchone()
                # If the forecast doesn't exist in database, we should update the forecase
                if (result) :
                    print('Duplicated Data')
                else :
                    with connection.cursor() as cursor:
                        # Create a new record
                        sql = "INSERT INTO `finedust_forecast` (`dateTime`, `image`) VALUES (%s, %s)"
                        print(sql)
                        cursor.execute(sql, (dateTime, image))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()
        finally:
            connection.close()

    def updateAvgDatabase(self, data):
        # Connect to the database
        connection = pymysql.connect(host=DATABASES_MYSQL['HOST'],
                                     user=DATABASES_MYSQL['USER'],
                                     password=DATABASES_MYSQL['PASSWORD'],
                                     db=DATABASES_MYSQL['SCHEMA'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                for region_key, region_value in region_dict.items():
                    # Create a new record
                    sql = "INSERT INTO `finedust_data` " \
                          "VALUES ('0'," + str(2) + "," + str(data[region_key][0]) + "," + str(data[region_key][0]) + "," + str(data[region_key][0]) + ")"
                    print(sql)
                    cursor.execute(sql)
                    id = cursor.lastrowid

                    sql = "INSERT INTO `open_api` " \
                          "VALUES ('0'," + "'" + self.date + "'" + "," + str(self.region_info[region_value]) + "," + str(self.crawler_info) + "," + str(id) + ")"
                    print(sql)
                    cursor.execute(sql)

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        finally:
            connection.close()

    def start(self):
        self.get_oepndata()

if __name__ == '__main__':
    crawler = OpenDataCrawler()
    crawler.start()
