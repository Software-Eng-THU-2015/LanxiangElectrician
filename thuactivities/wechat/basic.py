# -*- coding: utf-8 -*-
"""
Ref.: https://github.com/doraemonext/wechat-python-sdk/blob/master/wechat_sdk/basic.py
"""

import hashlib
# import time
# import json
# import cgi
# from StringIO import StringIO

from .exceptions import ParseError, NeedParseError, NeedParamError, OfficialAPIError

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
        self.__is_parse = False
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


    def _check_token(self):
        """
        检查 Token 是否存在
        """
        if not self.__token:
            raise NeedParamError('Please provide Token parameter in the construction of class.')
