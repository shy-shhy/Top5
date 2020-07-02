# -*- coding: utf-8 -*-
import scrapy
import json


class Player1Spider(scrapy.Spider):
    name = "player_1"
    allowed_domains = ["dongqiudi.com"]
    start_urls = [
        'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=16093&app=dqd&version=214&platform=android' #中超
        'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15854&app=dqd&version=214&platform=android' #韩国
        'https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=15047&app=dqd&version=214&platform=android' #土耳其
    ]

    def parse(self, response):
        datas = json.loads(response.text).get('content')['rounds'][0]['content']['data']
        for data in datas:
            url = response.request.url
            if '16093' in url:
                url = '中超'
            elif '15854' in url:
                url = '韩国'
            elif '15047' in url:
                url = '土耳其'


            rank = data.get('rank')
            img = data.get('person_logo')

            name = data.get('person_name')
            name = xiaoniu_en.Translate.xiaoniu_english(self, value=name)

            team = data.get('team_name')
            team = dicts.Team_dict.team_dict(team)
            if team:
                team = team
            else:
                team = Translate(self, value=team)

            count = data.get('count')
            time.sleep(1)

            item = playerItem(
                leage=url,
                be_from=be_from,
                rank=rank,
                img=img,
                name=name,
                team=team,
                count=count
            )

            yield item
            print(item)
