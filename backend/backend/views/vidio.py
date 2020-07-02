import  json
from django.http import HttpResponse,JsonResponse
from backend.models import DongqiudiVidio,VidioUser
import time,datetime
from django.core import  serializers
from django.forms.models import model_to_dict
import random


#返回视频数据
def vidio(request):
    class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)

    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    # start = post_data.get('start')
    open_id = post_data.get('open_id')
    num = random.randint(0,613)

    if open_id =='false':
        result =DongqiudiVidio.objects.filter(no__gte=num)[0:15]
        result = json.loads(serializers.serialize('json', result))
        return JsonResponse(data=result,safe=False)

    else:
        pinglun = []
        ping =DongqiudiVidio.objects.filter(no__gte=num)[0:15]
        for dic in ping:
            dic = model_to_dict(dic)
            url = dic['mp4']
            result =  VidioUser.objects.filter(vidio_url=url,open_id=open_id)
            if result:
                for i in result:
                    dic['shou'] =1 if i.shoucang==1 else 0
                    dic['likes'] =1 if i.like == 1 else 0
                    pinglun.append(dic)
            else:
                dic['shou']=0
                dic['likes']=0
                pinglun.append(dic)

        return JsonResponse(data=pinglun,safe=False)

# 点击新闻事件
def click_video(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    url = post_data.get('url')

    result = DongqiudiVidio.objects.filter(mp4=url)
    for dic in result:
        count = dic.dianji
        new_count = count+1
    DongqiudiVidio.objects.filter(mp4=url).update(dianji=new_count)
    return HttpResponse(content='ok')

#点击，收藏，点赞
def click_dianshou(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)

    url = post_data.get('url')
    open_id = post_data.get('open_id')
    action = post_data.get('action')

    if action == 'unfav':
        VidioUser.objects.filter(open_id=open_id,vidio_url=url).update(shoucang=0)
        result = DongqiudiVidio.objects.filter(mp4=url)
        for dic in result:
            count = dic.shoucang
            count  -=1
        DongqiudiVidio.objects.filter(mp4=url).update(shoucang=count)

    elif action == 'fav':
        if VidioUser.objects.filter(open_id=open_id,vidio_url=url):
            VidioUser.objects.filter(open_id=open_id,vidio_url=url).update(shoucang=1)
            result = DongqiudiVidio.objects.filter(mp4=url)
            for dic in result:
                count = dic.shoucang
                count += 1
            DongqiudiVidio.objects.filter(mp4=url).update(shoucang=count)
        else:
            new_data = VidioUser(open_id=open_id,vidio_url=url,like=0,shoucang=1,fanxiang=0)
            new_data.save()

            result = DongqiudiVidio.objects.filter(mp4=url)
            for dic in result:
                count = dic.shoucang
                count += 1
            DongqiudiVidio.objects.filter(mp4=url).update(shoucang=count)


    if action == 'unlike':
        VidioUser.objects.filter(open_id=open_id,vidio_url=url).update(like=0)
        result = DongqiudiVidio.objects.filter(mp4=url)
        for dic in result:
            count = dic.like
            count -= 1
        DongqiudiVidio.objects.filter(mp4=url).update(like=count)

    elif action == 'like':
        if VidioUser.objects.filter(open_id=open_id,vidio_url=url):
            VidioUser.objects.filter(open_id=open_id,vidio_url=url).update(like=1)
            result = DongqiudiVidio.objects.filter(mp4=url)
            for dic in result:
                count = dic.like
                count += 1
            DongqiudiVidio.objects.filter(mp4=url).update(like=count)
        else:
            new_data = VidioUser(open_id=open_id,vidio_url=url,like=1,shoucang=0,fanxiang=0)
            new_data.save()

            result = DongqiudiVidio.objects.filter(mp4=url)
            for dic in result:
                count = dic.shoucang
                count += 1
            DongqiudiVidio.objects.filter(mp4=url).update(like=count)

    return HttpResponse(content='ok')

#分享
def fenxiang(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    url = post_data.get('url')
    result =  DongqiudiVidio.objects.filter(mp4=url)
    for i in result:
        count = i.fenxiang
        count+=1
    DongqiudiVidio.objects.filter(mp4=url).update(fenxiang=count)
    return HttpResponse(content='ok')


# 分享视频页面
def share_url(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    url = post_data.get('url')

    result = DongqiudiVidio.objects.filter(mp4=url)
    result = json.loads(serializers.serialize('json', result))

    return JsonResponse(data=result,safe=False)



