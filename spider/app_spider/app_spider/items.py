# -*- coding: utf-8 -*-



import scrapy


class scoreItem(scrapy.Item):
    rank = scrapy.Field()
    logo = scrapy.Field()
    team_name = scrapy.Field()
    matches = scrapy.Field()
    matches_won = scrapy.Field()
    matches_drew = scrapy.Field()
    matches_lost = scrapy.Field()
    goal = scrapy.Field()
    score = scrapy.Field()
    leage = scrapy.Field()

class playerItem(scrapy.Item):
    leage = scrapy.Field()
    be_from = scrapy.Field()
    rank = scrapy.Field()
    img = scrapy.Field()
    name = scrapy.Field()
    team = scrapy.Field()
    count = scrapy.Field()

class clubItem(scrapy.Item):
    leage= scrapy.Field()
    be_from= scrapy.Field()
    rank= scrapy.Field()
    img= scrapy.Field()
    team= scrapy.Field()
    count= scrapy.Field()

class game_matchItem(scrapy.Item):
    url = scrapy.Field()
    team_a =scrapy.Field()
    team_a_logo =scrapy.Field()
    team_b =scrapy.Field()
    team_b_logo =scrapy.Field()
    start_time =scrapy.Field()

class SchedulerSpiderItem(scrapy.Item):
    url= scrapy.Field()
    date_utc = scrapy.Field()
    start_time = scrapy.Field()
    team_A_name = scrapy.Field()
    team_A_logo = scrapy.Field()
    fs_A = scrapy.Field()
    fs_B = scrapy.Field()
    TVList = scrapy.Field()
    match_title = scrapy.Field()
    team_B_name = scrapy.Field()
    team_B_logo = scrapy.Field()
    well_time= scrapy.Field()
