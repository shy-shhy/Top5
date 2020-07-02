import json
from  urllib.parse import  urlencode
import  requests

class Translate():
    def __init__(self):
        pass

    def xiaoniu_uy(self,value):
        url = 'https://api.niutrans.vip/NiuTransServer/translation?'

        data = {
            'from': 'zh',
            'src_text': value,
            'to': 'uy',
            'apikey': '514b68838cc5684f24c265d93a443246'
        }

        base_url = url + urlencode(data)
        res = requests.get(base_url)
        result = json.loads(res.text).get('tgt_text')

        print(result)
        # return result



if __name__ == '__main__':

    b = Translate()
    b.xiaoniu_uy('JDG')

