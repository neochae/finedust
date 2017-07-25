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

resp = requests.get('https://api.waqi.info/api/feed/@1451/obs.kr.json')
print(resp.text)

# # response = urllib2.urlopen('https://api.waqi.info/api/feed/@1451/obs.kr.json')
# js_location = pd.read_json('https://api.waqi.info/api/feed/@1451/obs.en.json')

# print(js_location['rxs'][0])