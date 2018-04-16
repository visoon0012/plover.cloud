from django.db import models
from app_user.models import User


# 用户SS服务器配置
class UserSSConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    system_ip = models.CharField(max_length=190)  # 服务器用户名
    system_name = models.CharField(max_length=190)  # 服务器用户名
    system_pass = models.CharField(max_length=190)  # 服务器密码

    ss_port = models.IntegerField()  # ss端口
    ss_pass = models.CharField(max_length=190)  # ss密码

    is_share = models.BooleanField(default=False)  # 是否共享
    error_times = models.IntegerField(default=0)  # 错误次数

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.system_ip
