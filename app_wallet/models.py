from django.contrib.auth.models import User
from django.db import models


class UserWallet(models.Model):
    """
    用户钱包
        一个用户可以有多个钱包
        每个钱包对应一个币种
    """
    user = models.ForeignKey(User)
    wallet_type = models.IntegerField(default=0)  # 钱包类型(币种) 0-BTC，1-LTC
    address = models.CharField(max_length=255)  # 钱包地址
    status = models.IntegerField(default=0)  # 状态

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "用户：%s - %s - %s" % (self.user.username, self.wallet_type, self.address)


class WalletFlow(models.Model):
    """
    钱包流水
    """
    wallet = models.ForeignKey(UserWallet)
    trade_type = models.IntegerField(default=0)  # 0-未知，1-进账，2-出账
    address = models.CharField(max_length=255, blank=True, default='')  # 地址
    status = models.IntegerField(default=0)  # 状态

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.trade_type, self.address)
