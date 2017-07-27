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
cursor = connection.cursor()
sql = "SELECT DISTINCT CITY_NAME FROM `finedust_global_info` "
cursor.execute(sql)
result = cursor.fetchall()

a = pd.DataFrame(result)
b = a['CITY_NAME'].tolist()
print(b)