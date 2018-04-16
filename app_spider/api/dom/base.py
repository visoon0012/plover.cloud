import json

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_spider.models import DomSource


@csrf_exempt
def save_dom(request):
    """
    保存页面 - DOM
    :param request:
    :return:
    """
    json_data = json.loads(request.body.decode("utf-8"))  # 分析
    flag = False
    # 检测是否已有该url
    try:
        DomSource.objects.get(url=json_data['url'])
    except ObjectDoesNotExist as e:
        flag = True
    except Exception as e:
        print(e)
    # 没有，保存
    if flag:
        dom_temp = DomSource.objects.create(url=json_data['url'],
                                            dom=json_data['dom'],
                                            source=json_data['source'],
                                            source_type=json_data['source_type'])
        dom_temp.save()
        return HttpResponse(json.dumps({'message': '保存成功'}), content_type="application/json", status=200)
    else:
        return HttpResponse('保存失败，已有该资源', content_type="application/json", status=400)
