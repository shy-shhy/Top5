import  requests,json,pymysql,datetime,csv,re,hashlib


class Nur_gaoxiaoShiPin():

#初始化数据库
    def __init__(self):
        dbparams = {
            'host': '39.100.245.203',
            'port': 3306,
            'user': "root",
            'password': "asus123836.",
            'database': "scrapy",
            'charset': 'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursur = self.conn.cursor()

    def shipin(self,page):
        self.page = page
        url = 'http://api.nur.cn/index.php?m=ver4&phone=1|0|Meizu|720|cmcc&access_token=' \
              '1179e0c3VgUIB1UAVgEHBFFSXFoJD10LAVYMCwEABlABA1EGXgdRaltvFncEdVIEAAUc1c1c1c1&jid=' \
              '190e35f7e0d9e82b222&ver=1&a=video_list_910&catid=3&page={}'.format(self.page)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }

        response = requests.get(headers=headers, url=url)
        response.encoding = 'utf-8'
        return response.text

    def get_data(self,int):
        for i in range(int):
            html = Nur_gaoxiaoShiPin.shipin(self,page=i)
            datas = json.loads(html).get('list')
            for data in datas:
                item = {}

                item['url'] = data.get('mp4')
                item['title'] = data.get('title')
                thumb = data.get('thumb')
                if thumb:
                    item['thumb'] = thumb[0]
                else:
                    item['thumb'] = ''
                item['pub_time'] = Nur_gaoxiaoShiPin.time_format(self,data.get('update_time'))
                item['likes_total'] = data.get('hand')

                if Nur_gaoxiaoShiPin.virdect(self,id=item['url']):
                    print(item)
                    Nur_gaoxiaoShiPin.save_data(self,item=item)
                    Nur_gaoxiaoShiPin.save_url(self, id=item['url'])
                    print(item)

# 保存id
    def save_url(self,id):
        list = []
        with open('nur_gaoxiaoshipin.csv', 'a', encoding='utf-8', newline='') as fp:
            list.append(id)
            writer = csv.writer(fp)
            writer.writerow(list)

# 判断id
    def virdect(self,id):
        with open('nur_gaoxiaoshipin.csv', mode='r', encoding='cp936') as fp:
            data = fp.read()
            if id in data:
                return False
            else:
                return  True


    def save_data(self,item):
        SQL = """
                    INSERT INTO nur_gaoxiaoshipin (url, title, thumb, pub_time, like_total)
                    values (%s,%s,%s,%s,%s)
                """

        self.cursur.execute(SQL, (item['url'], item['title'],item['thumb'], item['pub_time'],
                                  item['likes_total']))
        self.conn.commit()
        print('Insert success for nur_gaoxiaoshipin')


    def time_format(self, pub_time):
        now_time = datetime.datetime.now()
        if pub_time == 'ﺑﺎﻳﺎﺗﯩﻦ':
            pub_time = (now_time + datetime.timedelta(days=+0)).strftime("%Y-%m-%d %H:%M:%S")

        elif 'ﺳﺎﺋﻪﺕ' in pub_time:
            pub_time = re.findall(r"\d+", pub_time)
            pub_time = int(pub_time[0])
            pub_time = (now_time + datetime.timedelta(hours=-pub_time)).strftime("%Y-%m-%d %H:%M:%S")

        elif 'ﻛﯜﻥ' in pub_time:
            pub_time = re.findall(r"\d+", pub_time)
            pub_time = int(pub_time[0])
            pub_time = (now_time + datetime.timedelta(days=-pub_time)).strftime("%Y-%m-%d %H:%M:%S")

        elif 'ﮪﻪﭘﺘﻪ' in pub_time:
            pub_time = re.findall(r"\d+", pub_time)
            pub_time = int(pub_time[0]) * 7
            pub_time = (now_time + datetime.timedelta(days=-pub_time)).strftime("%Y-%m-%d %H:%M:%S")

        else:
            pub_time = re.findall(r"\d+", pub_time)
            pub_time = int(pub_time[0]) * 30
            pub_time = (now_time + datetime.timedelta(days=-pub_time)).strftime("%Y-%m-%d %H:%M:%S")

        return pub_time


dic = Nur_gaoxiaoShiPin().get_data(10)



