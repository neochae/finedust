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
DATABASES_POSTGRESQL = {
    'SCHEMA': 'sep545',
    'USER': 'sep545',
    'PASSWORD': '1234',
    'HOST': '52.78.164.147',
    'PORT': '5432',
}

DATABASES_MYSQL = {
    'SCHEMA': 'sep545',
    'USER': 'sep545',
    'PASSWORD': '1234',
    'HOST': '52.78.164.147',
    'PORT': '3306',
}

#Key
DATAGOKRSERVICEKEY = 'DHLLCOxUmx4Y%2BVmiWJWzlVLbXWTHc4zWli%2FyEHuh2WdfUoya0mR5DZBFfgn5yXgYotvtjyCy7ZkbcT%2Bo4Zv04g%3D%3D'

#images
IMAGE_DIR = BASE_DIR + "/images/"
