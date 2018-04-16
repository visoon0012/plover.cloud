from django.db import models
from app_user.models import User


# 系统消息
class SystemMessage(models.Model):
    title = models.CharField(max_length=255)  # 标题
    content = models.TextField()  # 正文
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 用户消息
class UserMessage(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='form_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    content = models.TextField()  # 正文
    is_read = models.BooleanField(default=False)  # 是否已读
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)  # 修改时间

    def __str__(self):
        return self.content
