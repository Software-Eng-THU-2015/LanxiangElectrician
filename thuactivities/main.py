# -*- coding: utf-8 -*-
"""
Tornado server of thuactivities.
Author: Norrix
2015-11-07
"""

import tornado.ioloop
import tornado.web
from wechat import WechatBasic


class WeixinHandler(tornado.web.RequestHandler):
    def initialize(self, token, appID, appsecret):
        self.token = token
        self.appID = appID
        self.appsecret = appsecret

    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        wechat = WechatBasic(self.token)
        if wechat.check_signature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('GET: Check signature failed.')

    def post(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        body_text = self.request.body
        wechat = WechatBasic(self.token)
        if wechat.check_signature(signature, timestamp, nonce):
            wechat.parse_data(body_text)
            message = wechat.get_message()

            response = None
            if message.type == 'text':
                if message.content == 'test':
                    response = wechat.response_text('^_^')
                else:
                    response = wechat.response_text(message.content)
            else:
                response = wechat.response_text('未知类型')
            self.write(response)
        else:
            self.write('POST: Check signature failed.')



application = tornado.web.Application([
    (r"/weixin", WeixinHandler, dict(token='TOKEN', appID='wxa467435e08f049b6', appsecret='d4624c36b6795d1d99dcf0547af5443d')),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()