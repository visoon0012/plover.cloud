from __future__ import absolute_import, unicode_literals

import logging
from datetime import timedelta

from celery import shared_task
from celery.task import periodic_task

from app_movie.models import DoubanMovie, DoubanMovieSimple
from app_movie.utils import get_movie_simple
from app_spider.utils import get_resource_urls, get_resources
from libs.spider.movie_spider import douban_spider

logger = logging.getLogger(__name__)


@periodic_task(run_every=(timedelta(hours=12)), ignore_result=True, )
def auto_get_resource_urls():
    get_resource_urls()


@periodic_task(run_every=(timedelta(hours=12)), ignore_result=True, )
def auto_get_resources():
    get_resources()
