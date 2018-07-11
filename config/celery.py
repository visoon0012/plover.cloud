from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import timedelta

from celery.utils.log import get_task_logger
from django.conf import settings
from kombu import Queue, Exchange

logger = get_task_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# app = Celery('config', include=['apps.chat.tasks', ])
app = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.CELERYD_CONCURRENCY = 2  # 任务并发数
app.conf.CELERYD_TASK_SOFT_TIME_LIMIT = 30  # 任务超时时间
app.conf.CELERY_DISABLE_RATE_LIMITS = True  # 任务频率限制开关
app.conf.enable_utc = False
app.conf.timezone = "Asia/Shanghai"
