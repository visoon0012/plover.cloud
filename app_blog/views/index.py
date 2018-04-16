# from django.contrib.auth.models import User
# from django.db.models import Count
# from django.shortcuts import render
#
# from app_blog.models import Blog
#
#
# def index(request):
#     """
#     博客园界面
#     :param request:
#     :return:
#     """
#     users = Blog.objects.all().values('author__username').annotate(blog_count=Count('id'))
#     return render(request, 'blog/themes/default/index.html', locals())
