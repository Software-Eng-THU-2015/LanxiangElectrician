# -*- coding: utf-8 -*-
"""
Ref.: https://github.com/doraemonext/wechat-python-sdk/blob/master/wechat_sdk/basic.py
"""

import hashlib
# import time
# import json
# import cgi
# from StringIO import StringIO

from .messages import MESSAGE_TYPES, UnknownMessage
from .exceptions import ParseError, NeedParseError, NeedParamError, OfficialAPIError
from .reply import TextReply
from .lib import XMLStore

class WechatBasic(object):
    """
    微信基本功能类
    """
    def __init__(self, token=None, appid=None, appsecret=None, access_token=None, 
                 access_token_expires_at=None):
        """
        @param token: 微信 Token
        @param appid: App ID
        @param appsecret: App Secret
        @param access_token: 直接导入的 access_token 值
        @param access_token_expires_at: 直接导入的 access_token 的过期时间
        """
        self.__token = token
        self.__appid = appid
        self.__appsecret = appsecret
        self.__access_token = access_token
        self.__access_token_expires_at = access_token_expires_at
        self.__is_parsed = False
        self.__message = None

    def check_signature(self, signature, timestamp, nonce):
        """
        验证微信消息真实性
        @param signature: 微信加密签名
        @param timestamp: 时间戳
        @param nonce: 随机数
        @return: 通过验证返回 True, 未通过验证返回 False
        """
        self._check_token()
        if not signature or not timestamp or not nonce:
            return False
        tmp_list = [self.__token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        if signature == hashlib.sha1(tmp_str.encode('utf-8')).hexdigest():
            return True
        else:
            return False

    def parse_data(self, data):
        """
        解析微信服务器发送过来的数据并保存类中
        @param data: HTTP Request 的 Body 数据
        @raises ParseError: 解析微信服务器数据错误, 数据不合法
        """
        result = {}
        if type(data) == bytes:
            data = data.decode('utf-8')
        elif type(data) == str:
            pass
        else:
            raise ParseError('Type of data is not utf-8/unicode.')

        try:
            xml = XMLStore(xmlstring=data)
        except Exception:
            raise ParseError('XML ParseError.')

        result = xml.xml2dict
        result['raw'] = data
        result['type'] = result.pop('MsgType').lower()
        message_type = MESSAGE_TYPES.get(result['type'], UnknownMessage)
        self.__message = message_type(result)
        self.__is_parsed = True

    @property
    def message(self):
        return self.get_message()

    def get_message(self):
        self._check_parse()
        return self.__message
        
    def response_text(self, content, escape=False):
        """
        将文字信息 content 组装为符合微信服务器要求的响应数据
        @param content: 回复文字
        @param escape: 是否转义该文本内容 (默认不转义)
        @return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()
        #content = self._transcoding(content)
        #if escape:
        #    content = cgi.escape(content)
        return TextReply(message=self.__message, content=content).render()

    def _check_parse(self):
        """
        检查是否成功解析微信服务器传来的数据
        """
        if not self.__is_parsed:
            raise NeedParseError

    def _check_token(self):
        """
        检查 Token 是否存在
        """
        if not self.__token:
            raise NeedParamError('Please provide Token parameter in the construction of class.')
