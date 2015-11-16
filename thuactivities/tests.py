# -*- coding: utf-8 -*-
"""
Tests for tornado server.
Author: Norrix
2015-11-07
"""

import urllib.request as urllib2

data = '''
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[测试消息]]></Content>
<MsgId>1234567890123456</MsgId>
</xml>
'''.encode('utf-8')

cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)
request = urllib2.Request(
        url = r'http://localhost/weixin?signature=9049f1b29792ff11552050c57e5e3669f18a7225&timestamp=1447671051&nonce=188517302',
        headers = {'Content-Type': 'text/xml'},
        data = data,
    )

print(opener.open(request).read().decode('utf-8'))
