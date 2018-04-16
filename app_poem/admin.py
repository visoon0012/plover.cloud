from django.contrib import admin

from app_poem.models import Poem, Author, Tag, Dynasty


class PoemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'dynasty', 'get_tags', 'get_id')
    search_fields = ('title',)


admin.site.register(Poem, PoemAdmin)
admin.site.register(Author)
admin.site.register(Dynasty)
admin.site.register(Tag)
