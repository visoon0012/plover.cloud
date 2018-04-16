from django.contrib import admin

from app_movie.models import MovieResource, DoubanMovie, DoubanMovieSimple, UserMovieSimpleMark


class MovieResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'download_uuid', 'source', 'created_time', 'updated_time')
    search_fields = ('title', 'name', 'download_uuid',)


class DoubanMovieAdmin(admin.ModelAdmin):
    list_display = ('douban_id', 'show_times', 'select_times', 'created_time', 'updated_time')


class UserMovieSimpleMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie_simple', 'is_fork', 'is_watched', 'is_like', 'comment', 'created_time', 'updated_time')


admin.site.register(MovieResource, MovieResourceAdmin)
admin.site.register(DoubanMovie, DoubanMovieAdmin)
admin.site.register(DoubanMovieSimple)
admin.site.register(UserMovieSimpleMark, UserMovieSimpleMarkAdmin)
