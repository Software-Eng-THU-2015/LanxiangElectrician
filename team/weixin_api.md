# 微信API功能

## 基础支持
* 获取access_token（2000次/日）
说明：全局票据，512个字符长度，有效期7200秒。
请求：GET方式
> https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET

正常返回
> {"access_token":"ACCESS_TOKEN","expires_in":7200}

错误返回
> {"errcode":40013,"errmsg":"invalid appid"}

## 接收普通消息
* 验证消息真实性
说明：收到消息后判断token、timestamp、nonce进行sha1加密后的signature以验证消息是否来自微信。

* 文本消息
```
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName> 
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[this is a test]]></Content>
<MsgId>1234567890123456</MsgId>
</xml>
```

* 图片消息
```
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<PicUrl><![CDATA[this is a url]]></PicUrl>
<MediaId><![CDATA[media_id]]></MediaId>
<MsgId>1234567890123456</MsgId>
</xml>
```

## 接受事件推送
* 关注/取关事件
说明：5s无响应会发起重试，共3次。
```
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[subscribe]]></Event>
</xml>
```

* 扫描二维码事件
说明：略

* 上报地理位置事件
说明：每次进入公众号时都会上报地理位置。

* 自定义菜单事件（点击了click类按钮）
说明：如果有子菜单，那么不会产生事件上报。
```
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[CLICK]]></Event>
<EventKey><![CDATA[EVENTKEY]]></EventKey>
</xml>
```

* 点击菜单链接跳转事件（点击了view类按钮）
```
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[VIEW]]></Event>
<EventKey><![CDATA[www.qq.com]]></EventKey>
</xml>
```
