import  requests
import  json
import  pymysql
import  datetime
import csv

class dongqiudi_vidio():

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

    def vidio(self,url):
        self.url = url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }

        response = requests.get(headers=headers, url=self.url)
        response.encoding = 'utf-8'
        return response.text

    def get_data(self,url):
            html = dongqiudi_vidio.vidio(self,url=url)
            next_url = json.loads(html).get('next')
            print(next_url)
            datas = json.loads(html).get('articles')
            for data in datas:
                item = {}
                item['id'] = data.get('id')
                item['title'] = data.get('title')
                item['thumb'] = data.get('thumb')
                item['mp4'] = data.get('video_info')['video_src']
                item['pub_time'] = data.get('published_at')
                item['avatar'] = 'https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXEgVS72kWucKk8XibicQlspRySDMWicCBfibgEbYQHpHbicVOjp7vlXIib0AxPicJ65gstwThJkEibgRTTQ/132'
                item['nickname'] = 'توپ بىلگە'
                id = str(item['id'])
                if dongqiudi_vidio.virdect(self,id=id):
                    print(item)
                    # dongqiudi_vidio.save_vidio(self,item=item)
                    # dongqiudi_vidio.save_url(self, id=id)

            dongqiudi_vidio.get_data(self,url=next_url)

# 保存id
    def save_url(self,id):
        list = []
        with open('dongqiudi.csv', 'a', encoding='utf-8', newline='') as fp:
            list.append(id)
            writer = csv.writer(fp)
            writer.writerow(list)

# 判断id
    def virdect(self,id):
        with open('dongqiudi.csv', mode='r', encoding='cp936') as fp:
            data = fp.read()
            if id in data:
                return False
            else:
                return  True


    def save_vidio(self,item):
        SQL = """
                    INSERT INTO dongqiudi_vidio (id, title, thumb, mp4, pub_time, avatar, nickname)
                    values (%s,%s,%s,%s,%s,%s,%s)
                """

        self.cursur.execute(SQL, (item['id'], item['title'], item['thumb'], item['mp4'],item['pub_time'], item['avatar'],item['nickname']))
        self.conn.commit()
        print('Insert success for nur_index')


if __name__ == '__main__':
    url = 'https://api.dongqiudi.com/v3/archive/app/tabs/getlists?id=100043&platform=android&version=220'
    dic = dongqiudi_vidio().get_data(url=url)



