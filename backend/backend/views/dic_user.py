from django.http import HttpResponse,JsonResponse
import requests,json
from backend.models import Score
from django.core import  serializers

def dic_user(request):
    if request.method == 'GET':
        '''获取请求者的IP信息'''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
        # print(ip)

#获取地址
        url = 'http://api.map.baidu.com/location/ip?ak=bpdjSeyOgE2GYwsCSvVYCmPTYQXqohl1&ip={}&coor=bd09ll'.format(ip)

        response = requests.post(url=url)
        res = json.loads(response.text)
        if res['status'] == 0:
            province = res['content']['address_detail']['province']
            if '新疆' in province:
                ip = 'good_user'
            else:
                ip = 'bad_user'
        else:
            ip = 'no data'

        return HttpResponse(content=ip)



# bad_user页面
def bad_user(request):
    if request.method == 'GET':
        result = Score.objects.all()[0:50]
        result = json.loads(serializers.serialize('json', result))
        return JsonResponse(data=result,safe=False)
