import  requests
import  json
import  pymysql
import  datetime
import csv

class nur_vidio():

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

    def vidio(self,page):
        self.page = page
        url = 'http://api.nur.cn/index.php?m=ver4&' \
          'phone=1|0|Meizu|720|cmcc&access_token=&' \
          'jid=190e35f7e0d9e82b222&ver=1&a=' \
          'video_list_910&catid=9&page={}'.format(self.page)

        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }

        response = requests.get(headers=headers, url=url)
        response.encoding = 'utf-8'
        return response.text

    def get_data(self,int):

        for i in range(int):
            html = nur_vidio.vidio(self,page=i)

            datas = json.loads(html).get('list')
            for data in datas:
                item = {}
                item['id'] = data.get('id')
                item['title'] = data.get('title')
                item['thumb'] = data.get('thumb')
                item['mp4'] = data.get('mp4')
                item['pub_time'] = datetime.datetime.now()
                item['avatar'] = 'https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXEgVS72kWucKk8XibicQlspRySDMWicCBfibgEbYQHpHbicVOjp7vlXIib0AxPicJ65gstwThJkEibgRTTQ/132'
                item['nickname'] = 'توپ بىلگە'

                id = item.get('mp4')
                if nur_vidio.virdect(self,id=id):
                    nur_vidio.save_url(self,id)
                    nur_vidio.save_vidio(self,item=item)

# 保存id
    def save_url(self,id):
        list = []
        with open('id.csv', 'a', encoding='utf-8', newline='') as fp:
            list.append(id)
            writer = csv.writer(fp)
            writer.writerow(list)

# 判断id
    def virdect(self,id):
        with open('id.csv', mode='r', encoding='cp936') as fp:
            data = fp.read()
            if id in data:
                return False
            else:
                return  True


    def save_vidio(self,item):
        SQL = """
                    INSERT INTO nur_vidio (id, title, thumb, mp4, pub_time, avatar, nickname)
                    values (%s,%s,%s,%s,%s,%s,%s)
                """

        self.cursur.execute(SQL, (item['id'], item['title'], item['thumb'], item['mp4'],item['pub_time'], item['avatar'],item['nickname']))
        self.conn.commit()
        print('Insert success for nur_index')

dic = nur_vidio().get_data(1000)



