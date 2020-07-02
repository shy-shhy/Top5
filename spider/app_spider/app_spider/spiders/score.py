# -*- coding: utf-8 -*-
import scrapy
import  json
from app_spider.items import  scoreItem
from app_spider.thridparty.xiaoniu_en import Translate
from app_spider.thridparty import  dicts



class ScoreSpider(scrapy.Spider,Translate):
    name = "score"
    allowed_domains = ["dongqiudi.com"]
    start_urls = [
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=14931&app=dqd&version=214&platform=android', #英超
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15013&app=dqd&version=214&platform=android', #西甲
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15385&app=dqd&version=214&platform=android', #意甲
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15014&app=dqd&version=214&platform=android', #德甲
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15045&app=dqd&version=214&platform=android', #法甲
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15854&app=dqd&version=214&platform=android', #韩国
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=16093&app=dqd&version=214&platform=android', #中超
            'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15047&app=dqd&version=214&platform=android'  #土耳其
    ]

    def parse(self, response):
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
        elif '15854' in url:
            url = 'K联赛'
        elif '16093' in url:
            url = '中超'
        elif '15047' in url:
            url = '土超'


        dic = json.loads(response.text)

        datas = dic['content'].get('rounds')[0]['content']['data']
        for data in datas:
            rank = data.get('rank')
            logo = data.get('team_logo')

            team_name = data.get('team_name')
            name = dicts.Team_dict.team_dict(team_name)
            if name:
                team_name = name
            else:
                # team_name = Translate.xiaoniu_english(self,value=team_name)
                team_name = data.get('team_name')


            matches = data.get('matches_total')
            matches_won = data.get('matches_won')
            matches_drew = data.get('matches_draw')
            matches_lost = data.get('matches_lost')
            goal = data.get('goals_pro')+'/'+data.get('goals_against')
            score = data.get('points')

            item = scoreItem(
                rank= rank,
                logo= logo,
                team_name= team_name,
                matches= matches,
                matches_won= matches_won,
                matches_drew=matches_drew,
                matches_lost=matches_lost,
                goal= goal,
                score = score,
                leage= url
            )

            yield  item
            # print(item)

