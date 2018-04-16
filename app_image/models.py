from django.db import models


class ImageSource(models.Model):
    href = models.TextField(blank=True, null=True)  # 链接
    title = models.CharField(max_length=255, blank=True, null=True)  # 标题，如果有
    source = models.CharField(max_length=255, blank=True, null=True)  # 来源
    source_type = models.CharField(max_length=255, blank=True, null=True)  # 来源类型
    remark = models.TextField(blank=True, null=True)  # 备注
    show_times = models.IntegerField(default=0)  # 显示次数
    select_times = models.IntegerField(default=0)  # 搜索次数
    like_times = models.IntegerField(default=0)  # 喜欢
    dislike_times = models.IntegerField(default=0)  # 不喜欢
    report_times = models.IntegerField(default=0)  # 举报
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)  # 更新日期

    def __str__(self):
        return self.href
