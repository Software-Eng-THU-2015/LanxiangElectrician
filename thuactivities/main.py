# -*- coding: utf-8 -*-
"""
Tornado server of thuactivities.
Author: Norrix
2015-11-07
"""
import tornado.ioloop
import tornado.web
from wechat import WechatBasic

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        token = 'TOKEN'
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        wechat = WechatBasic(token)
        if wechat.check_signature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('fail')

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()