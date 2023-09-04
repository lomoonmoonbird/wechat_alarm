#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

import pymysql
from app import config
from app.config import TEMPLATE_ID


def initDataBase():
    try:
        db = pymysql.connect(host=config.DBHOST, user=config.DBUSER, password=config.DBPWD, port=3306)
        cursor = db.cursor()
        cursor.execute(
            "create database if not exists {} default character set UTF8MB4".format(config.DBNAME))
        cursor.close()
        db.close()
        print("创建数据库{}成功".format(config.DBNAME))
    except Exception as e:
        print(e)


def initTable():
    initUser()
    initConfig()


def initUser():
    try:
        db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                             password=config.DBPWD, db=config.DBNAME,
                             port=3306, charset='UTF8MB4')
        cursor = db.cursor()
        sql = 'create table if not exists {}(\
                id int(20) auto_increment,\
                phonenumber varchar(20) default null,\
                verifycode varchar(20) default null,\
                userid varchar(512) default null,\
                isbind bit default 0,\
                primary key(id)\
            )engine=InnoDB default charset=UTF8MB4'.format('user')
        cursor.execute(sql)
        cursor.close()
        db.close()
        print("创建数据表{}成功".format('user'))
    except Exception as e:
        print(e)


def initConfig():
    try:
        db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                             password=config.DBPWD, db=config.DBNAME,
                             port=3306, charset='UTF8MB4')
        cursor = db.cursor()
        sql = '''create table if not exists config(\
                id int(20) auto_increment,\
                APPID varchar(255) default null,\
                APPSECRET varchar(255) default null,\
                TOKEN varchar(512) default null,\
                TEMPLATE_ID varchar(512) default null,\
                primary key(id)\
            )engine=InnoDB default charset=UTF8MB4;'''
        cursor.execute(sql)
        cursor.close()
        db.close()
        config_data = selectConfig()
        if config_data is None:
            insertConfig()
        print("创建数据表{}成功".format('config'))
    except Exception as e:
        traceback.print_exc()


def selectConfig():
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from config where id=1;'

    cursor.execute(sql)
    config_data = cursor.fetchone()
    cursor.close()
    db.close()
    if config_data is not None:
        return {
            'APPID':config_data[1],
            'APPSECRET':config_data[2],
            'TOKEN':config_data[3],
            'TEMPLATE_ID':config_data[4],
        }
    else:
        return None


def insertConfig(APPID=config.APPID,APPSECRET=config.APPSECRET,TOKEN=config.TOKEN,TEMPLATE_ID=config.TEMPLATE_ID):
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'insert into config(APPID,APPSECRET,TOKEN,TEMPLATE_ID) values ("{}","{}","{}","{}");'.format(APPID,
                                                                                   APPSECRET,
                                                                                   TOKEN,
                                                                                   TEMPLATE_ID,
                                                                                   )
    print(sql)
    cursor.execute(sql)
    cursor.execute("commit")
    cursor.close()
    db.close()


def updateConfig(APPID, APPSECRET, TOKEN,TEMPLATE_ID):
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update config set APPID="{}",APPSECRET="{}",TOKEN="{}",TEMPLATE_ID="{}" where id=1;'.format(APPID,
                                                                                   APPSECRET,
                                                                                   TOKEN,TEMPLATE_ID
                                                                                   )
    print(sql)
    cursor.execute(sql)
    cursor.execute("commit")
    cursor.close()
    db.close()


def insertUser(userid, phonenumber, verifycode, isbind):
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'insert into user(userid,phonenumber,verifycode,isbind) values ("{}","{}","{}","{}");'.format(userid,
                                                                                                       phonenumber,
                                                                                                       verifycode,
                                                                                                       isbind
                                                                                                       )
    print(sql)
    cursor.execute(sql)
    cursor.execute("commit")
    cursor.close()
    db.close()


def updateUser( userid, phonenumber, verifycode, isbind):
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'update user set userid="{}",phonenumber="{}",verifycode="{}",isbind="{}" where userid="{}";'.format(userid,
                                                                                                              phonenumber,
                                                                                                              verifycode,
                                                                                                              isbind,
                                                                                                              userid
                                                                                                              )
    print(sql)
    cursor.execute(sql)
    cursor.execute("commit")
    cursor.close()
    db.close()

def deleteUser(userid):
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'delete from user where userid="{}";'.format(userid)
    print(sql)
    cursor.execute(sql)
    cursor.execute("commit")
    cursor.close()
    db.close()


def selectPhoneByUserId(userid):
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'select phonenumber from {} where userid="{}" limit 1;'.format('user', userid)

    cursor.execute(sql)
    phonenumber = cursor.fetchone()
    cursor.close()
    db.close()
    if phonenumber is not None:
        return phonenumber[0]
    else:
        return None

def selectUserIdByPhone(phone):
    db = pymysql.connect(host=config.DBHOST, user=config.DBUSER,
                         password=config.DBPWD, db=config.DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'select userid from {} where phonenumber="{}";'.format('user', phone)
    cursor.execute(sql)
    userid = cursor.fetchone()
    cursor.close()
    db.close()
    if userid is not None:
        return userid[0]
    else:
        return None
