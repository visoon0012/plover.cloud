from django.contrib import admin

from app_image.models import ImageSource


class ImageSourceAdmin(admin.ModelAdmin):
    list_display = ('href', 'source', 'source_type', 'title')


admin.site.register(ImageSource, ImageSourceAdmin)
