from django.db import models

from app_user.models import User


class WechatResponse(models.Model):
    """微信返回 - VALUE"""
    message = models.TextField()

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class WechatRequest(models.Model):
    """微信接收 - KEY"""
    message = models.TextField()
    message_type = models.CharField(max_length=190, default='')  # 消息类型
    response = models.ForeignKey(WechatResponse, on_delete=models.SET_NULL, blank=True, null=True)  # 微信返回

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class UserWechatRequest(models.Model):
    """
    用户微信消息
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)  # 用户
    message = models.TextField()

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
