#!/bin/env python
#coding:utf-8


import urllib.request,json
import sys
from optparse import OptionParser


# 更改为自己公众号参数
corpid = 'wxccee75962d4a1085'
secret = '4567eb1feecde10b12cf7e93602e96cd'
toparty = '0'
agentid = '0'


class WeChat(object):
        __token_id = ''
        # init attribute
        def __init__(self,url):
                self.__url = url.rstrip('/')
                self.__corpid = corpid
                self.__secret = secret

        # Get TokenID
        def authID(self):
                params = {'appid':self.__corpid, 'secret':self.__secret, "grant_type":"client_credential"}
                data = urllib.parse.urlencode(params)

                content = self.getToken(data)
                # print(content)
                try:
                        self.__token_id = content['access_token']
                        # print content['access_token']
                except KeyError:
                        raise KeyError

        # Establish a connection
        def getToken(self,data,url_prefix='/'):
                url = self.__url + url_prefix + 'token?'
                try:
                        response = urllib.request.Request(url + data)
                except KeyError:
                        raise KeyError
                result = urllib.request.urlopen(response)
                content = json.loads(result.read())
                return content

        # Get sendmessage url
        def postData(self,data,url_prefix='/'):
                url = self.__url + url_prefix + 'message/custom/send?access_token=%s' % self.__token_id
                request = urllib.request.Request(url,data.encode('UTF-8'))
                try:
                        result = urllib.request.urlopen(request)
                except urllib.request.HTTPError as e:
                        if hasattr(e,'reason'):
                                print ('reason',e.reason)
                        elif hasattr(e,'code'):
                                print ('code',e.code)
                        return 0
                else:
                        content = json.loads(result.read())
                        result.close()
                return content

        # send message
        def sendMessage(self,title,content):

                self.authID()

                data = json.dumps({
                        'touser':"obuB86Sry12G-JCY679L-0JZwQu4",
                        'toparty':toparty,
                        'msgtype':"text",
                        'agentid':agentid,
                        'text':{
                                "content": "Title:  {0}\n Content:  {1}".format(title, content)
                        },
                        'safe':"0"
                },ensure_ascii=False)

                response = self.postData(data)
                print (response)

if __name__ == '__main__':
        a = WeChat('https://api.weixin.qq.com/cgi-bin')
        title, content = sys.argv[1], sys.argv[2]
        parser = OptionParser()
        parser.add_option("-t", "--title", dest="title", default=title, )
        parser.add_option("-c", "--content", dest="content", default=content, )
        (options, args) = parser.parse_args()

        a.sendMessage(options.title,options.content)