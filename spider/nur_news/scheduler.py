import  requests,json,pymysql
from thridparty.dicts import Team_dict
from thridparty.xiaoniuy import Translate
from thridparty.time_format import time_format
from thridparty.game_match import Game_match
import datetime
import hashlib
import csv

class scheduler():
    def __init__(self):
        dbparams = {
            'host': '39.100.245.203',
            'port': 3306,
            'user': "root",
            'password': "asus123836.",
            'database': "scrapy_copy",
            'charset': 'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursur = self.conn.cursor()

    def req(self,start_time):
        url = 'https://api.dongqiudi.com/data/tab/new/' \
              'important?version=214&start={}' \
              '%3A00%3A00&init=1'.format(start_time)

        # print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }

        response = requests.get(headers=headers, url=url)
        response.encoding = 'utf-8'
        return response.text


    def get_data(self,start_time):
            dic = []
            html = scheduler.req(self,start_time=start_time)
            datas = json.loads(html).get('list')
            nextDate = json.loads(html).get('nextDate')

            for data in datas:
                item = {}

                start_play = data.get('start_play')             #开始时间
                time = datetime.datetime.strptime(start_play, "%Y-%m-%d %H:%M:%S")
                out_date = (time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                item['start_play'] = out_date
                item['round_name'] = data.get('round_name')             #比赛类型

                team_A_name = data.get('team_A_name')
                if Team_dict.team_dict(team_A_name):
                    item['team_A_name'] = Team_dict.team_dict(team_A_name)
                else:
                    item['team_A_name'] = Translate.xiaoniu_uy(self,team_A_name)
                item['team_A_logo'] = data.get('team_A_logo')

                team_B_name = data.get('team_B_name')
                if Team_dict.team_dict(team_B_name):
                    item['team_B_name'] = Team_dict.team_dict(team_B_name)
                else:
                    item['team_B_name'] = Translate.xiaoniu_uy(self, team_B_name)
                item['team_B_logo'] = data.get('team_B_logo')

                item['fs_A'] = data.get('fs_A')
                item['fs_B'] = data.get('fs_B')


                item['match_title'] = Game_match().game_match(data.get('match_title'))           #比赛标题

                if item['round_name']:
                    date_utc = item['start_play'].split(' ')[0]

                    if date_utc in dic:
                        item['date_utc'] = ''
                    else:
                        dic.append(date_utc)
                        item['date_utc'] = date_utc  # 年-月-日

                    item['time_utc'] = time_format(data.get('time_utc')) #比赛时间

                    hash = str(item['start_play']).strip('')+ item['team_A_logo']

                    if scheduler().virdect(id=hash):
                        scheduler().save_url(id=hash)
                        scheduler.save_vidio(self,item=item)
                        print(item)
            if nextDate:
                nextDate = nextDate.split(' ')[0] + " 00"
                dic = scheduler().get_data(nextDate)
#保存MD5
    def save_url(self, id):
        list = []
        with open('schedule.csv', 'a', encoding='utf-8', newline='') as fp:
            list.append(id)
            writer = csv.writer(fp)
            writer.writerow(list)

#判断MD5
    def virdect(self, id):
        with open('schedule.csv', mode='r', encoding='utf-8') as fp:
            data = fp.read()
            if id in data:
                return False
            else:
                return True

    def save_vidio(self,item):
        SQL = """
                    INSERT INTO schedule (start_paly, round_name, team_A_name,
                     team_A_logo, team_B_name, team_B_logo, fs_A,
                    fs_B,match_title,date_utc,time_utc)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

        self.cursur.execute(SQL, (item['start_play'], item['round_name'], item['team_A_name'],
                                  item['team_A_logo'],item['team_B_name'], item['team_B_logo'],item['fs_A'],
                                  item['fs_B'], item['match_title'], item['date_utc'],item['time_utc']))
        self.conn.commit()
        print('Insert success for scheduler')

def main():
    pub_time = "2020-05-10 00"
    dic = scheduler().get_data(pub_time)

if __name__ == '__main__':
    main()