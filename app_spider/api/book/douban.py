"""
对接豆瓣图书接口
"""

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_book.models import DoubanBook


@csrf_exempt
def processing_douban_book(request):

    return HttpResponse(json.dumps({'message': '处理完毕'}), content_type="application/json")


@csrf_exempt
def save_douban_book(request):
    """
    保存前端传来的豆瓣book信息，回传最后一个豆瓣图书id
    :param request:
    :return:
    """
    json_data = json.loads(request.body.decode("utf-8"))
    douban_id = json_data['douban_id']
    if douban_id == 0:
        # 表示前端刚开始搜索，不知道最后搜索到的ID
        douban_book_last = DoubanBook.objects.order_by('-douban_id').first()
        return HttpResponse(json.dumps({'douban_id': douban_book_last.douban_id}), content_type="application/json")
    else:
        # 保存到数据库
        json_data = json_data['json_data']
        DoubanBook.objects.create(
            douban_id=douban_id,
            json_data=json_data,
        ).save()
        return HttpResponse(json.dumps({'douban_id': douban_id}), content_type="application/json")
