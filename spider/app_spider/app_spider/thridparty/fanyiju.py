import requests
import json

def fanyiju(value):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "43",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "218.241.146.90:8888",
        "Origin": "http://www.mzywfy.org.cn",
        "Referer": "http://www.mzywfy.org.cn/mainIndex.jsp"
    }

    pyload ={
    "from": "zh",
    "to": "ww",
    "src_text": value
    }

    url = "http://218.241.146.90:8888/translate/trans"

    r = requests.post(url=url, data=json.dumps(pyload),headers=headers)

    if r.status_code ==200:
        r.encoding = r.apparent_encoding
        res = r.text

        load = json.loads(res)
        data = load.get("responseData")
        value = data.replace("&nbsp;",'').replace("<br/>","")
        print(value)
        return value


    else:
        return "请求失败"


def main():
    value = "皇马"
    fanyiju(value)

if __name__ == '__main__':
    main()

