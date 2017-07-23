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

#Key
