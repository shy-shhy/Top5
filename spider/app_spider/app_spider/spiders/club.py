# -*- coding: utf-8 -*-
import scrapy
import json
from app_spider.thridparty.xiaoniuy import Translate
from app_spider.thridparty.dicts import Team_dict
import time
from app_spider.items import clubItem


class ClubSpider(scrapy.Spider,Translate):
    name = "club"
    allowed_domains = ["dongqiudi.com"]
    start_urls = [
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/team?season_id=14931&app=dqd&version=214&platform=android&type=team',
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/team?season_id=15013&app=dqd&version=214&platform=android&type=team',
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/team?season_id=15385&app=dqd&version=214&platform=android&type=team',
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/team?season_id=15014&app=dqd&version=214&platform=android&type=team',
        'https://sport-data.dongqiudi.com/soccer/biz/data/ranking/team?season_id=15045&app=dqd&version=214&platform=android&type=team',

    ]

    def parse(self, response):
        datas = json.loads(response.text).get('content')['data']
        for data in datas:
            item = {}
            url = data.get('url')
            print(url)
            item['be_from'] = data.get('name')
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})

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
            img = data.get('team_logo')

            team = Team_dict.team_dict(data.get('team_name'))
            if team:
                team = team
            else:
                team = Translate.xiaoniu_uy(self,value=data.get('team_name'))

            count = data.get('count')
            # time.sleep(1)

            item = clubItem(
              leage= url,
              be_from=be_from,
              rank=rank,
              img=img,
              team=team,
              count= count
            )

            yield item
            # print(item)