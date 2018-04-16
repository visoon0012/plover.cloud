from django.contrib import admin

from app_user.models import User


# class UserInfoAdmin(admin.ModelAdmin):
#     list_display = ('phone', 'score', 'token',)
#
#
# admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(User)
