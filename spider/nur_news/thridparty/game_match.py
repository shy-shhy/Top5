import  re
from thridparty.dicts import  Team_dict
from thridparty.xiaoniuy import Translate

class Game_match():
    def __init__(self):
        pass

    def game_match(self,value):
        try:
            value_1 = value.split(' ')[0]
            value_2 = value.split(' ')[1]
            if Team_dict.team_dict(value_1) and '轮' in value_2:
                integer = re.findall(r"\d+", value)[0]
                i = "ئايلانما"
                font = Team_dict.team_dict(value_1)
                return '{}{}-{}'.format(font, integer, i)
            elif  '经典回顾' in value:
                return 'كىلاسسىك مۇسابىقىلەر'
            elif '东亚杯' in value:
                return 'شەرقى ئاسىيا لوڭقىسى'
            elif '意杯' in value:
                return 'ئىتالىيە لوڭقىسى'
            elif '美洲杯' in value:
                return  'ئامىرىكا قىتئەسى لوڭقىسى'
            elif '足总杯' in value:
                return 'پۇتبول ئومۇمىي لوڭقىسى مۇسابىقىسى '
            else:
                return Translate().xiaoniu_uy(value)
                # return value
        except:
            return Translate().xiaoniu_uy(value)
            # return value

if __name__ == '__main__':
     value = 'K联赛第26轮'
     dic = Game_match().game_match(value=value)
     print(dic)
