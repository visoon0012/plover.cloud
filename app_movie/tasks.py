from __future__ import absolute_import, unicode_literals

import logging
from datetime import timedelta

from celery import shared_task
from celery.task import periodic_task

logger = logging.getLogger(__name__)


# 模拟一个耗时操作
@periodic_task(run_every=(timedelta(seconds=6)), ignore_result=True, )
def test():
    logger.warning('自动任务调起')
