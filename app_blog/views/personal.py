# import json
#
# from django.contrib.auth.models import User
# from django.forms import model_to_dict
# from django.http import HttpResponseRedirect, HttpResponse
# from django.shortcuts import render
# from django.urls import reverse
# from django.utils.safestring import mark_safe
# from markdown import markdown
#
# from app_blog.forms import BlogSaveForm
# from app_blog.models import Blog, Tag, Category, Comment
# from libs.util.auth import login_auth_view, post_auth
#
#
# @login_auth_view
# def center(request):
#     """
#     博客管理中心
#     :param request:
#     :return:
#     """
#     author = User.objects.get(username=request.session.get('username'))
#     blog_list = Blog.objects.filter(author=author)
#     for blog in blog_list:
#         blog.content = mark_safe(markdown(blog.content))
#     comments = Comment.objects.filter(blog__author=author).order_by('-id')
#     return render(request, 'blog/themes/default/center.html', locals())
#
#
# def home(request, username):
#     """
#     显示首页
#     :param request:
#     :param username:
#     :return:
#     """
#     author = User.objects.get(username=username)
#     blog_list = Blog.objects.filter(author=author)
#     for blog in blog_list:
#         blog.content = mark_safe(markdown(blog.content))
#     tags = Tag.objects.filter(author=author)
#     categories = Category.objects.filter(author=author)
#     return render(request, 'blog/themes/default/home.html', locals())
#
#
# def blog_detail(request, username, blog_id):
#     """
#     显示博客
#     :param request:
#     :param username:
#     :param blog_id:
#     :return:
#     """
#     author = User.objects.get(username=username)
#     tags = Tag.objects.filter(author=author)
#     categories = Category.objects.filter(author=author)
#     blog = Blog.objects.get(id=blog_id)
#     blog.content = mark_safe(markdown(blog.content))
#     comments = Comment.objects.filter(blog=blog)
#     return render(request, 'blog/themes/default/detail.html', locals())
#
#
# def post_comment(request, username, blog_id):
#     """
#     发表评论
#     :param request:
#     :param username:
#     :param blog_id:
#     :return:
#     """
#     blog = Blog.objects.get(id=blog_id)
#     Comment.objects.create(
#         blog=blog,
#         name=request.POST.get('name'),
#         email=request.POST.get('email'),
#         content=request.POST.get('content')
#     ).save()
#     return HttpResponseRedirect(reverse('app_blog_detail', args=(username, blog_id)))
#
#
# @login_auth_view
# def delete_blog(request):
#     if 'blog_id' in request.GET and request.GET.get('blog_id'):
#         Blog.objects.get(id=request.GET.get('blog_id')).delete()
#     return HttpResponseRedirect(reverse('app_blog_center'))
#
#
# @login_auth_view
# def delete_comment(request):
#     if 'comment_id' in request.GET and request.GET.get('comment_id'):
#         Comment.objects.get(id=request.GET.get('comment_id')).delete()
#     return HttpResponseRedirect(reverse('app_blog_center'))
#
#
# @login_auth_view
# def edit_blog(request):
#     """
#     编辑博客
#     :param request:
#     :return:
#     """
#     blog_id = ''
#     title = ''
#     content = ''
#     if request.method == 'GET':
#         if 'blog_id' in request.GET and request.GET.get('blog_id'):
#             blog = Blog.objects.get(id=request.GET.get('blog_id'))
#             blog_id = blog.id
#             title = blog.title
#             content = blog.content
#     return render(request, 'blog/themes/default/edit.html', locals())
#
#
# @login_auth_view
# @post_auth
# def edit_blog_save(request):
#     """
#     编辑博客 - 保存
#     :param request:
#     :return:
#     """
#     form = BlogSaveForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         user = User.objects.get(username=request.session['username'])
#         result = {}
#         if 'blog_id' in cd and cd['blog_id']:
#             blog = Blog.objects.get(id=cd['blog_id'])
#             blog.title = cd['title']
#             blog.content = cd['content']
#             blog.save()
#             result['is_new'] = 0
#         else:
#             blog = Blog.objects.create(
#                 title=cd['title'],
#                 author=user,
#                 content=cd['content']
#             )
#             blog.save()
#             result['is_new'] = 1
#         result['blog_id'] = blog.id
#         return HttpResponse(json.dumps(result), content_type="application/json")
#     else:
#         return HttpResponse(json.dumps(form.errors), content_type="application/json")
