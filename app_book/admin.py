from django.contrib import admin

from app_book.models import Novel, NovelChapter, NovelFork


class NovelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'like_times', 'dislike_times', 'error_times', 'created_time', 'updated_time')


class NovelChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'novel', 'title', 'error_times', 'created_time', 'updated_time')


class NovelForkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'novel', 'read', 'used', 'created_time', 'updated_time')


admin.site.register(Novel, NovelAdmin)
admin.site.register(NovelChapter, NovelChapterAdmin)
admin.site.register(NovelFork, NovelForkAdmin)
