from django.http import HttpResponse,JsonResponse
import requests,json
from backend.models import HomeInformation
from django.core import  serializers



def home_date(request):
    result = HomeInformation.objects.all()
    result = json.loads(serializers.serialize('json', result))

    return JsonResponse(data=result,safe=False)
