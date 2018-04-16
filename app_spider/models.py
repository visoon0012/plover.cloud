from django.db import models


class DomSource(models.Model):
    """
    网页源码
    """
    url = models.TextField()  # 链接-全
    dom = models.TextField(blank=True, null=True)  # dom 内容
    source = models.CharField(max_length=255, blank=True, null=True)  # 来源
    source_type = models.CharField(max_length=255, blank=True, null=True)  # 来源类型
    remark = models.TextField(blank=True, null=True)  # 备注
    status = models.CharField(max_length=255, blank=True, null=True)  # 状态
    read_times = models.IntegerField(default=0)  # 解析次数
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)  # 更新日期

    def __str__(self):
        return self.url


class Proxy(models.Model):
    """
    代理
    """
    uuid = models.CharField(max_length=100, unique=True)  # ip+port的UUID，防止重复
    ip = models.CharField(max_length=255)  # ip
    port = models.CharField(max_length=10)  # port
    type = models.CharField(max_length=10)  # http/https
    survival_time = models.CharField(max_length=255)  # 存活时间
    verification_time = models.CharField(max_length=255)  # 检测时间

    def __str__(self):
        return '%s:%s' % (self.ip, self.port)


class UrlResource(models.Model):
    """
    待爬取资源
    """
    uuid = models.CharField(max_length=100, unique=True)  # 网址的UUID，防止重复
    href = models.TextField()  # 网址链接
    title = models.CharField(max_length=255, blank=True, null=True)  # 标题
    source = models.CharField(max_length=255, blank=True, null=True)  # 来源
    source_type = models.CharField(max_length=255, blank=True, null=True)  # 来源类型 - 电影/电视剧
    spider_times = models.IntegerField(default=0)  # 解析次数
    error_times = models.IntegerField(default=0)  # 错误次数
    is_alive = models.BooleanField(default=True)  # 是否存活，不存活的不爬取
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)  # 更新日期

    def __str__(self):
        return self.href


class Job(models.Model):
    """
    工作信息
    """
    source = models.CharField(max_length=255, default='gxrc.com', blank=True, null=True)  # 来源
    href = models.TextField()  # 网址链接
    uuid = models.CharField(max_length=100, unique=True)  # 网址的UUID，防止重复
    job_name = models.CharField(max_length=255)  # 工作名称
    company_name = models.CharField(max_length=255, blank=True, null=True)  # 公司名称
    amount = models.CharField(max_length=255, blank=True, null=True)  # 工资
    place = models.CharField(max_length=255, blank=True, null=True)  # 上班地点
    update = models.CharField(max_length=255, blank=True, null=True)  # 最后更新时间
    number = models.CharField(max_length=255, blank=True, null=True)  # 招聘人数
    education = models.CharField(max_length=255, blank=True, null=True)  # 学历要求
    experience = models.CharField(max_length=255, blank=True, null=True)  # 经验要求
    nature = models.CharField(max_length=255, blank=True, null=True)  # 公司性质
    welfare = models.TextField()  # 公司福利
    # 拓展信息
    job_info = models.TextField()  # 工作内容及要求
    company_info = models.TextField()  # 公司信息
    company_address = models.TextField()  # 公司地址

    # 自定义信息
    job_keywords = models.TextField()  # 工作关键字
    company_keywords = models.TextField()  # 公司关键字

    def __str__(self):
        return self.job_name
