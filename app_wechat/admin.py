from django.contrib import admin
from .models import *


admin.site.register(WechatResponse)
admin.site.register(WechatRequest)
admin.site.register(UserWechatRequest)