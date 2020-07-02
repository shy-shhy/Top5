# -*- coding: utf-8 -*-
import scrapy
import  json
from app_spider.items import  SchedulerSpiderItem
from app_spider.thridparty.dicts import  Team_dict
from app_spider.thridparty.xiaoniuy import Translate
from app_spider.thridparty.time_format import time_format
import  time as t


class SchedulerSpider(scrapy.Spider,Translate):
    name = "scheduler"
    allowed_domains = ["dongqiudi.com"]

    def start_requests(self):
        yield scrapy.Request(
            'https://api.dongqiudi.com/data/tab/new/important?version=214&start=2020-05-1016%3A00%3A00&init=1',
            headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"})


    def parse(self, response):
        dict_res =  json.loads(response.text)
        URL = response.request.url
        lists = dict_res.get("list")

        count = []
        for list in lists:
            item = SchedulerSpiderItem()

            item['url'] = URL
            team_A_name = Team_dict.team_dict(list["team_A_name"])
            if team_A_name:
                item['team_A_name'] = team_A_name
            else:
                item['team_A_name']= list.get('team_A_name')

            item["team_A_logo"] = list.get("team_A_logo")

            team_B_name = Team_dict.team_dict(list["team_B_name"])
            if team_A_name:
                item['team_B_name'] = team_B_name
            else:
                item['team_B_name'] = list.get('team_B_name')


            item["team_B_logo"] = list.get("team_B_logo")

            time = list.get("date_utc")
            if time in count:
                item['well_time'] = ""
            else:
                count.append(time)
                item['well_time'] = list.get('date_utc')

            item["date_utc"] = list.get("date_utc")


            item["start_time"] = time_format(list.get('time_utc'))

            match_title = list.get("match_title")
            if match_title is None:
                match_title = ""
            if "经典回顾" in match_title:
                item['match_title'] = Team_dict.team_dict("经典回顾")
            elif "英雄联盟" in match_title:
                item['match_title'] = Team_dict.team_dict('英雄联盟')
            elif 'KPL' in match_title:
                item['match_title'] = Team_dict.team_dict('KPL')
            elif 'K联赛' in match_title:
                item['match_title'] = Team_dict.team_dict('k联赛')
            elif '友谊赛' in match_title:
                item['match_title'] = Team_dict.team_dict('友谊赛')
            elif "足球电竞职业联赛" in match_title:
                item['match_title'] = Team_dict.team_dict('足球电竞职业联赛')
            else:
                item['match_title'] = Translate.xiaoniu_uy(self,match_title)



            TVList = Team_dict.team_dict(list.get("TVList"))
            if TVList:
                item['TVList'] =TVList

            else:
                if '懂球帝PP小程序' in list.get('TVList'):
                    item['TVList'] = Team_dict.team_dict('懂球帝PP小程序')
                else:
                    item['TVList'] = list.get("TVList")


            item["fs_A"] = list.get("fs_A")

            item["fs_B"] = list.get("fs_B")
            t.sleep(1)


            print(item)
            # yield  item