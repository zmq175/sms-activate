# -*- coding=utf-8 -*-
import configparser
import time
import json
import hashlib
import urllib
# import urllib2
import urllib.request
import urllib.parse

from sqlalchemy.orm import Session

import MySQL
import VerifyCodeService


class Request:
    method = ''
    bizContent = ''

    def setBizContent(self, bizContent):
        if type(bizContent) is dict or type(bizContent) is list:
            self.bizContent = json.dumps(bizContent, separators=(',', ':'))
        else:
            self.bizContent = bytes(bizContent)

    def getBizContent(self):
        return self.bizContent

    def setMethod(self, method):
        self.method = method
        return self

    def getMethod(self):
        return self.method


class Client:
    appId = ''
    timestamp = ''
    version = ''
    signType = ''
    secretKey = ''

    def __init__(self):
        self.timestamp = int(round(time.time() * 1000))  # bytes(int(time.mktime(time.time())))
        self.version = '1.0'
        self.signType = 'md5'

    def setAppId(self, appId):
        self.appId = appId

    def setSecretKey(self, secretKey):
        self.secretKey = secretKey

    def setSignType(self, signType):
        self.signType = signType

    def setVersion(self, version):
        self.version = version

    def setTimestamp(self, timestamp):
        self.timestamp = bytes(timestamp)

    def createSignature(self, data, secretKey):
        list = []
        for k in sorted(data):
            list02 = [k, data[k]];
            # print("=".join('%s' %id for id in list02))
            # str02 = '='.json('%s' %id for id in list02)
            list.append("=".join('%s' % id for id in list02))
        list.append('key=' + secretKey)
        return hashlib.md5('&'.join(list).encode("utf-8")).hexdigest().upper()

    def execute(self, request):
        post = {}
        post['app_id'] = self.appId
        post['version'] = self.version
        post['timestamp'] = self.timestamp
        post['biz_content'] = request.getBizContent()
        post['method'] = request.getMethod()
        post['sign_type'] = self.signType
        post['sign'] = self.createSignature(data=post, secretKey=self.secretKey)
        headers = {
            'User-Agent': 'Mozilla 5.0 Python-SMS-SDK v1.0.0 (Haowei tech)'
        }
        # data = urllib.urlencode(post)
        data = urllib.parse.urlencode(post)
        data = data.encode('utf-8')

        # request = urllib2.Request('http://api.shansuma.com/gateway.do', data=data, headers=headers)
        request = urllib.request.Request('http://api.shansuma.com/gateway.do')
        print(data)
        f = urllib.request.urlopen(request, data)
        return f.read().decode('utf-8')
        # return urllib2.urlopen(request).read().decode('utf8')


def send_verify_code(mobile_number, ip):
    # 加载配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 从配置文件中获取信息
    method = config.get('DEFAULT', 'method')
    app_id = config.get('DEFAULT', 'app_id')
    secret_key = config.get('DEFAULT', 'secret_key')
    version = config.get('DEFAULT', 'version')

    # 实例化Request对象并设置请求方法和业务内容
    req = Request()
    req.setMethod(method=method)
    content = json.loads(config.get('DEFAULT', 'content'))
    print(content['sign'])
    verify_code = VerifyCodeService.check_or_create_verify_code(db=MySQL.session, mobile_number=mobile_number, ip=ip)
    req.setBizContent(bizContent={
        'mobile': [mobile_number],    # 接受号码
        'sign': content['sign'],       # 已通过审核的签名内容，这里不加签名id
        'send_time': '',
        'type': 0,
        'template_id': content['template_id'],  # 已通过审核的模板id
        'params': {
            'code': verify_code
        }
    })
    # 实例化Client对象并设置app id、secret key和版本号
    client = Client()
    client.setAppId(appId=app_id)
    client.setSecretKey(secretKey=secret_key)
    client.setVersion(version=version)

    # 发送请求并获取响应结果
    res = client.execute(req)

    print(res)
    return verify_code

if __name__ == '__main__':
    send_verify_code(mobile_number="18610735579", ip="127.0.0.1")