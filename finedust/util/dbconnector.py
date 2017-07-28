# -*- coding: utf-8 -*-
import sys
import os
import pymysql.cursors
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *

class DBConnector :
    def __init__(self):
        self.connection = pymysql.connect(host=DATABASES_MYSQL['HOST'],
                             user=DATABASES_MYSQL['USER'],
                             password=DATABASES_MYSQL['PASSWORD'],
                             db=DATABASES_MYSQL['SCHEMA'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def connection_DB(self):
      return self.connection.cursor()

    def close_DB(self):
      return self.connection.close()

    def commit_DB(self):
        self.connection.commit()

if __name__ == '__main__':
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "SELECT `region`.`name`,  `region_category`.`name` FROM `region`, `region_category` WHERE `region`.`category` = `region_category`.`category_id`"
    cursor.execute(sql)
    result = cursor.fetchall()
    a = pd.DataFrame(result)
    print(a)