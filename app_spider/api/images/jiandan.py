"""
煎蛋网爬虫（后端实现）
"""
import json

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_image.models import ImageSource
from app_spider.models import DomSource
from libs.spider.image_spider import jiandan


@csrf_exempt
def save_jiandan_images(request):
    """
    获取保存煎蛋妹纸图
    :param request:
    :return:
    """
    #
    flag = True
    count = 195
    error_times = 0
    while flag:
        try:
            url = "http://jandan.net/ooxx/page-%s" % count
            print('正在搜索: %s' % url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            images = jiandan.processing(soup)
            for image in images:
                # 检测是否已有该图片
                try:
                    ImageSource.objects.get(href=image)
                    print("已有该图")
                    error_times += 1
                    continue
                except Exception as e:
                    print("未有该图，正在添加：%s" % image)
                    error_times = 0
                image_source = ImageSource.objects.create()
                image_source.href = image
                image_source.source = '煎蛋'
                image_source.source_type = '妹纸图'
                image_source.save()
            count += 1
            if error_times > 100:
                flag = False
        except Exception as e:
            flag = False
            print(e)
            print("终止，当前页数：" + str(count))
    return HttpResponse("获取完毕", content_type="application/json", status=200)
