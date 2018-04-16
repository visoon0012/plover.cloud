from django.contrib import admin

from app_blog.models import Category, Tag, Blog, Comment

admin.site.register([Category, Tag, Blog, Comment])
