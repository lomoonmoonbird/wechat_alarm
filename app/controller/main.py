#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app
from flask import request, redirect, url_for
import app.config as config
import logging
import datetime
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from app.exceptions import check_exception_time, get_res_message
from app.model.HandleWeChatMsg import handlemsg, pushTemp, getQRCode, pushTxt
from app.model.SQLHelper import *

# 初始化
logging = logging.getLogger('runserver.main')
initDataBase()
initTable()

# 微信消息接口
@app.route('/',methods=["POST","GET"])
@check_exception_time
def main():
    logging.debug('进入主页面')
    if(len(request.args)<2):
       return redirect(url_for('index'))
    try:
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")
        # echostr是微信用来验证服务器的参数，需原样返回
        if echostr:
            try:
                logging.debug('正在验证服务器签名')
                check_signature(config.TOKEN, signature, timestamp, nonce)
                logging.debug('验证签名成功')
                return echostr
            except InvalidSignatureException as e:
                logging.error('检查签名出错: '.format(e))
                return 'Check Error'
        # 也可以通过POST与GET来区别
        # 不是在进行服务器验证，而是正常提交用户数据
        logging.debug('开始处理用户消息')
        # 用户在手机端发送消息处理函数
        result = handlemsg(request.data)
        xml = result
        return xml
    # 处理异常情况或忽略
    except Exception as e:
        traceback.print_exc()
        return traceback.format_exc(e)


@app.route('/index',methods=["GET"])
@check_exception_time
def index():
    image = getQRCode()
    return image


@app.route('/push_temp',methods=["POST"])
@check_exception_time
def push_temp():
    '''
    推送模板告警数据，需要先调用update_config 接口完成公众号信息配置
    :return:
    '''
    warning_level = {
        '0': {'color':'#6DD400','msg':"正常"}, #正常
        '1': {'color':'#6DD400','msg':"告警恢复"}, #告警恢复
        '2': {'color':'#F7B500','msg':"中度告警"}, #中度告警
        '3': {'color':'#FA6400','msg':"严重告警"}, #严重告警
        '4': {'color':'#FF0019','msg':"紧急告警"}, #紧急告警
    }

    data = request.get_json().get("data",{})
    phone = request.get_json().get("phone","")
    title = request.get_json().get("title", "")
    level = request.get_json().get("level", "")
    content = request.get_json().get("content", "")
    if phone == '' or content == '' or level == '':
        return get_res_message("参数缺失", 400, None)
    if level not in warning_level:
        return get_res_message('告警等级需在0-4之间',400,None)

    message_data = {
        "title": {
            "value": title + '\r\n',
            "color": "#FF3300"
        },
        "content": {
            "value": content+ '\r\n',
            "color": "#272525"
        },
        "time": {
            "value": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ '\r\n',
            "color": "#272525"
        },
        "level": {
            "value": warning_level[level]['msg']+ '\r\n',
            "color": warning_level[level]['color']
        }
    }
    userid = selectUserIdByPhone(phone)
    if userid:
        res = pushTemp(userid,message_data, url="www.baidu.com")
        return get_res_message('推送成功', 200, None)
    else:
        return get_res_message('此手机号未查询到用户', 401, None)

@app.route('/push_txt',methods=["POST"])
@check_exception_time
def push_txt():
    # 推送测试信息数据，需要先调用update_config 接口完成公众号信息配置
    msg = request.get_json().get('msg','')
    phone = request.get_json().get('phone','')
    if phone != '' and msg != '':
        userid = selectUserIdByPhone(phone)
        if userid:
            pushTxt(userid,msg)
            return get_res_message('推送成功', 200, None)
        else:
            return get_res_message('此手机号未查询到用户', 401, None)
    else:
        return get_res_message("参数缺失", 400, None)

@app.route('/update_config',methods=["POST"])
@check_exception_time
def update_config():
    '''
    更新公众号配置信息
    :return:
    '''
    APPID = request.get_json().get('APPID','')
    APPSECRET = request.get_json().get('APPSECRET','')
    TOKEN = request.get_json().get('TOKEN','')
    TEMPLATE_ID = request.get_json().get('TEMPLATE_ID','')
    if APPID != '' and APPSECRET != '' and TOKEN != '' and TEMPLATE_ID != '':
        updateConfig(APPID, APPSECRET, TOKEN,TEMPLATE_ID)
        return get_res_message("配置成功", 200, None)
    else:
        return get_res_message("参数缺失", 400, None)


@app.route('/get_user',methods=['GET'])
@check_exception_time
def get_user():
    phone = request.args.get('phone', '')
    if phone == '':
        return get_res_message("参数缺失", 400, None)
    userid = selectUserIdByPhone(phone)
    if userid:
        return get_res_message('查询成功', 200, {'phone':phone,'userid':userid})
    else:
        return get_res_message('此手机号未关注或绑定', 401, None)
