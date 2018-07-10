from __future__ import absolute_import, unicode_literals

import logging
from datetime import timedelta

from celery.schedules import crontab
from celery.task import periodic_task, task

from app_movie.utils import get_movie_simple

logger = logging.getLogger(__name__)


@periodic_task(run_every=(crontab(minute='0', hour='1')), ignore_result=True, )
def auto_get_movie_simple_0():
    get_movie_simple('movie', '热门')


@periodic_task(run_every=(crontab(minute='5', hour='1')), ignore_result=True, )
def auto_get_movie_simple_1():
    get_movie_simple('movie', '最新')


@periodic_task(run_every=(crontab(minute='10', hour='1')), ignore_result=True, )
def auto_get_movie_simple_2():
    get_movie_simple('tv', '热门')


@periodic_task(run_every=(crontab(minute='15', hour='1')), ignore_result=True, )
def auto_get_movie_simple_3():
    get_movie_simple('tv', '国产剧')


@periodic_task(run_every=(crontab(minute='20', hour='1')), ignore_result=True, )
def auto_get_movie_simple_4():
    get_movie_simple('tv', '美剧')


@periodic_task(run_every=(crontab(minute='25', hour='1')), ignore_result=True, )
def auto_get_movie_simple_5():
    get_movie_simple('tv', '日剧')


@periodic_task(run_every=(crontab(minute='30', hour='1')), ignore_result=True, )
def auto_get_movie_simple_6():
    get_movie_simple('tv', '韩剧')
