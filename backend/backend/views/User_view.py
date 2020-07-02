# -*- encoding=utf-8 -*-

import json

from django.http import JsonResponse
from django.views import View
from utils.response import wrap_json_response, ReturnCode, CommonResponseMixin
from utils.auth import already_authorized, c2s

from backend.models import User

# def test_session(request):
#     request.session['message'] = 'Test Django Session OK!'
#     response = wrap_json_response(code=ReturnCode.SUCCESS)
#     return JsonResponse(data=response, safe=False)


# class UserView(View, CommonResponseMixin):
#     def get(self, request):
#         pass
#
#     def post(self, request):
#         pass


def __authorize_by_code(request):
    '''
    使用wx.login的到的临时code到微信提供的code2session接口授权
    '''
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    # print(post_data)
    code = post_data.get('code')
    nickname = post_data.get('nickname')
    avatar = post_data.get('avatarUrl')
    city = post_data.get('city')
    gender = post_data.get('gender')
    province = post_data.get('province')



    if not code :
        response = 'no code'
        return JsonResponse(data=response, safe=False)

    data = c2s(code)
    openid = data.get('openid')
    # print('get openid: ', openid)
    if not openid:
        response = 'no code'
        return JsonResponse(data=response, safe=False)

    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid, nickname=nickname,avatar=avatar,city=city,gender=gender,province=province)
        new_user.save()
        # print(new_user)

    response = openid
    return JsonResponse(data=response, safe=False)

def authorize(request):
    return __authorize_by_code(request)