from django.db import models

from app_user.models import User


class Category(models.Model):
    """
    博客分类
    """
    name = models.CharField(verbose_name='名称', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    博客标签
    """
    name = models.CharField(verbose_name='名称', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    """
    博客
    """
    title = models.CharField(verbose_name='标题', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField(verbose_name='博客正文')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    评论
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='博客')
    name = models.CharField(verbose_name='称呼', max_length=255)
    email = models.EmailField(verbose_name='邮箱')
    content = models.CharField(verbose_name='内容', max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
