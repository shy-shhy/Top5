# -*- encoding=utf-8 -*-

import json
import requests
from utils import proxy
from dongqiudi import  settings
'''
return data 的格式
{
  "session_key": "JmRNs6uPEpFzlMRmg4NqJQ==",
  "expires_in": 7200,
  "openid": "oXSML0ZH05BItFTFILfgCGxXxxik"
}
'''


def code2session(code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (settings.WX_APP_ID, settings.WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    print(data)
    return data


code = '0216Br0a27RQ9K0T6z0a2iQq0a26Br0D'
code2session(code)