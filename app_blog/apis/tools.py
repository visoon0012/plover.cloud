# import json
#
# from django.http import HttpResponse
# from django.utils.safestring import mark_safe
# from django.views.decorators.csrf import csrf_exempt
# from markdown import markdown
#
# from libs.util.auth import login_auth_view
#
#
# @csrf_exempt
# @login_auth_view
# def change_to_markdown(request):
#     """
#     博客文本 to markdown
#     :param request:
#     :return:
#     """
#     content = request.POST.get('content', '')
#     content = mark_safe(markdown(content))
#     return HttpResponse(json.dumps({'content': content}), content_type="application/json")
