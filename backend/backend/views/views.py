# -*- coding: utf-8 -*-
import  json
from django.http import HttpResponse,JsonResponse
from backend.models import NurIndex,NurNews,NurSlideShow,\
    Schedule,NewsPriase,Shoucang,ClickNews,Comment,CommentPrice
from django.core import  serializers
from django.db.models import Q
import random
from django.forms.models import model_to_dict
from datetime import date, datetime
import time as t
import random
import  datetime as f
# 首页新闻列表
def index(request):
    if request.method == 'POST':
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        start = received_body.get('start')

#新闻
        news = []
        result = NurIndex.objects.all().order_by("-pub_time")[start-30:start]
        result = json.loads(serializers.serialize('json', result))

        for dic in result:
            url = dic['pk']

            count = Comment.objects.filter(url=url).count()
            dic['comment'] = count
            news.append(dic)
#轮播图

        slide_show={}
        resutl = NurSlideShow.objects.all().order_by('id').reverse()[0:5]
        slide_show['list'] = json.loads(serializers.serialize('json', resutl))

# 比赛
        contest ={}
        now_date=datetime.now()

        result = Schedule.objects.filter(start_paly__gte=now_date)[0:2]
        contest['list'] = json.loads(serializers.serialize('json',result))

        res =[news,slide_show,contest]

        return JsonResponse(data=res, safe=False, status=200)


# 下拉
def index_xiala(request):
    received_body = request.body.decode('utf-8')
    received_body = json.loads(received_body)
    start = received_body.get('start')

    news = {}
    result = NurIndex.objects.all().order_by("-pub_time")[start - 30:start]
    news['result'] = json.loads(serializers.serialize('json', result))
    return JsonResponse(data=news,safe=False)

#字典切片函数
def dict_slice(ori_dict, start, end):
    """
    字典类切片
    :param ori_dict: 字典
    :param start: 起始
    :param end: 终点
    :return:
    """
    slice_dict = {k: ori_dict[k] for k in list(ori_dict.keys())[start:end]}
    return slice_dict


#详情页
def news_detail(request):
    if request.method == 'POST':
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        uid = received_body.get('uid')
        openid = received_body.get('openid')
        # print(uid)
        # print(openid)

# 点击量
        count = NurIndex.objects.filter(uid=uid)
        for i in count:
            if i.count is None:
                clik = random.randint(20,120)
            else:
                dic = random.randint(1,3)
                clik = i.count + dic
            NurIndex.objects.filter(uid=uid).update(count=clik)

# 相关的内容查找功能
        data={}
        result = NurNews.objects.filter(url=uid)
        data['list'] = json.loads(serializers.serialize('json',result))
        dic = data['list'][0]['fields']

        news_index = []
        index_a = dic['a']
        index_b = dic['b']
        index_c = dic['c']
        index_d = dic['d']
        index_e = dic['e']

        news_index.append(index_a)
        news_index.append(index_b)
        news_index.append(index_c)
        news_index.append(index_d)
        news_index.append(index_e)


# 返回相关的新闻
        data = {}
        result = NurIndex.objects.filter(Q(title__contains=index_a) | Q(title__contains=index_b))
        data['list'] = json.loads(serializers.serialize('json', result))
        index = data['list'][0:4]


#头部

        more_list = []
        more = {}
        more['title'] = dic['title']
        more['time'] = dic['pub_time']
        more_list.append(more)

#新闻内容

        item = {}
        dic = dict_slice(dic,0,26)
        for i in dic:
            if  len(dic[i]) > 2:
                if 'نۇر تورى تەرجىمىسى' not in dic[i]:
                    item[i]= dic[i]


        list = []
        for i in item:
            news = {}
            if '.jpg' in item[i] and 'https://' in item[i] or '.gif' in item[i]:
                news['a'] = item[i]
            elif '.mp4' in item[i]:
                news['b'] = item[i]
            else:
                news['c'] = item[i]

            # print(news)
            list.append(news)


# 新闻点赞状态
        priase = []
#         if openid == 'false':
#             priase.append('false')
#         else:
#             if not NewsPriase.objects.filter(url=uid, open_id=openid):
#                 priase.append('false')
#             else:
#                 priase.append("true")

# 点赞的数量
        count = []


# 收藏
        shoucang = []
        if openid == 'false':
            shoucang.append('false')
        else:
            if not Shoucang.objects.filter(url=uid, open_id=openid):
                shoucang.append('false')
            else:
                shoucang.append("true")

#返回评论
        pinglun = []
        ping = Comment.objects.filter(url=uid,verify=1).order_by('-like_count')[0:4]
        for dic in ping:
            dic = model_to_dict(dic)
            comment_id = dic['comment_id']
            if openid == 'false':
                dic['CommentPrice'] = 'false'
                pinglun.append(dic)
            else:
                if not CommentPrice.objects.filter(comment_id=comment_id,open_id=openid):
                    dic['CommentPrice'] ='false'
                    pinglun.append(dic)
                else:
                    dic['CommentPrice'] = 'true'
                    pinglun.append(dic)

# 新闻点赞头像
        ava = NewsPriase.objects.filter(url=uid).order_by('-pub_time')
        avatar= json.loads(serializers.serialize('json', ava))

#评论总数
        comment = []
        count = Comment.objects.filter(url=uid).count()
        comment.append(count)

# 最后返回
        data=[
            more_list,list,index,news_index,priase,count,shoucang,pinglun,avatar,comment
        ]

        # return JsonResponse(data=data,safe=False,json_dumps_params={'ensure_ascii':False},content_type='application/json')
        return JsonResponse(data=data,safe=False)


#比赛页面下拉
def scheduler_bot(request):
    if request.method == 'POST':
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        start = received_body.get('start')
        new_date = (f.datetime.now()+f.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")

        data = {}
        result = Schedule.objects.filter(start_paly__gte=new_date).order_by("start_paly")[start-30:start]
        data['list'] = json.loads(serializers.serialize('json', result))

        return JsonResponse(data=data,safe=False)

#比赛页面上拉
def scheduler_top(request):
    if request.method == 'POST':
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        start = received_body.get('start')
        new_date = (f.datetime.now()+f.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")

        data = {}
        result = Schedule.objects.filter(start_paly__lte=new_date).order_by("-start_paly")[start-30:start]
        data['list'] = json.loads(serializers.serialize('json', result))

        return JsonResponse(data=data,safe=False)