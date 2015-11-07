# -*- coding: utf-8 -*-
"""
Ref.: https://github.com/doraemonext/wechat-python-sdk/blob/master/wechat_sdk/__init__.py
"""

__all__ = ['WechatBasic']

try:
    from wechat.basic import WechatBasic
except ImportError:
    pass