# -*- coding: utf-8 -*-
import sys
import os
import pymysql.cursors
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.util.dbconnector import *

def database_add_user(chat_id):
    db = DBConnector()
    cursor = db.connection_DB()
    sql = "REPLACE INTO `telegram_user` (`chat_id`) " \
          "VALUES (" + str(chat_id) + ")"
    cursor.execute(sql)
    db.commit_DB()
    cursor.close()
    db.close_DB()
    #print(sql)

def database_create_crawler_event(source_id):
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "INSERT INTO `crawling_event` (`crawling_id`, `source`) " \
          "VALUES (0, " + str(source_id) + ")"
    cursor.execute(sql)
    event_id = cursor.lastrowid
    db.commit_DB()
    cursor.close()
    db.close_DB()
    #print(sql, event_id)
    return event_id

def database_get_custom_category():
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "SELECT `name`, `category_id` " \
          "FROM `region_category` " \
          "WHERE `name` != '대한민국' " \
          "AND `name` != '중국'"
    cursor.execute(sql)
    categories = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close_DB()

    return dict(zip(categories.name, categories.category_id))


def database_get_custom_region():
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "SELECT `region`.`name`, `region`.`region_id` " \
          "FROM `region`, `region_category` " \
          "WHERE `region`.`category`=`region_category`.`category_id` AND `region_category`.`name`!='중국' AND `region_category`.`name`!='대한민국'"
    cursor.execute(sql)
    regions = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close_DB()

    return dict(zip(regions.name, regions.region_id))


def database_get_china_region():
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "SELECT `region`.`name`, `region`.`region_id` " \
          "FROM `region`, `region_category` " \
          "WHERE `region`.`category`=`region_category`.`category_id` AND `region_category`.`name`='중국'"
    cursor.execute(sql)
    regions = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close_DB()

    return dict(zip(regions.name, regions.region_id))


def database_get_domestic_region():
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "SELECT `region`.`name`, `region`.`region_id` " \
          "FROM `region`, `region_category` " \
          "WHERE `region`.`category`=`region_category`.`category_id` AND `region_category`.`name`='대한민국'"
    cursor.execute(sql)
    regions = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close_DB()

    return dict(zip(regions.name, regions.region_id))


def database_get_dust_info():
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "SELECT `finedust_info`.`name`, `finedust_info`.`info_id` FROM `finedust_info`"
    cursor.execute(sql)
    dusts = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close_DB()

    return dict(zip(dusts.name, dusts.info_id))


def database_add_to_favorite(chat_id, region):
    print(chat_id, region, " 관심지역 추가")
    #TODO, database query


def database_remove_favorite(chat_id, region):
    print(chat_id, region, " 관심지역 삭제")
    #TODO, database query


def database_get_source_id(base_url):
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "SELECT `source_id` FROM `source_info` WHERE `url`="+"'"+base_url+"'"
    print(sql)

    cursor.execute(sql)
    ids = pd.DataFrame(cursor.fetchall())
    cursor.close()
    db.close_DB()

    return ids['source_id'].tolist()[0]

'''
    미세먼지 정보를 database에 넣기 위한 API 
    region : region table의 키 값 (INT)
    crawler : crawling_event 키 값 (INT)
    time : 오염원이 측정된 시간 (DATIME format string)
    dust : finedust_info의 키 값 (INT)
    min, max, average : 측정 값들
'''
def database_add_finedust_data(region, crawler, time, dust, min, max, average):
    db = DBConnector()
    cursor = db.connection_DB()

    sql = "INSERT INTO `finedust_data` " \
          "VALUES ('0',"+str(dust)+","+ str(min)+","+str(max)+","+str(average)+")"
    cursor.execute(sql)
    id = cursor.lastrowid
    print(id, sql)

    sql = "INSERT INTO `open_api` " \
          "VALUES ('0',"+"'"+time+"'"+","+str(region)+","+str(crawler)+","+str(id)+")"
    print(sql)

    cursor.execute(sql)
    db.commit_DB()
    cursor.close()
    db.close_DB()
