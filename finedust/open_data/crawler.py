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

# Connect to the database
connection = pymysql.connect(host=DATABASES_MYSQL['HOST'],
                             user=DATABASES_MYSQL['USER'],
                             password=DATABASES_MYSQL['PASSWORD'],
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

class OpenDataCrawler :
    def __init__(self,id):
        self.basicUrl = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMinuDustFrcstDspth?searchDate='
        self.today = date.today().strftime('%Y-%m-%d')
        self.servieKey = '&ServiceKey=' + DATAGOKRSERVICEKEY
        self.lastUrl = '&ver=1.1&_returnType=json'

    def get_oepndata(self):
        resp = requests.get(self.basicUrl + self.today + self.servieKey + self.lastUrl, headers={'User-agent': 'Mozilla/5.0'})
        # with open('air_korea_forecast_sample.json', 'rt', encoding='UTF8') as data_file:
        #     resp = json.load(data_file)
        json_data = self.get_json(resp)
        json_normal_data = json_normalize(json_data['list'][0])
        self.updateDatabase(json_normal_data)

    def get_json(self, data):
        return json.loads(data.text)

    def updateDatabase(self, data):
        image = data['imageUrl7'][0]
        dateTime = data['dataTime'][0]
        print(image)
        print(dateTime)
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

    def start(self):
        self.get_oepndata()

if __name__ == '__main__':
    crawler = OpenDataCrawler(id)
    crawler.start()
