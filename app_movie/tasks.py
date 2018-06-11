from __future__ import absolute_import, unicode_literals

import logging
from datetime import timedelta

from celery.task import periodic_task

from app_movie.utils import get_movie_simple

logger = logging.getLogger(__name__)

@periodic_task(run_every=(timedelta(hours=12)), ignore_result=True, )
def auto_get_movie_simple():
    get_movie_simple('movie', '热门')
    get_movie_simple('movie', '最新')
    get_movie_simple('tv', '热门')
    get_movie_simple('tv', '国产剧')
    get_movie_simple('tv', '美剧')
    get_movie_simple('tv', '日剧')
    get_movie_simple('tv', '韩剧')
