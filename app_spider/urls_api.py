from django.conf.urls import url

from app_spider.api.poem import searcher
from app_spider.api.book import douban
from app_spider.api.images import jiandan
from app_spider.api.movie import spider
from app_spider.api.job import gxrc
from app_spider.api.proxies import xicidaili

urlpatterns = [
    # proxy
    url(r'^proxy/xicidaili/$', xicidaili.processing),
    # job
    url(r'^job/gxrc/list/$', gxrc.processing_list),
    url(r'^job/gxrc/data/$', gxrc.processing_data),
    # image
    url(r'^image/jiandan/ooxx/$', jiandan.save_jiandan_images),
    # book
    url(r'^book/douban/save/$', douban.save_douban_book),
    # poem
    url(r'^poem/save/$', searcher.processing_detail),
    # movie
    url(r'^movie/processing/index/$', spider.processing_index),
    url(r'^movie/processing/detail/$', spider.processing_detail),
]
