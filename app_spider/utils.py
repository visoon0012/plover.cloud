import json
import random
import logging
import uuid
from urllib import parse

import datetime
from bs4 import BeautifulSoup
from django.db.models import Min
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_movie.models import MovieResource
from app_spider.models import UrlResource
from libs.spider.movie_spider import dygang, _6vhao, btbtdy, dy2018, piaohua
from libs.spider.proxies import xicidaili

logger = logging.getLogger(__name__)


def get_resource_urls():
    # 1.获取代理
    # 2.爬取几大电影网站首页，把首页URL加入待爬取列表中
    urls = ['btbtdy.com', 'dygang.com', 'dy2018.com', 'piaohua.com', ]
    count = 1
    for url in urls:
        items = []
        try:
            if "dygang" in url:
                items = dygang.processing_index()
            elif "dy2018" in url:
                items = dy2018.processing_index()
            elif "piaohua" in url:
                items = piaohua.processing_index()
            elif "btbtdy" in url:
                items = btbtdy.processing_index()
            else:
                return HttpResponse('没有可以处理的方法', content_type="application/json", status=400)
        except Exception as e:
            pass
        #
        for item in items:
            try:
                url_resource = UrlResource(**item)
                url_resource.uuid = uuid.uuid3(uuid.NAMESPACE_URL, item['href'])
                url_resource.source = url
                url_resource.save()
                count += 1
            except Exception as e:
                pass
    return count


def get_resources():
    # 2.从待爬取数据库中获得待爬取链接。
    now = datetime.datetime.now()
    # start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    # start = now - datetime.timedelta(hours=24*30)
    # 搜索 错误次数小于10次 且 最后更新时间在30天前的电影
    urs = UrlResource.objects.filter(error_times__lte=10)
    # urs = UrlResource.objects.filter(error_times__lte=10, updated_time__lte=start)
    # 搜索搜索次数最少的URL
    # spider_times = urs_set.aggregate(Min('spider_times'))
    # urs = urs_set.filter(spider_times=spider_times['spider_times__min'])
    # 3.爬取信息，存放数据库
    for ur in urs:
        # 分析
        result = []
        try:
            if "dygang" in ur.source:
                result = dygang.processing_detail(ur.href)
            elif "dy2018" in ur.source:
                result = dy2018.processing_detail(ur.href)
            elif "6vhao" in ur.source:
                result = _6vhao.processing_detail(ur.href)
            elif "btbtdy" in ur.source:
                result = btbtdy.processing_detail(ur.href)
            elif "piaohua" in ur.source:
                result = piaohua.processing_detail(ur.href)
        except Exception as e:
            ur.error_times += 1
            pass
        # 保存到数据库
        new_count = 0
        for item in result:
            try:
                movie_resource = MovieResource.objects.create(
                    name=parse.unquote(item['name'][:255] if len(item['name']) > 255 else item['name']),
                    title=parse.unquote(ur.title),
                    download_link=parse.unquote(item['download_link']),
                    download_uuid=uuid.uuid3(uuid.NAMESPACE_URL, parse.unquote(item['download_link'])),
                    source=parse.unquote(item['source']),
                    source_type=ur.source_type
                )
                movie_resource.save()
                new_count += 1
            except Exception as e:
                movie_resource = MovieResource.objects.get(download_uuid=uuid.uuid3(uuid.NAMESPACE_URL, parse.unquote(item['download_link'])))
                movie_resource.source_type = ur.source_type
                movie_resource.save()
                pass
        # 保存搜索次数
        ur.spider_times += 1
        # 判断是否有新增，没有新增错误次数+1，有资源错误次数清零
        if new_count == 0:
            ur.error_times += 1
        else:
            ur.error_times = 0
        ur.save()
        logger.info('处理：%s，数据：%s，新增：%s' % (ur.href, len(result), new_count))
