import  requests
import  json
import  pymysql
import  datetime
import csv

dbparams = {
    'host': '39.100.245.203',
    'port': 3306,
    'user': "root",
    'password': "asus123836.",
    'database': "scrapy",
    'charset': 'utf8mb4'
}
conn = pymysql.connect(**dbparams)
cursur = conn.cursor()
fin = open('Top_1.jpg','rb')
img = fin.read()
fin.close()

sql = "INSERT INTO images VALUES (%s,%s);"
args = ('Top_1',img)
cursur.execute(sql,args)
conn.commit()
cursur.close()
conn.close()


# cursor = conn.cursor()
# cursor.execute("SELECT img FROM images LIMIT 1")
# fout = open('test_new.jpg', 'wb')
# fout.write(cursor.fetchone()[0])
# fout.close()
# cursor.close()
# conn.close()



