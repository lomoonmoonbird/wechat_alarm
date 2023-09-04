import logging
from wechatpy import parse_message
from wechatpy.events import *
from wechatpy.messages import TextMessage
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply

from app.exceptions import ClientError
from app.model.Menu import parsecontent

from app.model.SQLHelper import *
from wechatpy import WeChatClient

logging = logging.getLogger('runserver.handleWeChatMsg')


# 未认证的订阅号 
# https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433401084
# Message 类的成员变量
# id          消息 id, 64 位整型
# source      消息的来源用户，即发送消息的用户
# target      消息的目标用户
# create_time 消息的发送时间，UNIX 时间戳
# type        消息的类型
def handlemsg(data):
    '''
    处理接受到的消息内容，主要包含微信公众号定义的几种消息事件类型
    :param data:
    :return:
    '''
    config_data = selectConfig()
    if config_data is None:
        raise ClientError('请先配置公众号信息')
    client = WeChatClient(config_data['APPID'], config_data['APPSECRET'])
    msg = parse_message(data)
    if isinstance(msg, UnsubscribeEvent):
        # 取关
        deleteUser(msg.source)
        content = '取关成功'
    elif isinstance(msg, SubscribeEvent) or isinstance(msg, SubscribeScanEvent):
        # 关注
        content = '欢迎关注测试公众号，请先发送 "BD#手机号" 进行绑定手机号'
        client.menu.create({
            "button": [
                {
                    "type": "click",
                    "name": "查询绑定手机号",
                    "key": "GETBIND"
                }, {
                    "type": "click",
                    "name": "解除绑定",
                    "key": "UNBIND"
                }
            ]
        })
        insertUser(msg.source, '', '', '0')

    elif isinstance(msg, TextMessage):
        # 文本消息
        logging.debug('id为{}的用户发送消息:{}'.format(msg.source, msg.content))
        content = msg.content
    elif isinstance(msg, ClickEvent):
        # 按钮点击事件
        if msg.key == 'UNBIND':
            # 手机号解绑按钮
            content = '解除绑定成功,发送 "BD#手机号" 进行绑定手机号'
            updateUser(msg.source, '', '', '0')
        elif msg.key == 'GETBIND':
            # 查询绑定手机号
            phone = selectPhoneByUserId(msg.source)
            content = '您当前绑定手机号为：{}'.format(phone) if phone != '' else '您尚未绑定手机号'
        else:
            # 其他点击事件，目前没有
            content = 'null'
    else:
        content = str(msg)
    txt = parsecontent(content, msg.source)

    xml = txtreply(msg, txt)
    # if(len(records)>=10):
    #    saveContent(DBMSGNAME,DBPWD,'msg',records)
    #    records = []
    # 保存数据
    # stime = msg.create_time.strftime('%Y-%m-%d %H:%M:%S')
    # record = {"openid": msg.source, "name": "", "send": content, "receive": txt, "time": stime}
    # return [xml, record]
    return xml


def txtreply(msg, txt):
    reply = TextReply(content=txt, message=msg)
    xml = reply.render()
    return xml


def imgreply(msg, id):
    reply = ImageReply(message=msg)
    reply.media_id = id
    xml = reply.render()
    return xml


def pushTemp(user, data):
    user_id = user
    # url = 'http://122.112.155.213/index'.format(user_id)
    url = None
    config_data = selectConfig()
    if config_data is None:
        raise ClientError('请先配置公众号信息')
    client = WeChatClient(config_data['APPID'], config_data['APPSECRET'])
    client.message.send_template(user_id, config_data['TEMPLATE_ID'], data, url=url, mini_program=None)


def pushTxt(user_id, msg):
    config_data = selectConfig()
    if config_data is None:
        raise ClientError('请先配置公众号信息')
    client = WeChatClient(config_data['APPID'], config_data['APPSECRET'])
    client.message.send_text(user_id, msg)


def getQRCode():
    config_data = selectConfig()
    if config_data is None:
        raise ClientError('请先配置公众号信息')
    client = WeChatClient(config_data['APPID'], config_data['APPSECRET'])
    # 创建永久的二维码, 参数使用字符串而不是数字id
    res = client.qrcode.create({
        'action_name': 'QR_LIMIT_STR_SCENE',
        'action_info': {
            'scene': {'scene_str': "scan_qrcode_from_scene"},
        }
    })
    ticket = res.get('ticket')
    return client.qrcode.get_url(ticket)
