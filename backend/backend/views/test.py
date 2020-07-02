import  json
from django.http import HttpResponse,JsonResponse
from backend.models import NurIndex,NurNews,NurSlideShow,\
    Schedule,NewsPriase,Shoucang,ClickNews,Comment,CommentPrice
from django.core import  serializers
from django.db.models import Q
import random
from django.forms.models import model_to_dict
import  datetime

def test(request):
    now_date = datetime.datetime.now()
    result = Schedule.objects.filter(start_paly__gt=now_date)[0:2]
    result = json.loads(serializers.serialize('json', result))
    return JsonResponse(data=result, safe=False)