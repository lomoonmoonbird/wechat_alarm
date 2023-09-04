#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from app.model.SQLHelper import *


def parsecontent(content, userid):
    # command = getcommand(content)
    # if command == 0:
    #     txt = menuReply()
    # elif command == 1:
    #     txt = tempReply(content)
    if content.startswith('BD#'):
        phone_bumber = content.replace('BD#', '')
        print(phone_bumber)
        if selectPhoneByUserId(userid) is None:
            insertUser(userid,phone_bumber,'000000','0')
        else:
            updateUser(userid, phone_bumber, '000000', '0')
        txt = '手机号绑定成功，您绑定的手机号为：' + phone_bumber
    else:
        txt = defaultReply(content)
    return txt



# 伪对话AI
def defaultReply(content):
    return content.replace('你', '我').replace('吗', '呀').replace('?', '!')
