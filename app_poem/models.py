from django.db import models


class Author(models.Model):
    """
    作者
    """
    name = models.CharField(max_length=255)  # 作者名字
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dynasty(models.Model):
    """
    朝代
    """
    name = models.CharField(max_length=255)  # 朝代名字
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=255)  # 标签名字
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Poem(models.Model):
    """
    诗
    """
    get_id = models.IntegerField(default=0)  # 获取的id，防止重复
    title = models.CharField(max_length=255)  # 标题
    content = models.TextField()  # 正文
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # 作者
    dynasty = models.ForeignKey(Dynasty, on_delete=models.CASCADE)  # 朝代
    tags = models.ManyToManyField(Tag)  # 标签
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_time = models.DateTimeField(auto_now=True)

    def get_tags(self):
        return " / ".join([tag.name for tag in self.tags.all()])

    def __str__(self):
        return self.title
