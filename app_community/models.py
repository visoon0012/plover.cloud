from django.db import models

from app_user.models import User


class CommunityKeyword(models.Model):
    """
    圈子 - 关键字
    """
    name = models.CharField(max_length=190)  # 关键字名称
    info = models.TextField()  # 关键字简介

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Community(models.Model):
    """
    圈子
    """
    name = models.CharField(max_length=190)  # 圈子名称
    info = models.TextField(blank=True)  # 圈子简介
    logo_img = models.TextField(blank=True)  # logo图片链接
    qr_code_img = models.TextField(blank=True)  # 群二维码图片链接
    keywords = models.ManyToManyField(CommunityKeyword)  # 圈子关键字
    password = models.CharField(max_length=190)  # 圈子密钥 - 有密钥可以直接加入圈子
    share_code = models.CharField(max_length=190)  # 圈子分享码(通过这个可以快速打开该圈子界面)
    can_search = models.BooleanField(default=True)  # 能否被搜索到

    managers = models.ManyToManyField(User)  # 管理员
    members = models.ManyToManyField(User)  # 圈子成员(管理员也属于成员)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class CommunityTwitter(models.Model):
    """
    圈子里的推特(微博) - 只能发一张图
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 发布者
    info = models.TextField(blank=True)  # 内容
    img = models.TextField(blank=True)  # 图片链接
    communities = models.ManyToManyField(Community)  # 所属圈子(在哪个圈子可以看到)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class CommunityTwitterComments(models.Model):
    """
    推特评论
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='评论人')  # 发布者
    to_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='被评论人')  # 被评论人
    info = models.TextField()  # 内容
    community_twitter = models.ForeignKey(CommunityTwitter, on_delete=models.CASCADE)  # 评论的推特

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
