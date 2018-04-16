from django.contrib import admin

from app_message.models import SystemMessage


class SystemMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_time',)


admin.site.register(SystemMessage, SystemMessageAdmin)
