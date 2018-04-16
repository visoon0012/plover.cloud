from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=255, default='')  # 昵称
    introduction = models.TextField(default='')  # 简介
    phone = models.CharField(max_length=255, default='')  # 用户绑定的手机号
    score = models.IntegerField(default=0)  # 积分
    like_times = models.IntegerField(default=0)  # 点赞次数
    dislike_times = models.IntegerField(default=0)  # 被踩次数
    report_times = models.IntegerField(default=0)  # 被举报次数

    def __str__(self):
        return self.username
