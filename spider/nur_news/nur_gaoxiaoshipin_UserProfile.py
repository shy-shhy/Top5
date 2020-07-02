import  requests,json,pymysql,datetime,csv,re,hashlib


class Nur_UserProfile():

#初始化数据库
    def __init__(self):
        dbparams = {
            'host': '139.199.221.197',
            'port': 3306,
            'user': "devlelop",
            'password': "LrzazAkDDKJLKGtH",
            'database': "devlelop",
            'charset': 'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursur = self.conn.cursor()

    def shipin(self,page):
        self.page = page
        url = 'http://api.nur.cn/index.php?m=ver4&phone=' \
              '1|0|Meizu|720|cmcc&access_token=' \
              '1179e0c3VgUIB1UAVgEHBFFSXFoJD10LAVYMCwEABlABA1EGXgdRaltvFncEdVIEAAUc1c1c1c1&jid=' \
              '190e35f7e0d9e82b222&ver=1&a=circle_list_910&catid=1&page={}'.format(self.page)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }

        response = requests.get(headers=headers, url=url)
        response.encoding = 'utf-8'
        return response.text

    def get_data(self,int):
        for i in range(int):
            html = Nur_UserProfile.shipin(self,page=i)
            print(i)
            datas = json.loads(html).get('list')
            for dic in datas:
                for data in dic['likes_list']:
                    item = {}
                    item['name'] = data['name']
                    item['face'] = data['face']
                    item['sex']  = data['sex']
                    # print(item)

                    if Nur_UserProfile.virdect(self, id=item['name']):
                        Nur_UserProfile.save_url(self, item['name'])
                        Nur_UserProfile.save_data(self, item)


# 保存id
    def save_url(self,id):
        list = []
        with open('nur_user.csv', 'a', encoding='utf-8', newline='') as fp:
            list.append(id)
            writer = csv.writer(fp)
            writer.writerow(list)

# 判断id
    def virdect(self,id):
        with open('nur_user.csv', mode='r', encoding='utf-8') as fp:
            data = fp.read()
            if id in data:
                return False
            else:
                return  True

    def save_data(self,item):
        SQL = """
                    INSERT INTO randomUserInfo(name,avatar,sex)
                    values (%s,%s,%s)
                """

        self.cursur.execute(SQL, (item['name'], item['face'],item['sex']))
        self.conn.commit()
        print('Insert success for nur_user')

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

if __name__ == '__main__':
    Nur_UserProfile().get_data(10000)