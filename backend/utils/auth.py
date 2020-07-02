#!/usr/bin/python                                                                  
# -*-encoding=utf8 -*-                                                             
# @Author         :
# @Email          : imooc@foxmail.com
# @Created at     : 2018/11/2
# @Filename       : auth.py
# @Desc           :


import json
import requests
from utils import proxy
from dongqiudi import settings

from backend.models import User

# from utils.wx.crypt import WXBizDataCrypt
from utils.wx.code2session import code2session


# 判断是否已经授权
def already_authorized(request):
    is_authorized = False

    if request.session.get('is_authorized'):
        is_authorized = True
    return is_authorized


def get_user(request):
    if not already_authorized(request):
        raise Exception('not authorized request')
    open_id = request.session.get('open_id')
    user = User.objects.get(open_id=open_id)
    return user


def c2s(code):
    return code2session(code)


def code2session(code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (settings.WX_APP_ID, settings.WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    return data

