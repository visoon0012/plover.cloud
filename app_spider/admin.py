from django.contrib import admin

# Register your models here.
from app_spider.models import Job, UrlResource


class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'company_name', 'nature', 'amount', 'update')
    search_fields = ('company_name', 'nature',)


class UrlResourceAdmin(admin.ModelAdmin):
    list_display = ('href', 'title', 'spider_times', 'error_times', 'is_alive', 'created_time', 'updated_time')


admin.site.register(Job, JobAdmin)
admin.site.register(UrlResource, UrlResourceAdmin)
