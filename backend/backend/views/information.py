# -*- coding: utf-8 -*-
import  json
from django.http import HttpResponse,JsonResponse
from backend.models import Score,Team,GameMatch,Jieshao,Player
from django.core import  serializers
from django.db.models import Q
from django.forms.models import model_to_dict


#积分榜
def score_info(request):
    if request.method == 'POST':
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        id = received_body.get('id')

        l = ["英超","西甲","意甲","德甲",'法甲']

        No = l[id]

        data={}
        result = Score.objects.filter(leage=No).order_by('ranking')
        data['list'] = json.loads(serializers.serialize('json',result))

        L = ['yingchao','xijia','yijia','dejia','fajia']
        id = L[id]

        res = Jieshao.objects.values(id)
        data['res_list'] = list(res)

        return JsonResponse(data=data, safe=False)


#球员榜
def top_player(request):
    if request.method == 'POST':
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        contry = received_body.get('id')
        top = received_body.get('top')

        if top == 3:
            scroll = received_body.get('scroll')

            list = ["英超", "西甲", "意甲", "德甲", '法甲', '土超']
            contry = list[contry]
#积分榜
            items = [
                '射手榜',  '助攻榜',   '黄牌',     '红牌',     '射门', '射正',
                '点球',    '击中门框', '尝试过人',  '成功过人', '越位',  '被犯规',
                '传球',    '关键传球', '传球成功率','成功传球', '成功直塞','成功长传',
                '争项总数', '争项成功', '抢断',     '抢断成功', '解围',   '拦载',
                '防线最后一人完成抢断', '犯规', '乌龙球','失误导致失球',   '被过',
                '丢失球权','扑救', '扑出点球', '出场次数', '出场时间','首发','右脚进球',
                '左脚进球','头球进球','禁区内进球','禁区外进球','造点球','抢回球权',
                '送点球','直接任意球进球','运动战进球','快攻进球','单刀球','禁区内射门',
                '禁区外射门','右脚射门','左脚射门','封堵传球','造点球','创造进球机会',
                '拦载成功'
            ]

            scroll = items[scroll]

            data = {}
            result = Player.objects.filter(leage=contry, be_from=scroll).order_by('ranking')
            data['list'] = json.loads(serializers.serialize('json', result))

            return JsonResponse(data=data, safe=False)
# 球员榜
        if top == 2:
            scroll = received_body.get('scroll')

            list = ["英超", "西甲", "意甲", "德甲", '法甲']
            contry = list[contry]

            items = [
                '射手榜', '助攻榜',   '黄牌',     '红牌',     '射门', '射正',
                '点球',    '击中门框', '尝试过人',  '成功过人', '越位',  '被犯规',
                '传球',    '关键传球', '传球成功率','成功传球', '成功直塞','成功长传',
                '争项总数', '争项成功', '抢断',     '抢断成功',  '拦截',
                '防线最后一人完成抢断', '犯规', '乌龙球','失误导致失球',   '被过',
                '丢失球权','扑救', '扑出点球', '出场次数', '出场时间','首发','右脚进球',
                '左脚进球','头球进球','禁区内进球','禁区外进球','造点球','抢回球权',
                '送点球','直接任意球进球','运动战进球','快攻进球','单刀球','禁区内射门',
                '禁区外射门','右脚射门','左脚射门','封堵传球','造点球','创造进球机会',
                '拦截成功'
            ]

            scroll = items[scroll]

            data = {}
            result = Player.objects.filter(leage=contry, be_from=scroll).order_by('ranking')
            data['list'] = json.loads(serializers.serialize('json', result))

            return JsonResponse(data=data, safe=False)

# 球队榜
        elif top == 1:
            scroll = received_body.get('scroll')

            list = ["英超", "西甲", "意甲", "德甲", '法甲', '土超']
            contry = list[contry]

            items = [
                 '进球', '控球率', '黄牌', '红牌', '犯规', '被犯规',
                '点球', '射门', '射正', '击中门框', '越位',
                '传球', '成功传球', '关键传球', '争顶总数','抢断',
                '成功直塞','抢断成功', '解围','防线最后一人完成抢断',
                '扑救','扑出点球',"失球","零封","领先情况下丢分",'落后情况得分',
                '禁区内进球','禁区外进球','直接任意球进球',"头球进球","尝试过人",
                '成功过人','被过','丢失球权',"角球",'助攻','传中','成功传中','长传',
                '成功长传','成功直塞', '拦截', "抢回球权",'乌龙球','送点球','传球成功率',
                '禁区内失球','禁区外失球','失误导致丢球','直接任意球进球','运动战进球',
                '快攻进球','单刀球','禁区内射门','禁区外射门','右脚射门','左脚射门',
                '封堵传球','造点球','创造进球机会','拦截成功'
            ]

            scroll = items[scroll]

            data = {}
            result = Team.objects.filter(leage=contry, be_from=scroll).order_by('ranking')
            data['list'] = json.loads(serializers.serialize('json', result))

            return JsonResponse(data=data, safe=False)

# 比赛安排
        elif top == 0:
            scroll = received_body.get('scroll')

            list = ["英超", "西甲", "意甲", "德甲", '法甲']
            contry = list[contry]

            data = {}
            result = GameMatch.objects.filter(url=contry).order_by('start_time')
            data['list'] = json.loads(serializers.serialize('json', result))

            return JsonResponse(data=data, safe=False)