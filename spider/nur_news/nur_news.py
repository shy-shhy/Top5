from selenium import  webdriver
from selenium.webdriver.chrome.options import Options
import  time,datetime
import pymysql
from lxml import  etree
import re
import  csv

class Index():

#初始化数据库
    def __init__(self):
        dbparams = {
            'host': '39.100.245.203',
            'port': 3306,
            'user': "root",
            'password': "asus123836.",
            'database': "scrapy",
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursur = self.conn.cursor()


#获取首页的数据
    def get_url(self):
        # 创建chrome浏览器驱动，无头模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(r"chromedriver.exe", chrome_options=chrome_options)
        driver.get("https://www.nur.cn/lists/16/1.shtml")

        js = "return action=document.body.scrollHeight"
        height = driver.execute_script(js)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        base = 'https://www.nur.cn'

        t1 = int(time.time())
        count = 0
        # and count < 1000

        while True:
            count += 1
            t2 = int(time.time())
            if t2-t1 <30 and count < 200:
                new_height = driver.execute_script(js)
                if new_height > height:
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

                    height = new_height
                    t1 = int(time.time())
            else:

                page = driver.page_source
                html = etree.HTML(page)

                paths = html.xpath('.//div[@class="tempWrap"]/ul/li')

                dic = {}
                for path in paths:
                    dic['img'] = path.xpath('./a/img/@src')[0]
                    dic['title'] = path.xpath('.//p/text()')[0]
                    dic['url']=base + path.xpath('./a/@href')[0]
                    self.save_head(dic)


                paths = html.xpath("//div[@class='view']/ul/li")
                for path in paths:
                    url = path.xpath('./a/@href')[0]
                    base_url = base + url
# 判断URL
    # 保存RUL
                    if self.virdect(base_url):
                        self.save_url(base_url)
                        item = {}

                        Uid = base_url
                        title = path.xpath('./a/h4/text()')[0]
                        try:
                            img = path.xpath('./a/img/@src')[0]
                            pub_time = path.xpath('./a/div/span[2]/text()')[0]
                        except:
                            img = path.xpath('./a/div[1]/img[1]/@src')[0]
                            pub_time = path.xpath('./a/div[2]/span[2]/text()')[0]

#时间格式
                        pub_time = self.time_format(pub_time)

                        item['Uid'] = Uid
                        item['pub_time'] = pub_time
                        item['img'] = img
                        item['title'] = title
#保存数据
                        self.detaiel(base_url)

                        self.save_index(item)
#详情页
#保存URL
                        self.save_url(base_url)

                print('到达最底部了')
                driver.close()
                break


#判断URL
    def virdect(self,base_url):
        with open('url.csv', mode='r', encoding='utf-8') as fp:
            data = fp.read()
            if base_url in data:
                return False
            else:
                return True

#保存URL
    def save_url(self,base_url):
        list = []
        with open('url.csv', 'a', encoding='utf-8', newline='') as fp:
            list.append(base_url)
            writer = csv.writer(fp)
            writer.writerow(list)

#时间转化
    def time_format(self,pub_time):
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
            pub_time = int(pub_time[0])*7
            pub_time = (now_time + datetime.timedelta(days=-pub_time)).strftime("%Y-%m-%d %H:%M:%S")

        else:
            pub_time = re.findall(r"\d+", pub_time)
            pub_time = int(pub_time[0]) * 30
            pub_time = (now_time + datetime.timedelta(days=-pub_time)).strftime("%Y-%m-%d %H:%M:%S")

        return pub_time


#保存首页数据
    def save_index(self,item):
        SQL = """
                    INSERT INTO nur_index (uid, title, image, pub_time)
                    values (%s,%s,%s,%s)
                """

        self.cursur.execute(SQL, (item['Uid'], item['title'], item['img'], item['pub_time']))
        self.conn.commit()
        print('Insert success for nur_index')

    def detaiel(self,url):
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                driver = webdriver.Chrome(r"D:/chromedriver.exe",chrome_options=chrome_options)

                driver.get(url)
                html = driver.page_source

                driver.close()
                html = etree.HTML(html)

                item = {}

                item['url'] = url
                item['title'] = html.xpath("//div[@class='view-center']/div/h2/text()")[0]
                item['resource'] = html.xpath("//div[@class='view-center']/div/div/span[1]/i/text()")[0]
                item['pub_time'] = html.xpath("//div[@class='view-center']/div/div/span[2]/i/text()")[0]
                spans = html.xpath("//div[@class='view-bottom']/div/span")
                paths = html.xpath("//div[@class='view_p mazmun']/p")

                item['p'] = len(paths)
                item['span'] = len(spans)

                list = ['a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's','u','t','v','w','x','y','z']

                for i in range(len(list)):
                    try:
                        item[i] = paths[i].xpath(".//img/@src")[0]
                    except:
                        try:
                            item[i] = paths[i].xpath("./text()")[0].strip().replace('/', '')
                        except:
                            try:
                                item[i] = paths[i].xpath('.//span/text()')
                                item[i] = ''.join(item[i])
                            except:
                                try:
                                    item[i]= paths[i].xpath('.//iframe/@scr')
                                except:
                                    try:
                                        item[i]=' '
                                    except:
                                        return

                list = ['a', 'b', 'c', 'd', 'e']
                count = -1
                for i in list:
                    count += 1
                    try:
                        item[i] = spans[count].xpath('./a/text()')[0]
                    except:
                        item[i] = ' '

                self.save_detail(item)

#保存详情页数据
    def save_detail(self,item):
        SQL = """
                        INSERT INTO nur_news(url,p_0,p_1,p_2,p_3,p_4,p_5,p_6,p_7,p_8,p_9,p_10,p_11,p_12,p_13,p_14,p_15,p_16,p_17,p_18,p_19,p_20,p_21,p_22,p_23,p_24,p_25,title,root,pub_time,a,b,c,d,e,p,span) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                              """

        line = self.cursur.execute(SQL, (item['url'],
                                         item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],
                                         item[8], item[9], item[10],
                                         item[11],
                                         item[12], item[13], item[14], item[15], item[16], item[17], item[18], item[19],
                                         item[20], item[21],
                                         item[22],
                                         item[23], item[24], item[25], item['title'], item['resource'],
                                         item['pub_time'], item['a'], item['b'],
                                         item['c'], item['d'], item['e'], item['p'], item['span']))

        self.conn.commit()
        print('Insert success for nur_news')

#轮播图
    def save_head(self,dic):
        SQL = """
            INSERT INTO nur_slide_show(img,text,url) values (%s,%s,%s)
        """
        self.cursur.execute(SQL,(dic['img'],dic['title'],dic['url']))
        self.conn.commit()
        print('Insert success for slide_show')


while True:
    start_time = datetime.datetime.now()

    log = str(start_time) + '  开始运行'
    print(log)
    list = []
    with open('csv.nur_LOG.csv', 'a', encoding='utf-8', newline='') as fp:
        list.append(log)
        writer = csv.writer(fp)
        writer.writerow(list)

    def main():
        b = Index()
        b.get_url()


    if __name__ == '__main__':
        main()


    end_time = datetime.datetime.now()

    log = str(end_time) + ' 结束运行'
    list = []
    with open('csv.nur_LOG.csv', 'a', encoding='utf-8', newline='') as fp:
        list.append(log)
        writer = csv.writer(fp)
        writer.writerow(list)


    time.sleep(1800)



























