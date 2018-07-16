from django.db import models

from app_user.models import User


class DoubanMovieSimple(models.Model):
    """
    豆瓣电影封面简介 - 用于排序之类的
    """
    douban_id = models.CharField(max_length=190, blank=True, null=True)  # 豆瓣id
    title = models.CharField(max_length=255, blank=True, null=True)  # 标题
    cover = models.CharField(max_length=255, blank=True, null=True)  # 封面
    cover_x = models.IntegerField(default=0)  # 封面宽度
    cover_y = models.IntegerField(default=0)  # 封面高度
    is_new = models.BooleanField(default=False)  # 是否新出
    rate = models.CharField(max_length=255, blank=True, null=True)  # 评分
    url = models.CharField(max_length=255, blank=True, null=True)  # 链接地址

    douban_tag = models.CharField(max_length=190, blank=True, null=True)  # 豆瓣标签
    douban_type = models.CharField(max_length=190, blank=True, null=True)  # 豆瓣类型
    level = models.IntegerField(default=0)  # 等级高度，越高排名越前

    resources = models.IntegerField(default=0)  # 资源数

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DoubanMovie(models.Model):
    """
    豆瓣电影详情
    """
    douban_id = models.CharField(max_length=190, blank=True, null=True, unique=True)  # 豆瓣id，唯一值
    json_data = models.TextField()  # 豆瓣返回的信息
    show_times = models.IntegerField(default=0)  # 显示次数
    select_times = models.IntegerField(default=0)  # 搜索次数

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class MovieResource(models.Model):
    """
    电影下载链接
    """
    title = models.CharField(max_length=255, blank=True, null=True)  # 片名
    name = models.CharField(max_length=255, blank=True, null=True)  # 资源名称
    source = models.CharField(max_length=255, blank=True, null=True)  # 来源
    source_type = models.CharField(max_length=255, blank=True, null=True, default='')  # 电影类型：movie/tv
    download_link = models.TextField(blank=True)  # 下载链接
    download_uuid = models.CharField(max_length=100, null=True, default=None, unique=True)  # 下载链接的uuid
    show_times = models.IntegerField(default=0)  # 显示次数（被搜索次数）
    like_times = models.IntegerField(default=0)  # 点赞次数
    dislike_times = models.IntegerField(default=0)  # 踩次数
    report_times = models.IntegerField(default=0)  # 举报次数
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MovieImage(models.Model):
    """电影图片"""
    source = models.CharField(max_length=255)  # key
    is_used = models.BooleanField(default=False)  # 是否已使用
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.source


class UserMovieSimpleMark(models.Model):
    """用户电影标记"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户
    movie_simple = models.ForeignKey(DoubanMovieSimple, on_delete=models.CASCADE)  # 关联电影
    is_fork = models.NullBooleanField(null=True, default=None, blank=True)  # 是否已收藏
    is_watched = models.NullBooleanField(null=True, default=None, blank=True)  # 是否已观看
    is_like = models.NullBooleanField(null=True, default=None, blank=True)  # 是否喜欢
    comment = models.TextField(null=True, default=None, blank=True)  # 评论
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s关于%s的评论' % (self.user.username, self.movie_simple.title)

