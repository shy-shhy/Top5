import  json
from django.http import HttpResponse,JsonResponse
from backend.models import NewsPriase,Shoucang,Comment,CommentPrice
import time,datetime
from django.core import  serializers
from django.forms.models import model_to_dict
# from datetime import date, datetime



# 点赞
def newsprice(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    url = post_data.get('url').strip()
    openId = post_data.get('openid').strip()
    avatar = post_data.get('avatar')


# 新闻点赞
    if not NewsPriase.objects.filter(url=url, open_id=openId):
        put_time = datetime.datetime.now()
        new_url = NewsPriase(url=url, open_id=openId,avatar=avatar,pub_time=put_time)
        new_url.save()

        return HttpResponse(content='create suc')

    else:
        #如果没有openid 判断用户还没点赞
        NewsPriase.objects.filter(url=url,open_id=openId).delete()
        return HttpResponse(content='delete suc')



# 收藏
def shoucang(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    url = post_data.get('url').strip()
    openId = post_data.get('openid').strip()

    # 如果没有新闻URL 直接保存
    if not Shoucang.objects.filter(url=url, open_id=openId):
        new_url = Shoucang(url=url, open_id=openId)
        new_url.save()

        return HttpResponse(content='create suc')

    # 如果URL存在 判断有没有用户的openid
    else:
        # 如果没有openid 判断用户还没点赞
            Shoucang.objects.filter(url=url, open_id=openId).delete()
            return HttpResponse(content='del suc')


# 写评论
def send_comment(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)

    url = post_data.get('url')
    open_id = post_data.get('open_id')
    nick_name = post_data.get('nickname')
    avatar = post_data.get('avatar')
    comment = post_data.get('value')
    comment_id = open_id + str(int(time.time()))
    cur = datetime.datetime.now()

    new_comment = Comment(url=url,open_id=open_id,nickname=nick_name,avatar=avatar,value=comment,comment_id=comment_id,like_count=0,cur=cur,verify=0)
    new_comment.save()


    return HttpResponse(content='ok')


# 点赞评论
def comment_price(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)

    open_id = post_data.get('open_id')
    comment_id = post_data.get('comment_id')

    if not CommentPrice.objects.filter(open_id=open_id,comment_id=comment_id):
        new_price = CommentPrice(open_id=open_id, comment_id=comment_id)
        new_price.save()

        count = Comment.objects.filter(comment_id=comment_id)
        for i in count:
            dic = i.like_count + 1
            Comment.objects.filter(comment_id=comment_id).update(like_count=dic)
        return HttpResponse(content='ok')

    else:
        CommentPrice.objects.filter(open_id=open_id, comment_id=comment_id).delete()
        return HttpResponse(content='ok')


# 评论页面
def comment_detail(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    uid = post_data.get('url')
    openid = post_data.get('openId')

    data = []


    pinglun = []
    ping = Comment.objects.filter(url=uid,verify=1).order_by('-like_count')[0:4]
    for dic in ping:
        dic = model_to_dict(dic)
        comment_id = dic['comment_id']
        if openid == 'false':
            dic['CommentPrice'] = 'false'
            pinglun.append(dic)
        else:
            if not CommentPrice.objects.filter(comment_id=comment_id, open_id=openid):
                dic['CommentPrice'] = 'false'
                pinglun.append(dic)
            else:
                dic['CommentPrice'] = 'true'
                pinglun.append(dic)


    allcomment = []
    ping = Comment.objects.filter(url=uid,verify=1).order_by('-cur')[:]
    for dic in ping:
        dic = model_to_dict(dic)
        comment_id = dic['comment_id']
        if openid == 'false':
            dic['CommentPrice'] = 'false'
            allcomment.append(dic)
        else:
            if not CommentPrice.objects.filter(comment_id=comment_id, open_id=openid):
                dic['CommentPrice'] = 'false'
                allcomment.append(dic)
            else:
                dic['CommentPrice'] = 'true'
                allcomment.append(dic)

    data =[
        pinglun,allcomment
    ]

    return  JsonResponse(data=data ,safe=False)


