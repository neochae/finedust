#settings for AWS working

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(PROJECT_DIR)

#Crawler
PHANTOM_WEBDRIVER = "/usr/bin/phantomjs"

#Telegram
TELEGRAM_TOKEN = "380017530:AAEngJF7oCIos-WzKf-XDOwKTumhoV-H5KE"

#Naver Login
NID = 'kaistsw2017'
NPWD = 'naver111'


#Database
DATABASES = {
    'NAME': 'sep545',
    'USER': 'sep545',
    'PASSWORD': '1234',
    'HOST': '52.78.164.147',
    'PORT': '5432',
}

#Key
