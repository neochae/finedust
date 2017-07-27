# -*- coding: utf-8 -*-
import sys
import os
import time
from datetime import date
import pymysql.cursors
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.util.screen import *

class OpenDataCrawler :
    def __init__(self,id):
        self.basicUrl = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMinuDustFrcstDspth?searchDate='
        self.today = date.today().strftime('%Y-%m-%d')
        self.servieKey = '&ServiceKey=' + DATAGOKRSERVICEKEY
        self.lastUrl = '&ver=1.1&_returnType=json'
        self.avgBasicUrl = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?itemCode=PM10&dataGubun=HOUR&searchCondition=WEEK&pageNo=1&numOfRows=1'

    def get_oepndata(self):
        resp = requests.get(self.basicUrl + self.today + self.servieKey + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        json_data = self.get_json(resp)
        json_normal_data = json_normalize(json_data['list'][0])
        self.updateDatabase(json_normal_data)

        resp = requests.get(self.avgBasicUrl + self.servieKey + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        json_data = self.get_json(resp)
        json_normal_data = json_normalize(json_data['list'][0])
        self.updateAvgDatabase(json_normal_data)

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
        dateTime = data['dataTime'][0]
        busan = data['busan'][0]
        chungbuk = data['chungbuk'][0]
        chungnam = data['chungnam'][0]
        daegu = data['daegu'][0]
        daejeon = data['daejeon'][0]
        gangwon = data['gangwon'][0]
        gwangju = data['gwangju'][0]
        gyeongbuk = data['gyeongbuk'][0]
        gyeonggi = data['gyeonggi'][0]
        gyeongnam = data['gyeongnam'][0]
        incheon = data['incheon'][0]
        jeju = data['jeju'][0]
        jeonbuk = data['jeonbuk'][0]
        jeonnam = data['jeonnam'][0]
        sejong = data['sejonggit'][0]
        seoul = data['seoul'][0]
        ulsan = data['ulsan'][0]

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
                sql = "SELECT * FROM `finedust_me` WHERE `dateTime`=%s"
                cursor.execute(sql, (dateTime,))
                result = cursor.fetchone()
                # If the forecast doesn't exist in database, we should update the forecase
                if (result) :
                    print('Duplicated Data')
                else :
                    with connection.cursor() as cursor:
                        # Create a new record
                        sql = "INSERT INTO `finedust_me` (`dateTime`, `busan`, `chungbuk`," \
                              " `chungnam`, `daegu`, `daejeon`, `gangwon`, `gwangju`," \
                              " `gyeongbuk`, `gyeonggi`, `gyeongnam`, `incheon`, `jeju`," \
                              " `jeonbuk`, `jeonnam`, `sejong`, `seoul`, `ulsan`)" \
                              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        print(sql)
                        cursor.execute(sql, (dateTime, busan, chungbuk, chungnam, daegu, daejeon, gangwon, gwangju, gyeongbuk,
                                             gyeonggi, gyeongnam, incheon, jeju, jeonbuk, jeonnam, sejong, seoul, ulsan))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()
        finally:
            connection.close()

    def start(self):
        self.get_oepndata()

if __name__ == '__main__':
    crawler = OpenDataCrawler(id)
    crawler.start()
