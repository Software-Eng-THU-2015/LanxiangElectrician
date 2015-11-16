# -*- coding: utf-8 -*-
"""
Ref.: https://github.com/doraemonext/wechat-python-sdk/blob/master/wechat_sdk/messages.py
"""

from .exceptions import ParseError

MESSAGE_TYPES = {}



class WechatMessage(object):
    def __init__(self, message):
        self.id = int(message.pop('MsgId', 0))
        self.target = message.pop('ToUserName', None)
        self.source = message.pop('FromUserName', None)
        self.time = int(message.pop('CreateTime', 0))
        self.__dict__.update(message)


def handle_for_type(type):
    def register(f):
        MESSAGE_TYPES[type] = f
        return f
    return register

@handle_for_type('text')
class TextMessage(WechatMessage):
    def __init__(self, message):
        self.content = message.pop('Content', '')
        super(TextMessage, self).__init__(message)


class UnknownMessage(WechatMessage):
    def __init__(self, message):
        self.type = 'unknown'
        super(UnknownMessage, self).__init__(message)