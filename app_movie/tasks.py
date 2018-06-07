from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


# 模拟一个耗时操作
@shared_task
def longtime_test():
    logger.warning('自动任务调起')
