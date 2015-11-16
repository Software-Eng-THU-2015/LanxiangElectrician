# -*- coding: utf-8 -*-
"""
Ref.: https://github.com/doraemonext/wechat-python-sdk/blob/master/wechat_sdk/reply.py
"""

import time

from .messages import WechatMessage

class WechatReply(object):
    def __init__(self, message=None, **kwargs):
        if 'source' not in kwargs and isinstance(message, WechatMessage):
            kwargs['source'] = message.target
        if 'target' not in kwargs and isinstance(message, WechatMessage):
            kwargs['target'] = message.source
        if 'time' not in kwargs:
            kwargs['time'] = int(time.time())

        self._args = dict()
        for k, v in kwargs.items():
            self._args[k] = v


class TextReply(WechatReply):
    """
    回复文字消息
    """
    TEMPLATE = """
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    </xml>
    """

    def __init__(self, message, content):
        """
        :param message: WechatMessage 对象
        :param content: 文字回复内容
        """
        super(TextReply, self).__init__(message=message, content=content)

    def render(self):
        return TextReply.TEMPLATE.format(**self._args)