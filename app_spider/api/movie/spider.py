import json
import random
import uuid
from urllib import parse

import datetime
from bs4 import BeautifulSoup
from django.db.models import Min
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_movie.models import MovieResource
from app_spider import utils
from app_spider.models import UrlResource
from libs.spider.movie_spider import dygang, _6vhao, btbtdy, dy2018, piaohua
from libs.spider.proxies import xicidaili


@csrf_exempt
def processing_index(request):
    """处理网页首页"""
    count = utils.get_resource_urls()
    return HttpResponse(json.dumps({'new': count}), content_type="application/json")


@csrf_exempt
def processing_detail(request):
    """处理电影详情页"""
    utils.get_resources()
    return HttpResponse(json.dumps({'message': 'ok'}), content_type="application/json")
