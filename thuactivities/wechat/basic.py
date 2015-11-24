# -*- coding: utf-8 -*-
"""
Ref.: https://github.com/doraemonext/wechat-python-sdk/blob/master/wechat_sdk/basic.py
"""

import hashlib
import requests
import time
import json
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
        if not (type(data) == bytes or type(data) == str):
            raise ParseError('Type of data is not bytes/str.')
        data = self._decoding(data)

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

    def get_access_token(self):
        """
        获取 Access Token 及 Access Token 过期日期, 仅供缓存使用, 如果希望得到原生的 Access Token 请求数据请使用 :func:`grant_token`
        @return: dict 对象, key 包括 `access_token` 及 `access_token_expires_at`
        """
        self._check_appid_appsecret()

        return {
            'access_token': self.access_token,
            'access_token_expires_at': self.__access_token_expires_at,
        }

    def response_text(self, content, escape=False):
        """
        将文字信息 content 组装为符合微信服务器要求的响应数据
        @param content: 回复文字
        @param escape: 是否转义该文本内容 (默认不转义)
        @return: 符合微信服务器要求的 XML 响应数据
        """
        self._check_parse()
        content = self._decoding(content)
        #if escape:
        #    content = cgi.escape(content)
        return TextReply(message=self.__message, content=content).render()

    def grant_token(self, override=True):
        """
        获取 Access Token
        详情请参考 http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
        @param override: 是否在获取的同时覆盖已有 access_token (默认为True)
        @return: 返回的 JSON 数据包
        @raise HTTPError: 微信api http 请求失败
        """
        self._check_appid_appsecret()

        response_json = self._get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.__appid,
                "secret": self.__appsecret,
            }
        )
        if override:
            self.__access_token = response_json['access_token']
            self.__access_token_expires_at = int(time.time()) + response_json['expires_in']
        return response_json

    def create_menu(self, menu_data):
        """
        创建自定义菜单
        """
        self._check_appid_appsecret()
        menu_data = self._decoding_dict(menu_data)
        return self._post(
            url='https://api.weixin.qq.com/cgi-bin/menu/create',
            data=menu_data
        )

    def _check_official_error(self, json_data):
        """
        检测微信公众平台返回值中是否包含错误的返回码
        @raises OfficialAPIError: 如果返回码提示有错误，抛出异常；否则返回 True
        """
        if "errcode" in json_data and json_data["errcode"] != 0:
            raise OfficialAPIError("{}: {}".format(json_data["errcode"], json_data["errmsg"]))

    def _request(self, method, url, **kwargs):
        """
        主动向微信服务器发送请求
        @param method: 请求方法
        @param url: 请求地址
        @param kwargs: 附加数据
        @return: 微信服务器响应的 json 数据
        @raise HTTPError: 微信api http 请求失败
        """
        if "params" not in kwargs:
            kwargs["params"] = {
                "access_token": self.access_token,
            }
        if isinstance(kwargs.get("data", ""), dict):
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        response_json = r.json()
        self._check_official_error(response_json)
        return response_json

    def _get(self, url, **kwargs):
        """
        使用 GET 方法向微信服务器发出请求
        @param url: 请求地址
        @param kwargs: 附加数据
        @return: 微信服务器响应的 json 数据
        @raise HTTPError: 微信api http 请求失败
        """
        return self._request(
            method="get",
            url=url,
            **kwargs
        )

    def _post(self, url, **kwargs):
        """
        使用 POST 方法向微信服务器发出请求
        @param url: 请求地址
        @param kwargs: 附加数据
        @return: 微信服务器响应的 json 数据
        @raise HTTPError: 微信api http 请求失败
        """
        return self._request(
            method="post",
            url=url,
            **kwargs
        )

    def _check_parse(self):
        """
        检查是否成功解析微信服务器传来的数据
        """
        if not self.__is_parsed:
            raise NeedParseError

    @property
    def access_token(self):
        self._check_appid_appsecret()
        if self.__access_token:
            now = time.time()
            if self.__access_token_expires_at - now > 60:
                return self.__access_token
        self.grant_token()
        return self.__access_token

    def _check_token(self):
        """
        检查 Token 是否存在
        """
        if not self.__token:
            raise NeedParamError('Please provide Token parameter in the construction of class.')

    def _decoding(self, data):
        """
        编码转换
        @param data: 需要转换的数据(bytes)
        @return: 转换好的数据(str)
        """
        if not data:
            return data
        result = None
        if isinstance(data, bytes):
            result = data.decode('utf-8')
        else:
            result = data
        return result

    def _decoding_list(self, data):
        """
        编码转换 for list
        @param data: 需要转换的 list 数据
        @return: 转换好的 list
        """
        if not isinstance(data, list):
            raise ValueError('Parameter data must be list object. data = %s' % (data,))

        result = []
        for item in data:
            if isinstance(item, dict):
                result.append(self._decoding_dict(item))
            elif isinstance(item, list):
                result.append(self._decoding_list(item))
            else:
                result.append(self._decoding(item))
        return result

    def _decoding_dict(self, data):
        """
        编码转换 for dict
        @param data: 需要转换的 dict 数据
        @return: 转换好的 dict
        """
        if not isinstance(data, dict):
            raise ValueError('Parameter data must be dict object. data = %s' % (data,))

        result = {}
        for k, v in data.items():
            k = self._decoding(k)
            if isinstance(v, dict):
                v = self._decoding_dict(v)
            elif isinstance(v, list):
                v = self._decoding_list(v)
            else:
                v = self._decoding(v)
            result.update({k: v})
        return result

    def _check_appid_appsecret(self):
        """
        检查 AppID 和 AppSecret 是否存在
        @raises NeedParamError: AppID 或 AppSecret 参数没有在初始化的时候完整提供
        """
        if not self.__appid or not self.__appsecret:
            raise NeedParamError('Please provide app_id and app_secret parameters in the construction of class.')