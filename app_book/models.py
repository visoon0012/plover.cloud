from django.db import models

from app_user.models import User


class DoubanBook(models.Model):
    """
    豆瓣图书
    """
    douban_id = models.CharField(max_length=190, blank=True, null=True, unique=True)  # 豆瓣id，唯一值
    json_data = models.TextField()  # 豆瓣返回的信息
    show_times = models.IntegerField(default=0)  # 显示次数
    select_times = models.IntegerField(default=1)  # 搜索次数
    updated_date = models.DateTimeField(auto_now=True)  # 更新日期


class Novel(models.Model):
    """
    小说
    """
    title = models.CharField(max_length=190, blank=True, null=True)  # 小说名称
    author = models.CharField(max_length=190, blank=True, null=True)  # 作者名称
    cover = models.TextField()  # 封面
    intro = models.TextField()  # 简介
    link = models.TextField()  # 小说链接
    like_times = models.IntegerField(default=0)  # 喜欢次数
    dislike_times = models.IntegerField(default=0)  # 不喜欢次数
    error_times = models.IntegerField(default=0)  # 错误次数
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.title, self.author)


class NovelChapter(models.Model):
    """
    小说章节
    """
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)  # 小说
    title = models.CharField(max_length=190, blank=True, null=True)  # 章节名称
    link = models.CharField(max_length=190)  # 原文链接地址
    content = models.TextField()  # 正文
    error_times = models.IntegerField(default=0)  # 错误次数
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.novel.title, self.title)


class NovelFork(models.Model):
    """
    被人Fork的小说
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)  # 小说
    read = models.ForeignKey(NovelChapter, on_delete=models.CASCADE, null=True, blank=True)  # 已经读到哪个章节
    used = models.BooleanField(default=True)  # 是否在用(有些人看着看着可能取消了)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.novel.title)
