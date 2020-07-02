# -*- coding: utf-8 -*-
import scrapy
import json
from app_spider.items import playerItem
from app_spider.thridparty.xiaoniuy import Translate
from app_spider.thridparty import dicts
from app_spider.thridparty import  xiaoniu_en
import time


class PlayerSpider(scrapy.Spider,Translate):
    name = "player"
    allowed_domains = ["dongqiudi.com"]
    start_urls = [
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/person?season_id=14931&app=dqd&version=214&platform=android&type=person', #英超
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/person?season_id=15013&app=dqd&version=214&platform=android&type=person'  #西甲
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/person?season_id=15385&app=dqd&version=214&platform=android&type=person'  #意甲
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/person?season_id=15014&app=dqd&version=214&platform=android&type=person'  #德甲
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/person?season_id=15045&app=dqd&version=214&platform=android&type=person'   #法甲

        ]

    def parse(self, response):
        datas = json.loads(response.text).get('content')['data']
        for data in datas:
            item = {}
            url = data.get('url')
            item['be_from'] = data.get('name')
            yield  scrapy.Request(url=url,callback=self.parse_detail,meta={'item':item})


    def parse_detail(self,response):
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
        be_from = response.meta['item']
        be_from = (be_from['be_from'])


        dic = json.loads(response.text)
        datas = dic.get('content')['data']
        for data in datas:
            rank = data.get('rank')
            img = data.get('person_logo')

            name = data.get('person_name')
            name = xiaoniu_en.Translate.xiaoniu_english(self,value=name)


            team = data.get('team_name')
            team = dicts.Team_dict.team_dict(team)
            if team:
                team = team
            else:
                team = Translate(self, value=team)



            count = data.get('count')
            # time.sleep(1)

            item = playerItem(
              leage= url,
              be_from=be_from,
              rank=rank,
              img=img,
              name=name,
              team=team,
              count= count
            )

            yield item
            # print(item)

