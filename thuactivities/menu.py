# -*- coding: utf-8 -*-
"""
Create customized menu
Author: Norrix
2015-11-24
"""

from wechat import WechatBasic
wechat = WechatBasic(appid='wxa467435e08f049b6', appsecret='d4624c36b6795d1d99dcf0547af5443d')
baseurl = 'http://115.29.78.42/wechat/'
wechat.create_menu({
    'button':[
        {
            'name': '我',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '我的信息',
                    'url': baseurl + 'myinfo'
                },
                {
                    'type': 'view',
                    'name': '我的活动',
                    'url': baseurl + 'myactivities'
                },
            ]
        },
        {
            'type': 'view',
            'name': '活动广场',
            'url': baseurl + 'activities'
        },
    ]})
print('Success.')