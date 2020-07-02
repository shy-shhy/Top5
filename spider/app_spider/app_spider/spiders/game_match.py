# -*- coding: utf-8 -*-
import scrapy
import  json
from app_spider.items import game_matchItem
from app_spider.thridparty.dicts import Team_dict
from app_spider.thridparty.xiaoniuy import Translate

class GameMatchSpider(scrapy.Spider):
    name = "game_match"
    allowed_domains = ["dongqiudi.com"]
    start_urls = [
        'https://sport-data.dongqiudi.com/soccer/biz/data/schedule?season_id=14931&app=dqd&version=214&platform=android',#英超
        'https://sport-data.dongqiudi.com/soccer/biz/data/schedule?season_id=15013&app=dqd&version=214&platform=android',#西甲
        'https://sport-data.dongqiudi.com/soccer/biz/data/schedule?season_id=15385&app=dqd&version=214&platform=android',#意甲
        'https://sport-data.dongqiudi.com/soccer/biz/data/schedule?season_id=15014&app=dqd&version=214&platform=android',#德甲
        'https://sport-data.dongqiudi.com/soccer/biz/data/schedule?season_id=15045&app=dqd&version=214&platform=android' #法甲
    ]

    def parse(self, response):
        datas = json.loads(response.text).get('content')['matches']
        for data in datas:
            url = response.request.url
            if '14931' in url:
                url = '英超'
            elif '15013' in url:
                url = '西甲'
            elif '15385' in url:
                url = '意甲'
            elif '15014' in url:
                url = '德甲'
            elif '15045' in url:
                url = '法甲'

            team_a = Team_dict.team_dict(data.get('team_A_name'))
            if team_a:
                team_a = team_a
            else:
                team_a = Translate.xiaoniu_uy(data.get('team_A_name'))


            team_a_logo = data.get('team_A_logo')

            team_b = Team_dict.team_dict(data.get('team_B_name'))
            if team_b:
                team_b = team_b
            else:
                team_b = Translate.xiaoniu_uy(data.get('team_B_name'))


            team_b_logo = data.get('team_B_logo')
            start_time = data.get('start_play')

            item = game_matchItem(
            url = url,
             team_a=team_a,
             team_a_logo=team_a_logo,
             team_b=team_b,
             team_b_logo=team_b_logo,
             start_time= start_time
            )
            # print(item)
            yield item