# -*- coding: utf-8 -*-
import pymysql
from app_spider.items import  scoreItem
from app_spider.items import  playerItem,clubItem,game_matchItem,SchedulerSpiderItem


class AppSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '39.100.245.203',
            'port': 3306,
            'user': "root",
            'password': "asus123836.",
            'database': "scrapy_copy",
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        if isinstance(item,scoreItem):
            SQL = """
                INSERT INTO score (leage, ranking, team_name, matches_won, matches_drew, matches_win, matches, score, logo, goal)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            self.cursor.execute(SQL,(item['leage'],item['rank'], item['team_name'], item['matches_lost'],
                                     item['matches_drew'], item['matches_won'], item['matches'],
                                     item['score'], item['logo'], item['goal']
                                    ))

            self.conn.commit()
            return item


        elif isinstance(item,playerItem):
            SQL = """
                INSERT INTO player (leage, be_from, ranking, img, name, team, count)
                values (%s,%s,%s,%s,%s,%s,%s)
            """
            self.cursor.execute(SQL,(item['leage'], item['be_from'], item['rank'],
                                     item['img'], item['name'], item['team'],
                                     item['count']
                                     ))
            self.conn.commit()
            return  item




        elif isinstance(item,clubItem):
            SQL = """
                           INSERT INTO team (leage, be_from,team, ranking, img, count)
                           values (%s,%s,%s,%s,%s,%s)
                       """
            self.cursor.execute(SQL, (item['leage'], item['be_from'], item['team'],
                                      item['rank'], item['img'], item['count']
                                      ))
            self.conn.commit()
            return item


        elif isinstance(item,game_matchItem):
            SQL = """
                           INSERT INTO game_match (url, team_a,team_a_logo, team_b, team_b_logo, start_time)
                           values (%s,%s,%s,%s,%s,%s)
                       """
            self.cursor.execute(SQL, (item['url'], item['team_a'], item['team_a_logo'],
                                      item['team_b'], item['team_b_logo'], item['start_time']
                                      ))
            self.conn.commit()
            return item

#比赛安排
        elif isinstance(item,SchedulerSpiderItem):
            sql = """
                        insert into schedule (date_utc, start_time, team_A_name, team_A_logo, fs_A, fs_B, TVList, match_title, team_B_name, team_B_logo,well_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       """

            self.cursor.execute(sql, (
            item["date_utc"], item["start_time"], item["team_A_name"], item["team_A_logo"], item["fs_A"],
            item["fs_B"], item["TVList"], item["match_title"], item["team_B_name"], item["team_B_logo"],
            item['well_time'])
                                 )

            self.conn.commit()




    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()